# deinfoxication backend

## What is deinfoxication?
deinfoxication comes from [infoxication](https://en.wikipedia.org/wiki/Information_overload) and it is basically a feed reader that learns which news are more relevant to you based on your own ratings instead of social and popularity stuff.

## Git flow
We use git flow to control releases and stuff, to initialize your repository you need to run `git flow init -d`.
To send features to the project always use `git flow feature`.
No pull request can be accepted on the master branch and all releases must have a proper `git flow release` with the
desired tag respecting [SEMVER](http://semver.org/).
