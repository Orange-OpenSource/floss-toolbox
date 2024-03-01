[![Opened issues](https://img.shields.io/github/issues-raw/Orange-OpenSource/floss-toolbox?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/issues)
[![Apache 2.0 license](https://img.shields.io/github/license/Orange-OpenSource/floss-toolbox?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/blob/dev/LICENSE.txt)
[![Versions](https://img.shields.io/github/v/release/Orange-OpenSource/floss-toolbox?label=Last%20version&style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/releases)
[![Still maintained](https://img.shields.io/maintenance/yes/2023?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/issues?q=is%3Aissue+is%3Aclosed)
[![Code size](https://img.shields.io/github/languages/code-size/Orange-OpenSource/floss-toolbox?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox)

[![Shell](https://img.shields.io/badge/-Shell-89e051?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/search?l=shell)
[![Python](https://img.shields.io/badge/-Python-3572A5?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/search?l=python)
[![Ruby](https://img.shields.io/badge/-Ruby-701516?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/search?l=ruby)
[![PHP](https://img.shields.io/badge/-PHP-4F5B93?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/search?l=php)

# FLOSS Toolbox

Toolbox to help developers and open source referents to have cleaner projects in _GitHub_ organizations, and more.

Toolbox is mainly written in _Shell_ because this language is very efficient for files processing and provides a strong and rich standard API with cool primitives and nice performanes due to system calls. It helps also to call system primitives easily.
Contains also _Ruby_ scripts. _Ruby_ are shiny gems, I love them.
_Python_ is also used. 
And a bit of _PHP_ because it is nice to use severa alnguages we are not used to.
For these needs scripting is enough.

# Environment

You should have mainly the following environments:
- _Bash_ version **3.2.5**
- _Ruby_ version **2.7.1**
- _Python_ version **3.7**

# Project tree

There are 5 folders containing scripts and programs to make your life a bit easier:

1. _toolbox/diver_ contains scripts to scrap data in Git logs and histories, look for sensitive data in sources, etc ;
2. _toolbox/github_ contains scripts and programs to make requests to GitHub API so as to automate some actions ;
3. _toolbox/gitlab_ contains scripts and programs to make requests to GitLab API so as to automate some actions ;
4. _toolbox/LicensesInventory_ contains program to get licenses of third party components thanks to dependency manager files ;
5. _toolbox/utils_ contains scripts to generate texts and stuff like that.

Feel free to read each README available in all of the subdirectories listed above.

# Dry run

To be sure you have a ready-to-run project, you can run the following dry-run command which will check if runtimes, third party tools and files are available.

```shell
bash dry-run.sh
```