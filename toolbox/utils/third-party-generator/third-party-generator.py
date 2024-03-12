#!/usr/bin/python3
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2024 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Version.............: 1.0.0
# Since...............: 12/03/2024
# Description.........: Builds a third-party Markdown based on a CSV file and a delimiter

import argparse
import csv
import os
import sys

from licenses import *

# Configuration
# -------------

# Script version
VERSION = "1.0.0"

# Error codes
EXIT_OK = 0
ERROR_BAD_ARGUMENTS = 1

# Other config
RESULT_FILE_NAME = "THIRD-PARTY.md.result"

# Check arguments
# ---------------

parser = argparse.ArgumentParser(description='This script will build a third-party file listing components based on a CSV file and a delimiter')
required_args = parser.add_argument_group('Required arguments')
required_args.add_argument('-f', '--file', help='The CSV file file to process', required=True)
required_args.add_argument('-d', '--delimiter', help='The delimter symbol (e.g. ";" to split fields for each line of the CSV file', required=True)
args = parser.parse_args()

content_file_name = args.file
content_file_delimiter = args.delimiter

if not os.path.isfile(content_file_name):
    print("❌ Error: the file parameter is not a file.")
    sys.exit(ERROR_BAD_ARGUMENTS)
else:
    print(f'🆗 File to process is "{content_file_name}" with delimiter "{content_file_delimiter}"')

# Service
# -------

# Process file to build the results
print(f'🆗 Let\'s now build the {RESULT_FILE_NAME} file!')
computed_components = 0
components_with_missing_licences = 0
with open(content_file_name, 'r') as content_file:
    with open(RESULT_FILE_NAME, 'w') as result_file:
        result_file.write("""
# Third Party Softwares

This document contains the list of Third Party Softwares along with the license information.

Third Party Software may impose additional restrictions and it is the user's responsibility to ensure that they have met the licensing
requirements of the relevant license of the Third Party Software they are using.
        """)
        csv_reader = csv.reader(content_file, delimiter=content_file_delimiter)
        for component_fields in csv_reader: # Iterator on each component returning one row (i.e. component) as array of fieds
            name = component_fields[0]
            repository = component_fields[1]
            license_name = component_fields[2]
            copyright = component_fields[3]
            version = component_fields[4]
            license_url = LICENSES[license_name]
            component_entry = """
## {name}

Version {version}

Copyright {copyright}

**{name}** is distributed under the terms and conditions of the [{license} License]({url}).
You may download the source code on the [following website]({repository}).""".format(name=name, version=version, copyright=copyright, license=license_name, url=license_url, repository=repository)
            result_file.write(component_entry)
            result_file.write("\n\n")
            computed_components += 1
            if license_name == "Other":
                components_with_missing_licences += 1

# Clean up
content_file.close()
result_file.close()
print("\n")
print(f'🎉 Operation completed! Find your result file at "{RESULT_FILE_NAME}" with {computed_components} components!')
if components_with_missing_licences > 0:
    print("\n")
    print(f'❗ But beware you have {components_with_missing_licences} components without managed licenses, you shall fix they result file with suitable names and URL ❗')
    print("👉 Please refer to either https://opensource.org/licenses or https://spdx.org/licenses/ 👈")
    print("🧡 You can also submit an issue or a pull request to manage new licences: https://github.com/Orange-OpenSource/floss-toolbox/issues/new 🧡")

sys.exit(EXIT_OK)