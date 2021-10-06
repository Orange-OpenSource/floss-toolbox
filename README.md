# floss-toolbox (version 2.1.0)

Toolbox to help developers and open source referents to have cleaner projects in GitHub organizations.

Toolbox is mainly written in Shell because this language is very efficient for files processing and provides a strong and rich standard API with cool primitives. Contains also Ruby scripts.

## Environment

You must have a _BASH_ ready environment and also _Ruby_.
For example, _Bash_ version here is _3.2.5_.

## Project tree

_toolbox/diver_ contains several scripts you need. At the root of this folder are _Shell_ main scripts.
_toolbox/diver/utils_ contains the programs called from the _Shell_ main scripts.
_toolbox/diver/data_ contains some datasets and projects samples to work on.
_toolbox/github_ contains _Ruby_ and _Shell_ scripts to use so as to deal with _GitHub_ REST API.

**Please, note for this version you have to copy/paste your project in the _toolbox/diver/data_ folder because non-absolute paths and commands are used in the scripts**

## The "diver" of source code and commits

### File of words

Some features parse a text file containing the words to look for in sources or git logs.
Items in this file can be separated with ';' and line breaks.

For example the following extract defines a list of words to find like first names, last names and sensitive words.
```
Foo;Bar;foo.bar@wizz.com
Alice;NoOne;alice.noone@where.com
Bod;Tinkerer;bob.the-tinkerer@company.com
password
login
```

### Features

#### Find contributors in files

The tooblox can look in each file of a project for words.
Such words may be developers' first names, last names, email addresses or whatever you want.
A report is created with a curated list of found words in precise files.

To run the feature:
```shell
bash find-contributor-in-files.sh --target path/to/project
```

This script uses another _Shell_ script in _utils_ folder (_find-hotwords-files.sh_) and expects to have a defined and readable file in _data_ folder (named _contributors-entries.txt_). Thus only the project to scan can be given in parameter of the script, and the file of contributors to look for can be versionned or statically defined.

Note this version provides a naive implementation for file processing which should be improved to reduce the computation time.
In fact this implementation is based on a three-levels-based loop: each line of each file is checked for each word.
Not so efficient, but it works and is suitable for first releases.

#### Find contributors in git log

The toolbox provides a script which can check in git logs if some words (first name, last name, emails, whatever you wrote) are used.
A report is created with a curated list of found words and associated commits.

To run the feature:
```shell
bash find-contributors-in-git-logs.sh --words path/to/file-of-words --project path/to/project --loglimit git-log-limit
```

For example, the words to find have to be listed in the _path/to/file-of-words_ file.
The log limit is the value to pass to the `git log` command, e.g. _2.weeks_ or _3.years_.
_path/to/the/project_ points to the root of the project to analyse.

#### Find credentials in sources

We assume the source code to analyse is not hosted on a git-based project, that is the reason why such tools like _git grep_ are not used.
This feature will look in the files for some keywords like passwords or logins.

To run the feature:
```shell
bash find-credentials-in-files.sh --project path/to/project
```

This script uses another _Shell_ script in _utils_ folder (_find-hotwords-files.sh_) and expect to have a defined and readable file in _data_ folder (named _contributors-entries.txt_). Thus only the project to scan can be given in parameter of the script, and the file of credentials to look for can be versionned or statically defined.

Note this version provides a naive implementation for file processing which should be improved to reduce the computation time.
In fact this implementation is based on a three-levels-based loop: each line of each file is checked for each word.
Not so efficient, but it works and is suitable for first releases.

Exemple of file listing credentials-relayed words:
```
login
password
pwd
key
ssh
host
account
mail
access
port
pass
```

#### Find missing signed-off fields

