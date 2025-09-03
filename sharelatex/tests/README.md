# Run tests on local with gitlabci-local
to run continus integration tests designed to run in gitlab.inria.fr in your local machine, you can install [gitlabci-local](https://pypi.org/project/gitlabci-local/)

`pip install gitlabci-local`

then run : `gcil --real-paths  --sockets --list` or in short `gcil -rSl`
to select the stage and job you want to run manually.
to run a specific job for example `py312-functional` just run :

`gcil -rS py312-functional`

This start specific dockers containers for tests, in our case this use real path for bind path in containers and sockets for emulated nested containers
(some jobs seems to run without real path, for exemple `tox`, just run `gcil -S tox`)
