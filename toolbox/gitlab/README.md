# GitLab

Table of Contents
=================		
   * [Play with GitLab web API](#play-with-gitlab-web-api)
      * [Prerequisites](#prerequisites-2)
      * [Prepare projects](#prepare-project-2)									
      * [Features](#features-3)			
         * [Make a backup of organization repositories](#make-a-backup-of-organization-repositories-1)			
         * [Check if there are leaks in organisation repositories (using gitleaks)](#check-if-there-are-leaks-in-organisation-repositories-using-gitleaks-1)			

# Play with GitLab web API

## Prerequisites

- [Python 3](https://www.python.org/)
- [Git](https://git-scm.com/) (version 2.32.0)
- [curl](https://github.com/curl/curl)
- [gitleaks](https://github.com/gitleaks/gitleaks)

- Create a [GitLab personal token](https://gitlab.com/-/profile/personal_access_tokens) and define it in the _configuration.rb_ file for the `GILAB_PERSONAL_ACCESS_TOKEN` variable.
- Define the GitLab organization id in the _configuration.rb_ file for the `GITLAB_ORGANIZATION_ID` variable. It will allow to send requests to query and modify your organization.

This project expects to have several third-party elements available and already added in your system, like _Python3_, _git_, _curl_ and _gitleaks_.
None of them have been modified nor distributed.
Thus there is no composition nor [aggregation (mere or not)](https://www.gnu.org/licenses/gpl-faq.html#MereAggregation) with them but these components are also called by the system calls mainly.

To check preconditions, run:

```shell
bash dry-run.sh
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