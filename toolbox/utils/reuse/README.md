# Reuse

# Apply REUSE formatted headers in source files

## Prerequisites

- Python 3.8
- reuse

## Description

Sometimes as open source referent or developer, we want to have our source files formatted with nice headers.
Such headers should apply SPDX format and be compliant with REUSE guidelines. You can also have a look on [their nice documentation](https://reuse.readthedocs.io/en/stable/usage.html) and their [GitHub doc](https://github.com/fsfe/reuse-tool/blob/main/docs/usage.rst) too.
Thus the *update-sources-ehader.py* will apply thanks to *reuse-tool* a predefined header on sources.

**But BEWARE, you MUST check your sources diff and ensure you modified ONLY the files you ARE ALLOWED TO modify and keep external copyrights, your are repsonsible of your own code.**.

## How to use it

```shell
# Install requirements
pip install -r requirements.txt

# For help
python3.8 update-sources-header.py --help

# Short version
python3.8 update-sources-header.py -t "path/to/project/to/process" -c "Your Company" -n "Software name" -d "Very short software description"

# Long version
python3.8 update-sources-header.py --target "path/to/project/to/process" --company "Your Company" --name "Software name" --description "Very short software description"
```

## How it works

The script will create a *Jinja2* template with a predefined pattern defined within the script. It will before ask the user the license applied to the project. Then the template (in *.reuse/templates*) folder will be placed in the target destination before the run of *reuse-tool*. This *Jinja2* will then be applied to each source files using the monoline comment symbol of the dedicated programming language.

Given the template bellow:
```jinja2
Software Name: SOFTWARE_NAME
{% for copyright_line in copyright_lines %}
{{ copyright_line }}
{% endfor %}
{% for expression in spdx_expressions %}
SPDX-License-Identifier: {{ expression }}
{% endfor %}

This software is distributed under the LICENSE_NAME,
the text of which is available at LICENSE_URL
or see the "LICENSE.txt" file for more details.

Authors: See CONTRIBUTORS.txt
Software description: SOFTWARE_DESCRIPTION"""
```

And the following command line:
```shell
python3.8 update-sources-header.py --target "path/to/some/Swift/project" -c "Cyberdine Inc." -n "Genisys" -d "Just an entertainement system of course"
```

The header for Swift files will be:
```swift
// Software Name: Genisys
// SPDX-FileCopyrightText: Cyberdine Inc.
// SPDX-License-Identifier: AGPL-3.0-only
//
// This software is distributed under the GNU Affero General Public License version 3,
// the text of which is available at https://opensource.org/license/agpl-v3
// or see the "LICENSE.txt" file for more details.
//
// Authors: See CONTRIBUTORS.txt
// Software description: Just an entertainement system of course
```

**You must have a look on your sources, some files can be processed even if you don't want to.**