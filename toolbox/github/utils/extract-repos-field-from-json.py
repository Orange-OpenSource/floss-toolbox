#!/usr/bin/python3
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Version.............: 1.0.0
# Since...............: 21/01/2022
# Description.........: Extract all values for the given field name in the JSON file.
#
# Usage: python3 extract-repos-field-from-json.py --field field_name --source json_file
#

import argparse
import json

# Check arguments
# ---------------

parser = argparse.ArgumentParser(description='Extract and writes in standard output specific fields from a jSON dump of repositories.')
required_args = parser.add_argument_group('Required arguments')
required_args.add_argument('-f', '--field', help='The name of the JSON property to extract', required=True)
required_args.add_argument('-s', '--source', help='The name of the JSON file to parse', required=True)
args = parser.parse_args()

field_name = args.field
file_name = args.source

# Extraction
# ----------

with open(file_name, 'r', encoding='utf-8') as f:
    repositories = json.load(f)
    f.close()

for repository in repositories:
    print(repository[field_name])