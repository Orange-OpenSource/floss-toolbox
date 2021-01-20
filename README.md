# floss-toolbox (version 1.0.0)

Toolbox to help developers and open source referents to have cleaner projects.

Tools are mainly written in _Shell_ because this language is enough efficient for files processing and provides a strong and rich standard API with cool primitives. Contains also _Ruby_ scripts.

Current features are:
* find contributors in source code
* find contributors in git logs
* find credentials in source code
* find missing signed-off fields in commits
* find creits / copyrights in source code

## Environment

You must have a _BASH_ ready environment and also _Ruby_.

## Project tree

_toolbox_ contains all the programs you need. At the root of this project are _Shell_ main scripts.
_utils_ contains the programs called from the _Shell_ main scripts.
_data_ contains some data sets and projects sampples to work on ; sensitive content maye be here.

**Please, note for this version you have to copy/paste your project in the _data_ folder because non-absolute paths and commands are used in the scripts**

## File of words

Some features parse a text file containing the words to look for in sources or _git_ logs.
Items in this file can be separated with ';' and line break.

For example the following extract defines a list of words to find like first names, last names and sensitive words.

The two following extacts produce the same outputs, write several wordss in the same line are just helpful for readers.

```
Foo;Bar;foo.bar@wizz.com
Alice;NoOne;alice.noone@where.com
Bod;Tinkerer;bob.the-tinkerer@company.com
password
login
```

```
Foo
Bar
foo.bar@wizz.com
Alice
NoOne
alice.noone@where.com
Bod
Tinkerer
bob.the-tinkerer@company.com
password
login
```

## Features

### Find contributors in files

The tooblox can look in each file of a project for words.
Such words may be developers' first names, last names, email addresses or whatever you want.
A report is created with a curated list of found words in precise files.

To run the feature:
```shell
bash find-contributor-in-files.sh --target path/to/project
```

This script uses another _Shell_ script in _utils_ folder (_find-hotwords-files.sh_) and expect to have a defined and readable file in _data_ folder (named _contributors-entries.txt_). Thus only the project to scan can be given in parameter of the script, and the file of contributors to look for can be versionned or statically defined.

Note this version provides a naive implementation for file processing which should be improved to reduce the computation time.
In fact this implementation is based on a three-levels-based loop: each line of each file is checked for each word.
Not so efficient, but it works and is suitable for a first release.

### Find contributors in git log

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

We assume the source code to analyse is not hosted on a git-based project, that is the reason why such tools like _git grep_ are not used.
This feature will look in the files for some keywords like passwords or logins.

To run the feature:
```shell
bash find-credentials-in-files.sh --project path/to/project
```

This script uses another _Shell_ script in _utils_ folder (_find-hotwords-files.sh_) and expect to have a defined and readable file in _data_ folder (named _contributors-entries.txt_). Thus only the project to scan can be given in parameter of the script, and the file of credentials to look for can be versionned or statically defined.

Note this version provides a naive implementation for file processing which should be improved to reduce the computation time.
In fact this implementation is based on a three-levels-based loop: each line of each file is checked for each word.
Not so efficient, but it works and is suitable for a first release.

Exemple of file listing credentials-relayed words:
```
login
password
pwd
key
ssh
credential
authentication
host
account
mail
access
port
pass
```

### Find missing signed-off fields

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

We can also check in sources if some hotwords are used, mainly about credits or copyrights notices.
For example, "credit", "created by" or "(C)" can refer to third-party components we missed to list.

To run the feature:
```shell
bash find-credits-in-files.sh --target path/to/project
```

This script uses another _Shell_ script in _utils_ folder (_find-hotwords-files.sh_) and expect to have a defined and readable file in _data_ folder (named _notices-entries.txt_). Thus only the project to scan can be given in parameter of the script, and the file of contributors to look for can be versionned or statically defined.

Note this version provides a naive implementation for file processing which should be improved to reduce the computation time.
In fact this implementation is based on a three-levels-based loop: each line of each file is checked for each word.
Not so efficient, but it works and is suitable for a first release.

Exemple of file listing hotwords for credits
```
copyright;(C);©
author;authors
credit
created
```
