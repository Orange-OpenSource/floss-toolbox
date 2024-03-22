#!/usr/bin/python3
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) Orange SA
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license,
# the text of which is available at https://opensource.org/license/apache-2-0
# or see the "LICENSE.txt" file for more details.
#
# Authors: See CONTRIBUTORS.txt
# Software description: A toolbox of scripts to help work of forges admins and open source referents

# Version.............: 1.2.0
# Since...............: 12/03/2024
# Description.........: Builds a CSV file based on user inputs.

import csv
import os
import sys

from collections import defaultdict
from configuration import *

# Configuration
# -------------

# Error codes
EXIT_OK = 0
ERROR_BAD_ARGUMENTS = 1

# Methods
# -------

def check_exit(input):
    if input.lower() == "bye":
        print("👋 Ok, bye!")
        sys.exit(EXIT_OK)

def check_value(value):
    if not value:
        print("✋ Woops, value must be defined")
        return False
    if DEFAULT_PROMPT_RESULT_FILE_DELIMITER in value:
        print(f'✋ Data are exported in CSV, avoid using "{DEFAULT_PROMPT_RESULT_FILE_DELIMITER}"')
        return False
    return True

# Service
# -------

# Check arguments
if len(sys.argv) != 1:
    print("""
This script will build a third-party file listing components based on user inputs, no need of arguments.

Usage: python3 third-party-prompt.py 
""")
    sys.exit(ERROR_BAD_ARGUMENTS)

# Check if temporary file exists and ask to recover or delete it
if os.path.isfile(DEFAULT_PROMPT_RESULT_FILE):
    print("⚠️  A previous backup exists")
    input_user_answer = input("❓ Do you want to use it? (yes/NO) ")
    if input_user_answer.lower() in ["yes", "y"]:
        print("🆗 Keeping current version of save file")
        save_file = open(DEFAULT_PROMPT_RESULT_FILE, "a")
    else:
        print("🆗 Deleting previous save file")
        os.remove(DEFAULT_PROMPT_RESULT_FILE)
        print("🔨 Creating new save file")
        save_file = open(DEFAULT_PROMPT_RESULT_FILE, "a")
else:
    print("🔨 No previous backup, creating a new save file")
    save_file = open(DEFAULT_PROMPT_RESULT_FILE, "x")

# Ask to user for component details: name, copyright, license, repository hyperlink
print("🆗 Let's get the details of the components to add!")
components_added = 0
components_with_missing_licences = 0
should_continue = True
while should_continue:
    try:

        # Name of the component must be defined
        input_component_name = input("✏️  Name of the component ('bye' to exit): ")
        if not check_value(input_component_name):
            continue
        check_exit(input_component_name)

        # Repository hyperlink to get component sources must be defined
        input_component_repo = input("✏️  Repository hyperlink of the component ('bye' to exit): ")
        if not check_value(input_component_repo):
            continue
        check_exit(input_component_repo)            

        # License name for the component must be defined
        available_licenses_count = len(LICENSES)
        print("✏️  Chose which license is applied within:")
        for index, key in enumerate(LICENSES.keys()):
            print(f'\t[{index}] {key}')
        try:
            choosen_license_index = int(input("✏️  Which number (e.g. type '0' if not listed): "))
            if choosen_license_index < 0 or choosen_license_index >= available_licenses_count:
                print("❌ Index not matching a choice, try again.")
                continue
            input_component_license_name = LICENSES_NAMES[choosen_license_index]
            if choosen_license_index == 0:
                components_with_missing_licences += 1
        except ValueError:
            print("❌ Not an index for the license, try again.")
            continue
        
        # Copyright assigned to the component is optional
        input_component_copyright = input("✏️  Copyright of the component ('bye' to exit, '{escape}' if unknown): ".format(escape=DEFAULT_AVOID_FIELD_SYMBOL))
        if not check_value(input_component_copyright):
            continue
        check_exit(input_component_copyright)

        # Version of the component is optional
        input_component_version = input("✏️  Version of the component ('bye' to exit, '{escape}' if unknown): ".format(escape=DEFAULT_AVOID_FIELD_SYMBOL))
        if not check_value(input_component_version):
            continue
        check_exit(input_component_version)

        # Add the new entry in storage file
        save_file.write(input_component_name + DEFAULT_PROMPT_RESULT_FILE_DELIMITER + input_component_repo + DEFAULT_PROMPT_RESULT_FILE_DELIMITER + input_component_license_name + DEFAULT_PROMPT_RESULT_FILE_DELIMITER + input_component_copyright + DEFAULT_PROMPT_RESULT_FILE_DELIMITER + input_component_version)
        save_file.write("\n")
        components_added += 1

    except ValueError:
        print("❌ Sorry, unexpected value, try again.")
        continue
    else:
        user_continues = input("❔ Ok, got the new component. More to add? (YES/no) ")
        if not user_continues or user_continues.lower() in ["yes", "y"]: # Empty string is "false"
            print("🆗 Let's add a new component")
            continue
        else:
            save_file.close()
            should_continue = False

# Clean up
save_file.close()
print("\n")
print(f'🎉 Operation completed! Find your result file at "{DEFAULT_PROMPT_RESULT_FILE}" with {components_added} new component(s)! 🎉')
if components_with_missing_licences > 0:
    print("\n")
    print(f'❗ But beware you have {components_with_missing_licences} components without managed licenses, you shall fix the result file with suitable names and URL ❗')
    print("👉 Please refer to either https://opensource.org/licenses or https://spdx.org/licenses/ 👈")
    print("🧡 You can also submit an issue or a pull request to manage new licences: https://github.com/Orange-OpenSource/floss-toolbox/issues/new 🧡")

# Some figures
result_file = open(DEFAULT_PROMPT_RESULT_FILE, "r")
reader = csv.reader(result_file, delimiter=DEFAULT_PROMPT_RESULT_FILE_DELIMITER)
stats = defaultdict(int)

for i, line in enumerate(reader):
    license_name = line[2]
    stats[license_name] += 1

result_file.close()
flat_stats = [(license, count) for license, count in stats.items()]
sorted_stats = sorted(flat_stats, key=lambda x: x[1], reverse=True)

print("\n")
print("ℹ️  Here are some metrics about the licences: ")
for license, count in sorted_stats:
    print(f"\t {count} component(s) under license {license}")

sys.exit(EXIT_OK)