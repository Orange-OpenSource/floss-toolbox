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
         * [Count lines of code in a directory](#count-lines-of-code-in-a-directory)
         * [Check if sources have headers](#check-if-sources-have-headers)

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
# To compute metrics in some folder
bash lines-count.sh --folder "absolute/path/to/target"

# To compute metrics for a remote repository to clone at given URL
bash lines-count.sh --url "HTTP-or-SSH-URL-of-Git-repository"
```

### Check if headers exist in sources using templates

_Keywords: #headers #sources #SPDX_

It is possible to run a scan in a project to check wether or not the source files contain (in fact start by) some header text.
For example it is a good practice or mandatory to have headers in sources files with legal mentions, and sometimes some headers can be missing.
The *check-sources-headers.rb* script will take a raw text file (without useless new lines or whitespaces), and generate some templates using comments symbols. If will look for source files in the project, and check if files start by the decorated version of the text, i.e. the template.

```shell
# Run the script to scan the given folder and using the given raw text template
ruby check-sources-headers.rb --folder data/project --template data/template.txt

# Or also display more debug traces
ruby check-sources-headers.rb --folder data/project --template data/template.txt --debug

# Or keep the previous generated templates (i.e. decorated raw header files)
ruby check-sources-headers.rb --folder data/project --template data/template.txt --keep

# Or exclude from scans a directory (e.g. generated files, docs, etc)
ruby check-sources-headers.rb --folder data/project --template data/template.txt --exclude data/project/directory/to/exclude

# Or use all these parameters!
ruby check-sources-headers.rb --folder data/ods-ios --template data/template-ods_ios.txt --debug --keep --exclude data/project/directory/to/exclude
```

The *check_source_headers.rb* script will generate as much templates as managed programming languages rules.
For example, if there are rules about CSS, it will create a template for the specific rules for CSS. But if there are several rules for CSS, the template will be overriden each time.
The generated template is named using the basic file name, e.g. if you give to the script a "template.txt" file, for CSS the script will build a "template.txt.CSS" file. For Swift, it will be "template.txt.SWIFT" (always extension uppercased).
Thus, supposing some previous file with that name exist, the script will ask you if you want to keep it or not.
You may want to get rid of it because it was for a previous run. But you may want to keep it because you saw some rules for a specific programming language are not really fulfilled (specially with whitespaces), so you would like to use your own custom template file.

**In a nutshell, if it failed the first time, use your custom template file (--keep) instead of using rules with comment symbols defined in the script.**

For example, for a template file name *template-ods_ios.txt* with the content bellow:
```text
Software Name: Orange Design System
SPDX-FileCopyrightText: Copyright (c) Orange SA
SPDX-License-Identifier: MIT

This software is distributed under the MIT license,
the text of which is available at https://opensource.org/license/MIT/
or see the "LICENSE" file for more details.

Authors: See CONTRIBUTORS.txt
Software description: A SwiftUI components library with code examples for Orange Design System
```

And in the Ruby script the following rule for Ruby programming language:
```ruby
check_for_sources($arguments[:folder], $arguments[:template], $arguments[:exclude], conform_files, not_conform_files, ".rb",  "#", "# ", "#")
```

The Ruby template checked at the beginning of files is:

```text
#
# Software Name: Orange Design System
# SPDX-FileCopyrightText: Copyright (c) Orange SA
# SPDX-License-Identifier: MIT
#
# This software is distributed under the MIT license,
# the text of which is available at https://opensource.org/license/MIT/
# or see the "LICENSE" file for more details.
#
# Authors: See CONTRIBUTORS.txt
# Software description: A SwiftUI components library with code examples for Orange Design System
#
```

But with the following rule without special symbols to open and close the header, the tempalte will be a bit different:

```ruby
check_for_sources($arguments[:folder], $arguments[:template], $arguments[:exclude], conform_files, not_conform_files, ".rb",  "", "# ", "")
```

```text
# Software Name: Orange Design System
# SPDX-FileCopyrightText: Copyright (c) Orange SA
# SPDX-License-Identifier: MIT
# 
# This software is distributed under the MIT license,
# the text of which is available at https://opensource.org/license/MIT/
# or see the "LICENSE" file for more details.
# 
# Authors: See CONTRIBUTORS.txt
# Software description: A SwiftUI components library with code examples for Orange Design System
```

This case is more interesting if you use the same symbol for first, last and intermediate lines (or if you use only monoline comment symbol).

### Generate a CONTRIBUTORS file

We may want to have a CONTRIBUTORS.txt or AUTHORS.txt files containing all the people names who worked or still work on the project.
To do so, we can use the VCS history as a source of truh ; e.g. Git as SCM.
The *generate-contributors-file.py* Python script will use Git commands to get logs, and build a CONTRIBUTORS file in the project with some notice
and the list of all entities (first name, uppercased lastname, email).
However, the user will have to deal namesakes and only might want to remove some bots accounts.

To run it:

```shell
python3.8 generate-contributors-file.py --target /path/to/myt/git/based/project
```

For example it will output a file with such content:

```text
# This is the official list of people have contributed code to 
# this repository.
#
# Names should be added to this file like so:
#     Individual's name <submission email address>
#     Individual's name <submission email address> <email2> <emailN>
#
# An entry with multiple email addresses specifies that the
# first address should be used in the submit logs and
# that the other addresses should be recognized as the
# same person.

# Please keep the list sorted.

renovate[bot] <29139666+renovate[bot]@users.noreply.github.com> 
BarryAllen <barry.allen@star.labs> 
Lex LUTHOR <100863844+lluthor@users.noreply.github.com>
Bruce WAYNE <batman@gmail.com>
Bruce WAYNE <bruce.waybe@wayneenterprise.com>
```

In the example above, we can see that the Renovate bot commit has been processed (maybe a line to remove), *BarryAllen* failed to configure his Git environment (because he types to fast on his keyboard we can suppose), the commit from GitHub Web UI of *Lex Luthor* has been picked and *Bruce WAYNE* used two addresses.

Maybe a better file after fixes could be:

```text
# This is the official list of people have contributed code to 
# this repository.
#
# Names should be added to this file like so:
#     Individual's name <submission email address>
#     Individual's name <submission email address> <email2> <emailN>
#
# An entry with multiple email addresses specifies that the
# first address should be used in the submit logs and
# that the other addresses should be recognized as the
# same person.

# Please keep the list sorted.
Barry ALLEN <barry.allen@star.labs> 
Lex LUTHOR <lex.luthor@lex.corp>
Bruce WAYNE <bruce.waybe@wayneenterprise.com> <batman@gmail.com>
```