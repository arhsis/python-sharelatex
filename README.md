# Python-sharelatex

Python-sharelatex is a library to interact with <https://sharelatex.irisa.fr>.
It also includes a command line tools to sync your remote project with git.
This allows you to work offline on your project and later sync your local copy with the remote one.

**Note: The <https://sharelatex.tum.de> only works with the branch `feature/sharelatextum`!**

## Links

- Source: <https://gitlab.inria.fr/sed-rennes/sharelatex>
- Documentation: <https://sed-rennes.gitlabpages.inria.fr/sharelatex/python-sharelatex>
- Mattermost: <https://mattermost.irisa.fr/sed-rba/channels/sharelatex-users>
- PyPI: <https://pypi.org/project/sharelatex/>

**The code is currently experimental and under development. Use it with caution.**

## Installation

### Via Docker

```shell
docker run --workdir /data --volume $(pwd):/data -it ghcr.io/pstoeckle/docker-images/sharelatex-tum:sha-eed00b6
```

### Via git and pip

```shell
git clone https://gitlab.inria.fr/sed-rennes/sharelatex/python-sharelatex
cd python-sharelatex
git checkout feature/sharelatextum
pip install -e .
```

## Compatibility notes

The tool is targetting the community edition of ShareLatex/Overleaf and we are testing it on:

- <https://sharelatex.irisa.fr> \-- `legacy` authentication method
- <https://overleaf.irisa.fr> \-- `gitlab` authentication method
- Overleaf CE (3.0.1) \-- `community` authentication method

## Persistent sessions

