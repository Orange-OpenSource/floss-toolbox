# GitHub

Table of Contents
=================
   * [Play with GitHub web API](#play-with-github-web-api)
      * [Project tree](#project-tree)
      * [Prerequisites](#prerequisites)
      * [Prepare project](#prepare-project)
      * [Features](#features)
         * [Display usages](#display-usage)
         * [Get all members of organization](#get-all-members-of-organization)
         * [Get members of organization with 2FA disabled](#get-members-of-organization-with-2fa-disabled)
         * [Get members of organization with "company" field undefined](#get-members-of-organization-with-company-field-undefined)
         * [Get projects which don't have any assigned team](#get-projects-which-dont-have-any-assigned-team)
         * [Get users which have undefined or hidden email](#get-users-which-have-undefined-or-hidden-email)
         * [Get users which may have not suitable fullname](#get-users-which-maye-have-not-suitable-fullname)
         * [Get repositories with undefined licenses](#get-repositories-with-undefined-licenses)
         * [Get repositories which seems to be unconform (i.e. missing files)](#get-repositories-which-seems-to-be-unconform-ie-missing-files)
         * [Get repositories which seems to be empty or have not enough files](#get-repositories-which-seems-to-be-empty-or-have-not-enough-files)
         * [Define users permissions for all projects to "push"](#define-users-permissions-for-all-projects-to-push)
         * [Define teams permissions for all projects to "push"](#define-teams-permissions-for-all-projects-to-push)
         * [Make a year review of the GitHub organization](#make-a-year-review-of-the-github-organization)
   * [Play with GitHub CLI (GH)](#play-with-github-cli-gh)
      * [Prerequisites](#prerequisites-1)
      * [Prepare project](#prepare-project-1)
      * [Features](#features-2)
         * [Make a backup of organization repositories](#make-a-backup-of-organization-repositories)
         * [Check if there are vulnerabilities alerts in organisation repositories](#check-if-there-are-vulnerabilities-alerts-in-organisation-repositories)
         * [Check if there are leaks in organisation repositories (using gitleaks)](#check-if-there-are-leaks-in-organisation-repositories-using-gitleaks)	

# Play with GitHub web API

## Project tree

1. _github_ contains all scripts and programs to play with GitHub API using Octokit or GH
2. _github/licenses_ contains third-party licenses files
3. _github/utils_ contains utility scripts calls by the wizard

## Prerequisites

- Ruby Gem: `octokit 6.1.1`
- Ruby Gem: `git 1.18.0`
- Ruby 2.7.1

- Create a [GitHub personal token](https://github.com/settings/tokens) and define it in the _configuration.rb_ file for the `GITHUB_PERSONAL_ACCESS_TOKEN` variable.
- Define the _GitHub_ organization name in the _configuration.rb_ file for the `GITHUB_ORGANIZATION_NAME` variable. It will allow to send requests to query and modify your organization.
- Define also the logins of the GitHub adminsitrators of your organization so as to prevent to change their permisssion for example.

This project expects to have several third-party elements available and already added in your system, like [Octokit Ruby gem](https://github.com/octokit/octokit.rb), [Git](https://git-scm.com/), [Ruby](https://www.ruby-lang.org), [Bash](https://www.gnu.org/software/bash/) and [Git Ruby gem](https://github.com/ruby-git/ruby-git)
None of them have been modified nor distributed.

Thus there is no composition nor [aggregation (mere or not)](https://www.gnu.org/licenses/gpl-faq.html#MereAggregation) with them but these components are also called by the system calls mainly, except for _Octokit_ and _Git_ Ruby gems under MIT licenses.

To check preconditions, run:

```shell
bash dry-run.sh
```

## Prepare project

```shell
gem install octokit
gem install git
```

of if you have _Bundler_:

```shell
bundle install
```

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

### Define teams permissions for all projects to "read"

_Keywords: #organisation #GitHub #permissions #teams #read_

Run the following command to update rights of all teams, for all projects.
Permissions will be set to "read".

```shell
bash GitHubWizard.sh set-teams-permissions-to-read
```

### Make a year review of the GitHub organization

_Keywords: #organisation #GitHub #KPI #year #review_

You will need to define a *.env* file with the GitHub API token for key *GITHUB_API_TOKEN*, the organization name and some settings.
Here the organization name is *Orange-OpenSource*, replace with your own and add the suitable token.

See for example:
```text
GITHUB_API_TOKEN=your-token
ORGANIZATION_NAME=Orange-OpenSource
TOP_N_PROG_LANG=5
TOP_N_LEAST_PROG_LANG=5
TOP_N_LICENSES=5
TOP_N_CONTRIBUTORS_OVERALL=10
TOP_N_CONTRIBUTORS_FOR_YEAR=10
TOP_N_REPOS_MOST_COMMITS=5
```

Run the following command to compute a year review of the organization

```shell
# Do not forget to install dependencies
pip install -r requirements.txt

# For year 2024
python3.8 github-year-review.py --year 2024

# For year 20°24 and commits counts computing (can be time expansive)
python3.8 github-year-review.py --year 2024 --count-commits
```

# Play with GitHub CLI (GH)

## Prerequisites

- GitHub CLI: version 1.3.1 (2021-09-30)
- Ruby 2.7.1
- Python 3

Some configuration details must be defined (in _configuration.rb_), like:
1. `GITHUB_ORGANIZATION_NAME` to store the name of the organization
2. `REPOSITORIES_CLONE_LOCATION_PATH` location of the clone sif you want to make a dump of the organisation repositories
3. `REPOSITORIES_CLONE_URL_JSON_KEY` to choose the JSON key to get the repository URL from GitHub API

This project expects to have several third-party elements available and already added in your system, like [[Ruby](https://www.ruby-lang.org), [Python 3](https://www.python.org/) and [GitHub CLI](https://github.com/cli/cli)
None of them have been modified nor distributed.

Thus there is no composition nor [aggregation (mere or not)](https://www.gnu.org/licenses/gpl-faq.html#MereAggregation) with them but these components are also called by the system calls mainly.

To check preconditions, run:

```shell
bash dry-run.sh
```

## Prepare project

```shell
brew install gh
```

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

You need to define in the _configuration.rb_ files the Github organisation at **GITHUB_ORGANIZATION_NAME** and also your GitHub personal token at **GITHUB_PERSONAL_ACCESS_TOKEN**.

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

You need to define in the _configuration.rb_ files the Github organisation at **GITHUB_ORGANIZATION_NAME** and also your GitHub personal token at **GITHUB_PERSONAL_ACCESS_TOKEN**.

**You should also have your _git_ environment ready i.e. add your SSH private key if you clone by SSH for example. _gh_ must be installed, and _python3_ be ready. Obviously _gitleaks_ must be installed**
