# Diver

Table of Contents
=================
   * [The diver of source code and commits](#the-diver-of-source-code-and-commits)
      * [Project tree](#project-tree)
      * [Prerequisites](#prerequisites)
      * [Input file](#file-of-words)
      * [Features](#features)
         * [Find contributors in files](#find-contributors-in-files)
         * [Find contributors in Git log](#find-contributors-in-git-log)
         * [Find credentials in sources](#find-credentials-in-sources)
         * [Find missing signed-off fields](#find-credentials-in-sources)
         * [Find credits](#find-credits)
         * [List conributors from Git history](#list-contributors-from-git-history)
         * [Extract email adress from Git history](#extract-email-address-from-git-history)

# The "diver" of source code and commits

## Project tree

1. _diver_ contains several scripts you need. At the root of this folder are _Shell_ main scripts.
2. _diver/utils_ contains the programs called from the _Shell_ main scripts.
3. _diver/data_ contains some datasets and projects samples to work on.

**Please, note for this version for some features you might have to copy/paste your project in the _toolbox/diver/data_ folder because non-absolute paths and commands are used in the scripts**

## Prerequisites

Some components must be available (dry-run script will help to find the ones missing):
- [Bash](https://www.gnu.org/software/bash/) (version 3.2.5)
- [Ruby](https://www.ruby-lang.org) (version 2.7.1)
- [Git](https://git-scm.com/) (version 2.32.0)
- [Cloc](https://github.com/AlDanial/cloc) (version 1.88)

This project expects to have these third party elements available and already added in your system.
Thus there is no composition nor [aggregation (mere or not)](https://www.gnu.org/licenses/gpl-faq.html#MereAggregation) with them but these components are also called by the system calls mainly.
None of them have been modified nor distributed.

To check preconditions, run:

```shell
bash dry-run.sh
```

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

### Count lines of code in a directory

_Keywords: #cloc #metrics #KPI #APP_

You can use one script to compute lines of code thanks to [cloc](https://github.com/AlDanial/cloc) program.
It will generate a report with all the metrics you may need.

```shell
bash lines-count.sh --target "absolute/path/to/target"
```