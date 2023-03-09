[![Opened issues](https://img.shields.io/github/issues-raw/Orange-OpenSource/floss-toolbox?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/issues)
[![Apache 2.0 license](https://img.shields.io/github/license/Orange-OpenSource/floss-toolbox?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/blob/dev/LICENSE.txt)
[![Versions](https://img.shields.io/github/v/release/Orange-OpenSource/floss-toolbox?label=Last%20version&style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/releases)
[![Still maintained](https://img.shields.io/maintenance/yes/2023?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/issues?q=is%3Aissue+is%3Aclosed)

# FLOSS Toolbox

Toolbox to help developers and open source referents to have cleaner projects in _GitHub_ organizations, and more.

Toolbox is mainly written in _Shell_ because this language is very efficient for files processing and provides a strong and rich standard API with cool primitives. Contains also _Ruby_ scripts. _Ruby_ are shiny gems, I love them. _Python_ is also used.

# Environment

You must have a _BASH_ ready environment and also _Ruby_.
Environment:
- _Bash_ version **3.2.5**
- _Ruby_ version **2.7.1**
- _Python_ version **3.7**

# Project tree

_toolbox/diver_ contains several scripts you need. At the root of this folder are _Shell_ main scripts.
_toolbox/diver/utils_ contains the programs called from the _Shell_ main scripts.
_toolbox/diver/data_ contains some datasets and projects samples to work on.
_toolbox/github_ contains _Ruby_ and _Shell_ scripts to use so as to deal with _GitHub_ REST API.

**Please, note for this version for some features you might have to copy/paste your project in the _toolbox/diver/data_ folder because non-absolute paths and commands are used in the scripts**

# Dry run

To be sure you have a ready-to-run project, you can run the dry-run command:

```shell
bash dry-run.sh
```

# The "diver" of source code and commits

## File of words

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

## Features

### Find contributors in files

_Keywords: #contributors #files #sources #hotwords_

The toolbox can look in each file of a project for words.
Such words may be developers' first names, last names, email addresses or whatever you want.
A report is created with a curated list of found words in precise files.

To run the feature:
```shell
bash find-contributor-in-files.sh --target path/to/project
```

This script uses another _Shell_ script in _utils_ folder (_find-hotwords-files.sh_) and expects to have a defined and readable file in _data_ folder (named _contributors-entries.txt_). Thus only the project to scan can be given in parameter of the script, and the file of contributors to look for can be versioned or statically defined.

Note this version provides a naive implementation for file processing which should be improved to reduce the computation time.
In fact this implementation is based on a three-levels-based loop: each line of each file is checked for each word.
Not so efficient, but it works and is suitable for first releases.

### Find contributors in git log

_Keywords: #contributors #git #history #logs #hotwords_

The toolbox provides a script which can check in git logs if some words (first name, last name, emails, whatever you wrote) are used.
A report is created with a curated list of found words and associated commits.

To run the feature:
```shell
bash find-contributors-in-git-logs.sh --words path/to/file-of-words --project path/to/project --loglimit git-log-limit
```

For example, the words to find have to be listed in the _path/to/file-of-words_ file.
The log limit is the value to pass to the `git log` command, e.g. _2.weeks_ or _3.years_.
_path/to/the/project_ points to the root of the project to analyse.

### Find credentials in sources

_Keywords: #credentials #files #sources #hotwords_

We assume the source code to analyse is not hosted on a git-based project, that is the reason why such tools like _git grep_ are not used.
This feature will look in the files for some keywords like passwords or logins.

To run the feature:
```shell
bash find-credentials-in-files.sh --project path/to/project
```

This script uses another _Shell_ script in _utils_ folder (_find-hotwords-files.sh_) and expect to have a defined and readable file in _data_ folder (named _contributors-entries.txt_). Thus only the project to scan can be given in parameter of the script, and the file of credentials to look for can be versioned or statically defined.

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

### Find missing signed-off fields

_Keywords: #git #commits #history #logs #signed #DCO_

Depending to the project we may want to have signed-off commits so as to agree to the Developer Certificate of Origin (https://developercertificate.org/).
Thus we may want to look in git commits messages if the signed-off field has been defined or not.
We want also to ensure each commit has an author.

To run the feature:
```shell
bash find-missing-developers-in-git-commits.sh --project path/to/project --loglimit git-log-limit
```

The log limit is the value to pass to the `git log` command, e.g. _2.weeks_ or _3.years_.
_path/to/the/project_ points to the root of the project to analyse.

### Find credits

_Keywords: #contributors #authors #credits #copyrights #files #hotwords_

We can also check in sources if some hotwords are used, mainly about credits or copyrights notices.
For example, "credit", "created by" or "(C)" can refer to third-party components we missed to list.

To run the feature:
```shell
bash find-credits-in-files.sh --target path/to/project
```

This script uses another _Shell_ script in _utils_ folder (_find-hotwords-files.sh_) and expect to have a defined and readable file in _data_ folder (named _notices-entries.txt_). Thus only the project to scan can be given in parameter of the script, and the file of contributors to look for can be versioned or statically defined.

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

### List contributors from Git history

_Keywords: #contributors #git #history #logs_

It is possible to make a list of contributors (first name, last name, email) using the remaining traces in the Git history.

To run the feature:
```shell
bash list-contributors-in-history.sh --project path/to.git/project --loglimit git-log-limit
```

The log limit is the value to pass to the `git log` command, e.g. _2.weeks_ or _3.years_.
_path/to/the/project_ points to the root of the project to analyse.


### Extract email address from Git history

_Keywords: #contributors #git #logs #history #email_

It is possible to make a list of contributors email addresses using the remaining traces in the Git history.

To run the feature:
```
bash extract-emails-from-history.sh  --project path/to.git/project --loglimit git-log-limit
```

The log limit is the value to pass to the `git log` command, e.g. _2.weeks_ or _3.years_.
_path/to/the/project_ points to the root of the project to analyse.

# Play with GitHub web API

## Prerequisites

- Ruby Gem: `octokit 4.20.0`
- Ruby Gem: `git 1.8.1`
- Ruby 2.7.1

- Create a [GitHub personal token](https://github.com/settings/tokens) and define it in the _configuration.rb_ file for the `GITHUB_PERSONAL_ACCESS_TOKEN` variable.
- Define the _GitHub_ organization name in the _configuration.rb_ file for the `GITHUB_ORGANIZATION_NAME` variable. It will allow to send requests to query and modify your organization.
- Define also the logins of the GitHub adminsitrators of your organization so as to prevent to change their permisssion for example.

## Prepare project

```ruby
gem install octokit
gem intall git
```

## Third-party elements

This project uses [Octokit](https://github.com/octokit/octokit.rb) Ruby client, licensed under MIT license.
It also uses [Git](https://github.com/ruby-git/ruby-git) Ruby gem, under MIT license.

## Features

### Display usage

```shell
bash GitHubWizard.sh
```

### Get all members of organization

_Keywords: #organisation #GitHub #members_

Run the following command and check the file with the FILENAME_MEMBERS name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-all-members
```

### Get members of organization with 2FA disabled

_Keywords: #organisation #GitHub #members #2FA #security_

Run the following command and check the file with the FILENAME_MEMBERS_2FA_DISABLED name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-members-2fa-disabled
```

### Get members of organization with "company" field undefined

_Keywords: #organisation #GitHub #members #company_

Run the following command and check the file with the FILENAME_MEMBERS_UNDEFINED_COMPANY name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-members-without-company
```

### Get projects which don't have any assigned team

_Keywords: #organisation #GitHub #members #teams_

Run the following command and check the file with the FILENAME_PROJECTS_WITHOUT_TEAM name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-projects-without-team
```

### Get users which have undefined or hidden email

_Keywords: #organisation #GitHub #members #email_

Run the following command and check the file with the FILENAME_USERS_WITH_BAD_EMAILS name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-users-with-bad-email
```

### Get users which may have not suitable fullname

_Keywords: #organisation #GitHub #members #fullname #name #handle_

Run the following command and check the file with the FILENAME_USERS_WITH_BAD_FULLNAMES name (_configuration.rb_)
```shell
bash GitHubWizard.sh get-users-with-bad-fullname
```

### Get repositories with undefined licenses

_Keywords: #organisation #GitHub #projects #licenses_

Run the following command and check the file with the FILENAME_PROJECTS_WITHOUT_LICENSES (_configuration.rb_)
```shell
bash GitHubWizard.sh get-projects-without-licenses
```

### Get repositories which seems to be unconform (i.e. missing files)

_Keywords: #organisation #GitHub #projects #guidelines #files_


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

_Keywords: #organisation #GitHub #projects #repository_

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

_Keywords: #organisation #GitHub #permissions #members #push_

Run the following command to update rights of all users except GitHub teams and GitHub administrators, for all projects.
Permissions will be set to "push", i.e. "write".

```shell
bash GitHubWizard.sh set-users-permissions-to-push
```

### Define teams permissions for all projects to "push"

_Keywords: #organisation #GitHub #permissions #teams #push_

Run the following command to update rights of all teams, for all projects.
Permissions will be set to "push", i.e. "write".

```shell
bash GitHubWizard.sh set-teams-permissions-to-push
```

# Play with GitHub CLI (GH)

## Prerequisites

- GitHub CLI: version 1.3.1 (2021-09-30)
- Ruby 2.7.1
- Python 3

Some configuration details must be defined (in _configuration.rb), like:
1. `GITHUB_ORGANIZATION_NAME` to store the name of the organization
2. `REPOSITORIES_CLONE_LOCATION_PATH` location of the clone sif you want to make a dump of the organisation repositories
3. `REPOSITORIES_CLONE_URL_JSON_KEY` to choose the JSON key to get the repository URL from GitHub API

## Prepare project

```shell
brew install gh
```

## Third-party elements

This project uses [GitHub CLI](https://github.com/cli/cli), licensed under MIT license.

## Features

### Make a backup of organization repositories

_Keywords: #organisation #GitHub #repositories #clones #dump_

This feature allows to clone all repositories of the defined GitHub organization and save them in a specific folder.

Run the following command:
```shell
bash GitHubWizard.sh backup-all-repositories-from-org
```

This script will trigger the _gh_ client which may ask you to athenticate to the GitHub API.
Then the Shell script will pick configuration details from the Ruby configuration file; and triggers another Shell script for the data process. A Python code will be called too. Yep, I like scripting. And both Python, Ruby and Shell.
_So imagine a python eating ruby gems in a shell. Gorgeous isn't it?_

You need to define in the _configuration.rb_ files the Github organisation at **GITHUB_ORGANIZATION_NAME**.
You have to also define the location to store clones at **REPOSITORIES_CLONE_LOCATION_PATH**

**You should also have your _git_ environment ready, i.e. add your SSH private key if you clone by SSH for example.**

### Check if there are vulnerabilities alerts in organisation repositories

_Keywords: #organisation #GitHub #repositories #Dependabot #vulnerabilities_

This feature allows to check in all repositories of the GitHub organisation if there are projects witch vulnerabilities alerts.

Run the following command:
```shell
bash GitHubWizard.sh vulnerabilities-alerts-for-all-repositories
```

This script will trigger the _gh_ client which may ask you to authenticate to the GitHub API.
Then the Shell script will pick configuration details from the Ruby configuration file; and triggers another Shell script for the data process. A Python code will be called too to process JSON sent by GitHub API.

The Python code will process JSON data, the Shell script will previously make a CURL request to to GraphQL API.

You need to define in the _configuration.rb_ files the Github organisation at **GITHUB_ORGANIZATION_NAME** and also your GitHub personal token at ** GITHUB_PERSONAL_ACCESS_TOKEN**.

**You should also have your _git_ environment ready i.e. add your SSH private key if you clone by SSH for example. _gh_ must be installed, and python3 be ready.**

### Check if there are leaks in organisation repositories (using gitleaks)

_Keywords: #organisation #GitHub #repositories #leaks #gitleaks_

**Warning: This operation can take long time because of both Git histories and file trees parsing**

This feature allows to check in all repositories of the GitHub organisation if there are leaks using the _gitleaks_ tool.

Run the following command:
```shell
bash GitHubWizard.sh look-for-leaks
```

This script will trigger the _gh_ client which may ask you to authenticate to the GitHub API.
Then the Shell script will pick configuration details from the Ruby configuration file ; and triggers another Shell script for the data process. A Python code will be called too to process JSON sent by GitHub API.

The [gitleaks](https://github.com/zricethezav/gitleaks) tool will be used to look inside the repository. To install it:

```shell
brew install gitleaks
```

You need to define in the _configuration.rb_ files the Github organisation at **GITHUB_ORGANIZATION_NAME** and also your GitHub personal token at ** GITHUB_PERSONAL_ACCESS_TOKEN**.

**You should also have your _git_ environment ready i.e. add your SSH private key if you clone by SSH for example. _gh_ must be installed, and _python3_ be ready. Obviously _gitleaks_ must be installed**

# Play with GitLab web API

## Prerequisites

- Ruby Gem: `git 1.8.1`
- Python3

- Create a [GitLab personal token](https://gitlab.com/-/profile/personal_access_tokens) and define it in the _configuration.rb_ file for the `GILAB_PERSONAL_ACCESS_TOKEN` variable.
- Define the GitLab organization id in the _configuration.rb_ file for the `GITLAB_ORGANIZATION_ID` variable. It will allow to send requests to query and modify your organization.

## Prepare project

```ruby
gem install git
```

## Features

### Make a backup of organization repositories

_Keywords: #organisation #GitLab #repositories #clones #dump_

This feature allows to clone all repositories of the defined GitLab organization (groups and subgroups incldued) and save them in a specific folder.

Run the following command:
```shell
bash GitLabWizard.sh backup-all-repositories-from-org
```

This script will get configuation details picked from the Ruby configuration file; and triggers another Shell script to make a CURL request to the GitLab endpoint. A Python code will be called so as to extract repositories URLbefoire the cloning operation.

You need to define in the _configuration.rb_ files the GitLab organisation ID at **GITLAB_ORGANIZATION_ID**.
You have to also define the location to store clones at **REPOSITORIES_CLONE_LOCATION_PATH** and the access token at **GILAB_PERSONAL_ACCESS_TOKEN**.

**You should also have your _git_ environment ready, i.e. add your SSH private key if you clone by SSH for example.**

### Check if there are leaks in organisation repositories (using gitleaks)

_Keywords: #organisation #GitLab #repositories #leaks #gitleaks_

**Warning: This operation can take long time because of both Git histories and file trees parsing**

This feature allows to check in all repositories of the GitHub organisation if there are leaks using the _gitleaks_ tool.

Run the following command:
```shell
bash GitLabWizard.sh look-for-leaks
```

This script needs a GitLab personal access otken to make requests to GitLab API and also the GitLab group ID to use to get projects under it.
The wizard Shell script will pick configuration details from the Ruby configuration file ; and triggers another Shell script for the data process. A Python code will be called too to process JSON sent by GItLab API..

The [gitleaks](https://github.com/zricethezav/gitleaks) tool will be used to look inside the repository. To install it:

```shell
brew install gitleaks
```

You need to define in the _configuration.rb_ files the GitLab organisation ID at **GITLAB_ORGANIZATION_ID**.
You have to also define the location to store clones at **REPOSITORIES_CLONE_LOCATION_PATH** and the access token at **GILAB_PERSONAL_ACCESS_TOKEN**.

**You should also have your _git_ environment ready i.e. add your SSH private key if you clone by SSH for example. _gh_ must be installed, and _python3_ be ready. Obviously _gitleaks_ must be installed**

# Licenses inventory

_Keywords: #licenses #SPM #Gradle #Maven #NPMJS #package_

## Disclaimer

*This is quite experimental feature, with results which must be verified by a human.*
*You must deal with platforms and APIs policies and fullfil them.*

*This is software is distributed on "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.*

## Prerequisites

- _Python_ version **3.7**
- _Python_ modules like _requests_, _xmltodict_ and _pytest-6.2.5_

```shell
pip install requests
pip install xmltodict
pip install pytest
```

## Fill the configuration file

Before to use the tools, the file 'config.ini' is at the root of the project, you have to personalize this file.

For example:
```text
[dependencies]
# Where to find the package manager file above
path to parse = /absolute/path/to/project_to_test
# The name of the package manager file to process store above
the filenames = go.mod
# For outputs
path to store the licenses = /absolute/path/to/project_to_test-licences
```

where:
- `path to parse` contains the dependencies manager files
- `the filenames` contains the names of the dependencies manager files to process
- `path to store the licenses` points to a folder containing the result files

## Run the tool

```shell
python3 sources/main.py
```

## Run the tests
 
To run integration tests:

```shell
 python3 -m pytest tests/integrationtests/test_search.py
```

To run unit tests:

```shell
 python3 -m pytest tests/unittests/test_config.py
 python3 -m pytest tests/unittests/test_dependency.py
 python3 -m pytest tests/unittests/test_files_check_the_directory.py
 python3 -m pytest tests/unittests/test_files_get_the_filenames_by_name.py
 python3 -m pytest tests/unittests/test_files_write_and_read.py
 python3 -m pytest tests/unittests/test_filter.py
 python3 -m pytest tests/unittests/test_parsing.py
 python3 -m pytest tests/unittests/test_parsing_download.py
```

or just

```shell
 python3 -m pytest tests/unittests/*.py
```

## Managed platforms

### Go language

`go.mod` files are managed.
Depending to the `go.mod` definitions implementation, some cases can be applied:

1. github.com will be requested if dependency starts by _github.com_
2. pkg.go.dev will be requested for other cases

For example:

```text
module ...

go 1.15

require (
	emperror.dev/errors v0.4.2                                          // <--- Request pkg.go.dev
	github.com/antihax/optional v1.0.0                                  // <--- Request github.com
	golang.org/x/tools v0.0.0-20201014231627-1610a49f37af // indirect   // <--- Not managed
	k8s.io/api v0.20.2                                                  // <--- Request pkg.go.dev
	sigs.k8s.io/controller-runtime v0.7.2                               // <--- Request pkg.go.dev
)
```

### Gradle environment

`build.gradle` and `build.gradle.kts` files are managed.
Some platforms are requests like _Maven Central_ (search.maven.org) and _GitHub_ (through api.github.com).

**Warning: unstable feature with maybe _Maven Central_ troubles.*

### Rust environment

`Cargo.lock` files are also managed.
The _crates.io_ platform will be requested for each dependency found.

### JavaScript/Node.js environment

`package.json` files can be parsed too.
The platform _npmjs.org_ wll be requested for each dependency found.

### Swift / SPM environment

If you use _Swift Package Manager_, you can parse `Package.swift` file.
The tool will extract the dependency URLs and request some forges, e.g. _github.com_.

### Dart / Flutter environment

The `pubspec.yaml` files can also be processed.
For each dependency found, the _pub.dev_ platform will be requested.

## Notes

The tool downloads a file for each dependency it found in the dependency manager file.
These files containing the licenses are in directory like 'licenses/sub_folder', where 'sub_folder' is created for each platform: Gradle, Rust, etc.

A file 'licenses.txt' is created in the folder 'licenses'. 
This file contains the list of the licenses for each dependency.
To personalize this folder, use 'config.ini'.
