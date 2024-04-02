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

# Version.............: 1.0.0
# Since...............: 04/04/2024
# Description.........: Using reuse-tool update source files header

import argparse
import os
import sys

sys.path.append('../_')
from licenses import *

# Configuration
# -------------

# Error codes
EXIT_OK = 0
ERROR_BAD_ARGUMENTS = 1

# Other config
TEMPLATE_PATH = ".reuse/templates/"
TEMPLATE_NAME = "customTemplate"
TEMPLATE_FULL_PATH = TEMPLATE_PATH + TEMPLATE_NAME + ".jinja2"

# Check arguments
# ---------------

parser = argparse.ArgumentParser(description='This script will update the source files headers with reuse-tool')
required_args = parser.add_argument_group('Required arguments')
required_args.add_argument('-t', '--target', help='The path to the folder where scan must be done (without ending /)')
required_args.add_argument('-c', '--company', help='The name of the company owning the copyright')
required_args.add_argument('-n', '--name', help='The software name to add in template')
required_args.add_argument('-d', '--description', help='A very short description of the software')
args = parser.parse_args()

target = args.target
if not target or not os.path.isdir(target):
    print("❌ Error: the target to scan is not defined or not a directory")
    sys.exit(ERROR_BAD_ARGUMENTS) 
else:
    print(f'🆗 Target to scan and update is: "{target}"')

company = args.company
if not company:
    print("❌ Error: the name of the company is not defined")
    sys.exit(ERROR_BAD_ARGUMENTS) 
else:
    print(f'🆗 Name of the company is: "{company}"')

software_name = args.name
if not software_name:
    print("❌ Error: the name of the software is not defined")
    sys.exit(ERROR_BAD_ARGUMENTS) 
else:
    print(f'🆗 Name of the software is: "{software_name}"')   

software_description = args.description
if not software_description:
    print("❌ Error: the description of the software is not defined")
    sys.exit(ERROR_BAD_ARGUMENTS) 
else:
    print(f'🆗 Description of the software is: "{software_description}"')   

# Service
# -------

# Prepare the Jinja2 template for REUSE tool
print(f"✏️  Creating template in target: {target + TEMPLATE_PATH}")
os.makedirs(target + "/" + TEMPLATE_PATH, exist_ok=True)

available_licenses_count = len(LICENSES)
print(f"✏️  Chose which license covers the software sources to modify within these {available_licenses_count} items:")
should_continue = True
while should_continue:
    for index, key in enumerate(LICENSES.keys()):
        print(f'\t[{index}] {key}')
    try:
        choosen_license_index = int(input("✏️  Which number (choose existing license): "))
        if choosen_license_index < 1 or choosen_license_index >= available_licenses_count:
            print("❌ Index not matching a suitable choice, try again.")
            continue
        license_identifier = LICENSES_NAMES[choosen_license_index]
        license_name = LICENSES[license_identifier][0]
        license_url = LICENSES[license_identifier][1]
        should_continue = False    
    except ValueError:
        print("❌ Not an index for the license, try again.")
        continue
print(f'🆗 License to apply is "{license_name}" with reference at "{license_url}"')

# Define the Jinja2 REUSE template
print("✏️  Defining REUSE tool Jinja2 template")
with open(target + "/" + TEMPLATE_FULL_PATH, 'w+') as template_file:
    template_content="""
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
    template_content = template_content.replace("SOFTWARE_NAME", software_name)
    template_content = template_content.replace("LICENSE_NAME", license_name)
    template_content = template_content.replace("LICENSE_URL", license_url)
    template_content = template_content.replace("SOFTWARE_DESCRIPTION", software_description)
    template_file.write(template_content)
template_file.close()

# Run the tool
print("✏️  Running REUSE tool command")
reuse_tool_scan_command="""
cd {target} && reuse annotate --template="{template}" --skip-unrecognised --copyright="{copyrightOwner}" --copyright-style="spdx" --exclude-year --license="{licenseName}" --recursive ./
""".format(target=target, template=TEMPLATE_NAME, copyrightOwner=company, licenseName=license_identifier)
os.system(reuse_tool_scan_command)
# No use of "contributors" REUSE parameter because already listed in CONTRIBUTORS.txt file (supposed to be for our own case, change it if needed with '--contributor')
# No use of --year for our own needs

print(f'🆗 Formatting task is completed!')
print(f'✋ But BEWARE, you MUST check your sources diff and ensure you modified ONLY the files you ARE ALLOWED TO modify and keep external copyrights')

sys.exit(EXIT_OK)