[![Opened issues](https://img.shields.io/github/issues-raw/Orange-OpenSource/floss-toolbox?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/issues)
[![Apache 2.0 license](https://img.shields.io/github/license/Orange-OpenSource/floss-toolbox?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/blob/dev/LICENSE.txt)
[![Versions](https://img.shields.io/github/v/release/Orange-OpenSource/floss-toolbox?label=Last%20version&style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/releases)
[![Still maintained](https://img.shields.io/maintenance/yes/2023?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/issues?q=is%3Aissue+is%3Aclosed)

[![Code size](https://img.shields.io/github/languages/code-size/Orange-OpenSource/floss-toolbox?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox)

[![Shell](https://img.shields.io/badge/-Shell-89e051?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/search?l=shell)
[![Python](https://img.shields.io/badge/-Python-3572A5?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/search?l=python)
[![Ruby](https://img.shields.io/badge/-Ruby-701516?style=for-the-badge)](https://github.com/Orange-OpenSource/floss-toolbox/search?l=ruby)

# FLOSS Toolbox

Toolbox to help developers and open source referents to have cleaner projects in _GitHub_ organizations, and more.

Toolbox is mainly written in _Shell_ because this language is very efficient for files processing and provides a strong and rich standard API with cool primitives. It helps also to call system primitives easily. Contains also _Ruby_ scripts. _Ruby_ are shiny gems, I love them. _Python_ is also used.

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

# About features
