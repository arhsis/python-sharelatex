import datetime
import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, Mapping, Sequence
from typing import cast as typing_cast
from unittest.mock import MagicMock, patch

from sharelatex import UpdateDatum
from sharelatex.cli import (
    RemoteItem,
    _sync_deleted_items,
    _sync_remote_files,
    remote_last_update_time,
)

UPDATE_DATA: UpdateDatum = {
    "updates": [
        {
            "fromV": 12,
            "toV": 13,
            "meta": {
                "users": [
                    {
                        "first_name": "john.doe",
                        "last_name": "",
                        "email": "john.doe@inria.fr",
                        "id": "62bdbb1c580c7c0095c6e8bd",
                    }
                ],
                "start_ts": 1752762714382,
                "end_ts": 1752762714382,
            },
            "labels": [],
            "pathnames": [],
            "project_ops": [
                {"remove": {"pathname": "test_folder/to_delete.tex"}, "atV": 12}
            ],
        },
        {
            "fromV": 11,
            "toV": 12,
            "meta": {
                "users": [
                    {
                        "first_name": "john.doe",
                        "last_name": "",
                        "email": "john.doe@inria.fr",
                        "id": "62bdbb1c580c7c0095c6e8bd",
                    }
                ],
                "start_ts": 1752762705235,
                "end_ts": 1752762705235,
            },
            "labels": [],
            "pathnames": ["test_folder/to_delete.tex"],
            "project_ops": [],
        },
        {
            "fromV": 9,
            "toV": 11,
            "meta": {
                "users": [
                    {
                        "first_name": "john.doe",
                        "last_name": "",
                        "email": "john.doe@inria.fr",
                        "id": "62bdbb1c580c7c0095c6e8bd",
                    }
                ],
                "start_ts": 1752762624011,
                "end_ts": 1752762700448,
            },
            "labels": [],
            "pathnames": [],
            "project_ops": [
                {"add": {"pathname": "test_folder/to_delete.tex"}, "atV": 10},
                {
                    "rename": {
                        "pathname": "test_folder/test.tex",
                        "newPathname": "test_folder/test_renamed.tex",
                    },
                    "atV": 9,
                },
            ],
        },
        {
            "fromV": 7,
            "toV": 9,
            "meta": {
                "users": [
                    {
                        "first_name": "john.doe",
                        "last_name": "",
                        "email": "john.doe@inria.fr",
                        "id": "62bdbb1c580c7c0095c6e8bd",
                    }
                ],
                "start_ts": 1752762367285,
                "end_ts": 1752762526576,
            },
            "labels": [],
            "pathnames": ["test_folder/test.tex"],
            "project_ops": [],
        },
        {
            "fromV": 6,
            "toV": 7,
            "meta": {
                "users": [
                    {
                        "first_name": "john.doe",
                        "last_name": "",
                        "email": "john.doe@inria.fr",
                        "id": "62bdbb1c580c7c0095c6e8bd",
                    }
                ],
                "start_ts": 1752762358366,
                "end_ts": 1752762358366,
            },
            "labels": [],
            "pathnames": [],
            "project_ops": [{"add": {"pathname": "test_folder/test.tex"}, "atV": 6}],
        },
        {
            "fromV": 5,
            "toV": 6,
            "meta": {
                "users": [
                    {
                        "first_name": "john.doe",
                        "last_name": "",
                        "email": "john.doe@inria.fr",
                        "id": "62bdbb1c580c7c0095c6e8bd",
                    }
                ],
                "start_ts": 1752750657031,
                "end_ts": 1752750657031,
            },
            "labels": [],
            "pathnames": ["main.tex"],
            "project_ops": [],
        },
        {
            "fromV": 0,
            "toV": 5,
            "meta": {
                "users": [],
                "start_ts": 1752576392452,
                "end_ts": 1752576392465,
                "origin": {"kind": "history-resync"},
            },
            "labels": [],
            "pathnames": [],
            "project_ops": [
                {"add": {"pathname": "sample.bib"}, "atV": 2},
                {"add": {"pathname": "main.tex"}, "atV": 1},
                {"add": {"pathname": "frog.jpg"}, "atV": 0},
            ],
        },
    ]
}


class TestRemoteLastUpdateTime(unittest.TestCase):
    def test_remote_last_update_time_file_updated(self) -> None:
        self.assertEqual(
            1752750657031, remote_last_update_time(UPDATE_DATA, "main.tex", "test")
        )

    def test_remote_last_update_time_file_created(self) -> None:
        self.assertEqual(
            1752576392465, remote_last_update_time(UPDATE_DATA, "frog.jpg", "test")
        )


@contextmanager
def into_tmpdir() -> Generator:
    """Run some code in the context of a tmp dir."""

    old_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            os.chdir(tmp_dir)
            yield tmp_dir
        except Exception as e:
            raise e
        finally:
            os.chdir(old_cwd)


def tmpdir(f: Any) -> Any:
    """
    Temporary directory.
    """

    def _wrapped(*args: Any, **kwargs: Any) -> None:
        with into_tmpdir() as tmpdir:  # type: ignore
            # create a dummy env there
            f(*args, Path(tmpdir), **kwargs)

    return _wrapped


class TestPull(unittest.TestCase):
    @patch.object(Path, "rmdir")
    @patch.object(Path, "unlink")
    def test_sync_delete_file_nomore_present_on_server(
        self, mock_unlink: Any, mock_rmdir: Any
    ) -> None:
        # simple test one empty folder in the remote server
        remote_items = typing_cast(
            Sequence[RemoteItem],
            [
                # the rootFolder
                {"folder_id": "0", "name": ".", "folder_path": ".", "type": "folder"}
            ],
        )
        # But one file locally (abs path)
        working_path = Path.cwd()
        f = Path("image.png").resolve()
        files = [f]

        _sync_deleted_items(working_path, remote_items, files)

        mock_rmdir.assert_not_called()
        mock_unlink.assert_called_once()
        mock_unlink.assert_called_with(f)

    @tmpdir  # type: ignore
    def test_sync_remote_files_download_new_files(self, _: Any) -> None:
        remote_items = typing_cast(
            Sequence[RemoteItem],
            [
                {
                    "folder_id": "rootFolderId",
                    "name": ".",
                    "folder_path": ".",
                    "type": "folder",
                },
                {
                    "_id": "myimageId",
                    "folder_id": "0",
                    "name": "myimage.png",
                    "folder_path": ".",
                    "type": "file",
                },
            ],
        )
        client = MagicMock()
        client.get_file = MagicMock()
        project_id = 0
        working_path = Path.cwd()
        # force to read local OS datetime (not git log datetime)
        datetimes_dict: Mapping[str, datetime.datetime] = {}
        _sync_remote_files(
            client, str(project_id), working_path, remote_items, datetimes_dict
        )

        client.get_file.assert_called_once()
        dest_path = working_path / "myimage.png"
        client.get_file.assert_called_with(
            str(project_id), "myimageId", dest_path=str(dest_path)
        )
