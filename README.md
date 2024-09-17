[![Opened issues](https://img.shields.io/github/issues-raw/Orange-OpenSource/floss-toolbox?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/issues)
[![Apache 2.0 license](https://img.shields.io/github/license/Orange-OpenSource/floss-toolbox?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/blob/dev/LICENSE.txt)
[![Versions](https://img.shields.io/github/v/release/Orange-OpenSource/floss-toolbox?label=Last%20version&style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/releases)
[![Still maintained](https://img.shields.io/maintenance/yes/2024?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/issues?q=is%3Aissue+is%3Aclosed)
[![Code size](https://img.shields.io/github/languages/code-size/Orange-OpenSource/floss-toolbox?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox)

[![Shell](https://img.shields.io/badge/-Shell-89e051?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/search?l=shell)
[![Python](https://img.shields.io/badge/-Python-3572A5?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/search?l=python)
[![Ruby](https://img.shields.io/badge/-Ruby-701516?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/search?l=ruby)
[![PHP](https://img.shields.io/badge/-PHP-4F5B93?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/search?l=php)

# FLOSS Toolbox

Toolbox to help developers and open source referents to have cleaner projects in _GitHub_ organizations, and more.

Toolbox is mainly written in _Shell_ because this language is very efficient for files processing and provides a strong and rich standard API with cool primitives and nice performances due to system calls. It helps also to call system primitives easily.
Contains also _Ruby_ scripts. _Ruby_ are shiny gems, I love them.
_Python_ is also used. 
And a bit of _PHP_ because it is nice to use several languages we are not used to (stop the routine!).
For these needs scripting is enough.

## Environment

You should have mainly the following environments bellow, but have a look on each folder README:
- _Bash_ version **3.2.5**
- _Ruby_ version **2.7.1**
- _Python_ version **3.7**

## Project tree

There are 5 folders containing scripts and programs to make your life a bit easier:

1. _toolbox/diver_ contains scripts to scrap data in Git logs and histories, look for sensitive data in sources, etc ;
2. _toolbox/github_ contains scripts and programs to make requests to GitHub API so as to automate some actions ;
3. _toolbox/gitlab_ contains scripts and programs to make requests to GitLab API so as to automate some actions ;
4. _toolbox/LicensesInventory_ contains program to get licenses of third party components thanks to dependency manager files ;
5. _toolbox/utils_ contains scripts to generate texts and stuff like that.

Feel free to read each README available in all of the subdirectories listed above.

## Dry run

To be sure you have a ready-to-run project, you can run the following dry-run command which will check if runtimes, third party tools and files are available.

```shell
bash dry-run.sh
```

## About the repository

### Renovate

[Renovate](https://docs.renovatebot.com/) is used to as to try to keep updated dependencies of the project.
A _renovate.json_ must be added at the project root with cofiguration details ; but **the organization admins must enable it** (through the [admin console](https://developer.mend.io/)).
By default [Dependabot](https://docs.github.com/fr/code-security/supply-chain-security/understanding-your-software-supply-chain/about-supply-chain-security#what-is-dependabot) was enabled for this project but has been replaced by _Renovate_.

### Gitleaks

[Gitleaks](https://github.com/gitleaks/gitleaks) is used so as to look for secrets and leak of sensitive data.
A _gitleaks.toml_ file has been placed at the project root, picked from the _Gitleaks_ repository, to define rules.
A *gitleaks-action.yml* is also defined to define the GitHub Action to call and some secrets to use to do so.
The *GITLEAKS_LICENSE* is defined in the organization level, **only the organization admins can make it visible to projects**.
This key (dedicated to organization) has been asked to the *Gitleaks* team and received gratefully from them.

### DCO

The *Developer Certificate of Origin* is applied here thanks to a [Probot bot](https://probot.github.io/apps/dco/).
On pull requests all commits must be signed off. This control is processed in an action.
