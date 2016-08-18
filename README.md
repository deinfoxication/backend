# deinfoxication backend

## Git flow
We use git flow to control releases and stuff, to initialize your repository you need to run `git flow init -d`.
To send features to the project always use `git flow feature`.
No pull request can be accepted on the master branch and all releases must have a proper `git flow release` with the
desired tag respecting [SEMVER](http://semver.org/).