Depending to the project we may want to have signed-off commits so as to agree to the Developer Certificate of Origin (https://developercertificate.org/).
Thus we may want to look in git commits messages if the signed-off field has been defined or not.
We want also to ensure each commit has an author.

To run the feature:
```shell
bash find-missing-developers-in-git-commits.sh --project path/to/project --loglimit git-log-limit
```

The log limit is the value to pass to the `git log` command, e.g. _2.weeks_ or _3.years_.
_path/to/the/project_ points to the root of the project to analyse.

#### Find credits

We can also check in sources if some hotwords are used, mainly about credits or copyrights notices.
For example, "credit", "created by" or "(C)" can refer to third-party components we missed to list.

To run the feature:
```shell
bash find-credits-in-files.sh --target path/to/project
```

This script uses another _Shell_ script in _utils_ folder (_find-hotwords-files.sh_) and expect to have a defined and readable file in _data_ folder (named _notices-entries.txt_). Thus only the project to scan can be given in parameter of the script, and the file of contributors to look for can be versionned or statically defined.

Note this version provides a naive implementation for file processing which should be improved to reduce the computation time.
In fact this implementation is based on a three-levels-based loop: each line of each file is checked for each word.
Not so efficient, but it works and is suitable for first releases.

Exemple of file listing hotwords for credits:
```
copyright;(C);©
author;authors
credit
created
```

### Play with GitHub web API

### Prerequisites

- Ruby Gem: `octokit 4.20.0`
- Ruby Gem: `git 1.8.1`
- Ruby 2.7.1

- Create a [GitHub personal token](https://github.com/settings/tokens) and define it in the _configuration.rb_ file for the `GITHUB_PERSONAL_ACCESS_TOKEN` variable.
- Define the _GitHub_ organization name in the _configuration.rb_ file for the `GITHUB_ORGANIZATION_NAME`variable. It will allow to send requests to query and modify your organization.
- Define also the logins of the GitHub adminsitrators of your organization so as to prevent to change their permisssion for example.

### Prepare project

```ruby
gem install octokit
gem intall git
```

### Third-party elements

This project uses [Octokit](https://github.com/octokit/octokit.rb) Ruby client, licensed under MIT license.
It also uses [Git](https://github.com/ruby-git/ruby-git) Ruby gem, under MIT license.

### Features

#### Display usage

```shell
bash GitHubWizard.sh
```

#### Get all members of organization

Run the following command and check the file with the FILENAME_MEMBERS name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-all-members
```

#### Get members of organization with 2FA disabled

Run the following command and check the file with the FILENAME_MEMBERS_2FA_DISABLED name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-members-2fa-disabled
```

#### Get members of organization with "company" field undefined

Run the following command and check the file with the FILENAME_MEMBERS_UNDEFINED_COMPANY name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-members-without-company
```

#### Get projects which don't have any assigned team

Run the following command and check the file with the FILENAME_PROJECTS_WITHOUT_TEAM name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-projects-without-team
```

#### Get users which have undefined or hidden email

Run the following command and check the file with the FILENAME_USERS_WITH_BAD_EMAILS name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-users-with-bad-email
```

### Get users which may have not suitable fullname

Run the following command and check the file with the FILENAME_USERS_WITH_BAD_FULLNAMES name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-users-with-bad-fullname
```

### Get repositories with undefined licenses

Run the following command and check the file with the FILENAME_PROJECTS_WITHOUT_LICENSES (_configuration.rb_)
```shell
bash GitHubWizard.sh get-projects-without-licenses
```

### Get repositories which seems to be unconform (i.e. missing files)

Run the following command and check the file with the FILENAME_PROJECTS_WITH_UNCONFORM_REPOSITORIES name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-projects-conformity
```
SSH will be used to clone repositories, thus you must have your SSH configuration ready:

1. Create an SSH key on your GitHub account [settings](https://github.com/settings/keys)
2. Add the SSH key in your environment

```shell
ssh-add .ssh/id_rsa
```

### Get repositories which seems to be empty or have not enough files

Run the following command and check the file with the FILENAME_EMPTY_PROJECTS name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-empty-projects
```
SSH will be used to clone repositories, thus you must have your SSH configuration ready:

1. Create an SSH key on your GitHub account [settings](https://github.com/settings/keys)
2. Add the SSH key in your environment

```shell
ssh-add .ssh/id_rsa
```

### Define users permissions for all projects to "push"

Run the following command to update rights of all users except GitHub teams and GitHub administrators, for all projects.
Permissions will be set to "push", i.e. "write".

```shell
bash GitHubWizard.sh set-users-permissions-to-push
```

### Define teams permissions for all projects to "push"

Run the following command to update rights of all teams, for all projects.
Permissions will be set to "push", i.e. "write".

```shell
bash GitHubWizard.sh set-teams-permissions-to-push
```
