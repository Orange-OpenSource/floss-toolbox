# Utils

# Generate text from template

## Prerequisites

- PHP

## Install prerequisites

```shell
brew install php
```

## Description

Sometimes as open source reference or software forges administrator, we need so send emails to people.
These emails can be big with lot of detials and hyperlinks to resources, and writing them is time expansive.
Becaise these emails are almost the same (except with some details), we can generate them using a template and variables.

```shell
php text-generator.php "_templates/new-GitHub-repository-contributors.fr.template.txt" "_templates/values.ini"
```

Here we give to the `text-generator.php` PHP script a template to process (first argument) and also an .ini file containing values (second argument). The script will check if all variables are filled, then will replace each entry in the text by the values.

For example, if we have such .ini file:

```text
[some_section_which_is_ignored]
; Some comment
VARIABLE_NAME = "Foo-Bar"
```

the script will replace all occurences of **%VARIABLE_NAME%** by "Foo-Bar" in the text. Then a file with the new version will be created with quite the same name but _.result_ at the end.