Sessions are persistent and store in the application directory (exact might differ on the OS used).
Is uses [appdirs](https://github.com/ActiveState/appdirs) internally.

## Note on passwords management

Passwords are stored in your keyring service (Keychain, Kwallet \...) thanks to the [keyring](https://pypi.org/project/keyring/) library.
Please refer to the dedicated documentation for more information.

## Quick examples

### Display the possible actions

[slatex]{.title-ref} is a subcommand of git that calls the `git-slatex`
programm shipped by this project.

```shell
$) git slatex

Usage: git-slatex [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  clone    Get (clone) the files from sharelatex projet URL and crate a...
  compile  Compile the remote version of a project
  new      Upload the current directory as a new sharelatex project
  pull     Pull the files from sharelatex.
  push     Push the commited changes back to sharelatex
```

For instance, you can get the help on a specific sub-command with the
following:

```shell
git slatex clone --help
```

### Get an existing project on slatex

```shell
$ git slatex clone --help
Usage: git-slatex clone [OPTIONS] [PROJET_URL] [DIRECTORY]

  Get (clone) the files from sharelatex project URL and create a local git
  depot.

  The optional target directory will be created if it doesn't exist. The
  command fails if it already exists. Connection information can be saved in
  the local git config.

  It works as follow:

      1. Download and unzip the remote project in the target directory

      2. Initialize a fresh git repository

      3. Create an extra ``__remote__sharelatex__`` to keep track of the
      remote versions of        the project. This branch must not be updated
      manually.

Options:
  --https-cert-check / --no-https-cert-check
                                  force to check https certificate or not
  --whole-project-download / --no-whole-project-download
                                  download whole project in a zip file from
                                  the server/ or download sequentially file by
                                  file from the server
  --login-username-tag TEXT       Most services expect email=...,
                                  password=....         However, some expect
                                  login=...,password. Thus, you can pass this
                                  other         tag via this option.

                                  Default='email'
  -l, --login-path TEXT           Only useful with the legacy authentication.
                                  You can pass         here the login path,
                                  e.g., ldap/login.

                                  Default: '/login'
  --ignore-saved-user-info BOOLEAN
                                  Forget user account information already
                                  saved (in OS keyring system)
  --save-password / --no-save-password
                                  Save user account information (in OS keyring
                                  system)
  -p, --password TEXT             User password for sharelatex server, if
                                  password is not provided, it will be asked
                                  online
  -u, --username TEXT             Username for sharelatex server account, if
                                  username is not provided, it will be asked
                                  online
  -a, --auth_type [gitlab|community|legacy]
                                  Authentification type.
  --help                          Show this message and exit.
```

#### Example

```shell
mkdir test
cd test
# download all files of a remote project
git slatex clone <project_URL> <local_path_to_project>
```

### Editing and pushing back to slatex

```shell
$ git slatex push --help
Usage: git-slatex push [OPTIONS]

  Synchronize the local copy with the remote version.

  This works as follow:

  1. The remote version is pulled (see the :program:`pull` command)

  2. After the merge succeed, the merged version is uploaded back to the
  remote server.

     Note that only the files that have changed (modified/added/removed) will
     be uploaded.

Options:
  -b, --git-branch TEXT           The name of a branch. We will commit the
                                  changes from Sharelatex on this file.

                                  Default: __remote__sharelatex__
  --force                         Force push
  --login-username-tag TEXT       Most services expect email=...,
                                  password=....         However, some expect
                                  login=...,password. Thus, you can pass this
                                  other         tag via this option.

                                  Default='email'
  -l, --login-path TEXT           Only useful with the legacy authentication.
                                  You can pass         here the login path,
                                  e.g., ldap/login.

                                  Default: '/login'
  --ignore-saved-user-info BOOLEAN
                                  Forget user account information already
                                  saved (in OS keyring system)
  --save-password / --no-save-password
                                  Save user account information (in OS keyring
                                  system)
  -p, --password TEXT             User password for sharelatex server, if
                                  password is not provided, it will be asked
                                  online
  -u, --username TEXT             Username for sharelatex server account, if
                                  username is not provided, it will be asked
                                  online
  -a, --auth_type [gitlab|community|legacy]
                                  Authentification type.
  --allow-list-for-local-files FILE
                                  You can pass a file with patterns. Local
                                  files that match these patterns will not be
                                  deleted although they are not present on the
                                  server
  --help                          Show this message and exit.
```

#### Example 2

```shell
# edit your files
# commit, commit, commit ...
#
# Push back your change to sharelatex
git slatex push
```

Concurrent updates may occur between your local files (because you
changed them) and the remote ones (because you collaborators changed
them). So before pushing, we try to make sure the merge between the
remote copy and the local ones is ok. You\'ll have to resolve the
conflict manually (as usual with Git) and attempt a new push.

### Pull changes from ShareLaTeX to local (like a git pull)

```shell
$ git slatex pull --help
Usage: git-slatex pull [OPTIONS]

  Pull the files from sharelatex.

  In the current repository, it works as follows:

  1. Pull in ``__remote__sharelatex__`` branch the latest version of the
  remote project

  2. Attempt a merge in the working branch. If the merge can't be done
  automatically,    you will be required to fix the conflict manually

Options:
  -b, --git-branch TEXT           The name of a branch. We will commit the
                                  changes from Sharelatex on this file.

                                  Default: __remote__sharelatex__
  --allow-list-for-local-files FILE
                                  You can pass a file with patterns. Local
                                  files that match these patterns will not be
                                  deleted although they are not present on the
                                  server
  --login-username-tag TEXT       Most services expect email=...,
                                  password=....         However, some expect
                                  login=...,password. Thus, you can pass this
                                  other         tag via this option.

                                  Default='email'
  -l, --login-path TEXT           Only useful with the legacy authentication.
                                  You can pass         here the login path,
                                  e.g., ldap/login.

                                  Default: '/login'
  --ignore-saved-user-info BOOLEAN
                                  Forget user account information already
                                  saved (in OS keyring system)
  --save-password / --no-save-password
                                  Save user account information (in OS keyring
                                  system)
  -p, --password TEXT             User password for sharelatex server, if
                                  password is not provided, it will be asked
                                  online
  -u, --username TEXT             Username for sharelatex server account, if
                                  username is not provided, it will be asked
                                  online
  -a, --auth_type [gitlab|community|legacy]
                                  Authentification type.
  --help                          Show this message and exit.
```

#### Example 3

```shell
# Pull changes from sharelatex
git slatex pull
```

### Create a remote project from a local git
```shell
git slatex new --help
Usage: git-slatex new [OPTIONS] PROJECTNAME BASE_URL

  Upload the current directory as a new sharelatex project.

  This literally creates a new remote project in sync with the local version.

Options:
  --https-cert-check / --no-https-cert-check
                                  force to check https certificate or not
  --whole-project-upload / --no-whole-project-upload
                                  upload whole project in a zip file to the
                                  server/ or upload sequentially file by file
                                  to the server
  --rate-max-uploads-by-sec FLOAT
                                  number of max uploads by seconds to the
                                  server (some servers limit the this rate),
                                  useful with --no-whole-project-upload
  --login-username-tag TEXT       Most services expect email=...,
                                  password=....         However, some expect
                                  login=...,password. Thus, you can pass this
                                  other         tag via this option.

                                  Default='email'
  -l, --login-path TEXT           Only useful with the legacy authentication.
                                  You can pass         here the login path,
                                  e.g., ldap/login.

                                  Default: '/login'
  --ignore-saved-user-info BOOLEAN
                                  Forget user account information already
                                  saved (in OS keyring system)
  --save-password / --no-save-password
                                  Save user account information (in OS keyring
                                  system)
  -p, --password TEXT             User password for sharelatex server, if
                                  password is not provided, it will be asked
                                  online
  -u, --username TEXT             Username for sharelatex server account, if
                                  username is not provided, it will be asked
                                  online
  -a, --auth_type [gitlab|community|legacy]
                                  Authentification type.
  --help                          Show this message and exit.
```

#### Example 4

```shell
git slatex new <base_server_URL> <new_project_name>
```
