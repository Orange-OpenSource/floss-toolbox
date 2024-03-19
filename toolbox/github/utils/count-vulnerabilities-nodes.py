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
# Since...............: 25/02/2022
# Description.........: In the given JSON file, produced by GitHub GraphQL API request file, count and return the number of vulnerabilities nodes
#
# Usage: python3 count-vulnerabilities-nodes.py --file file_name
#

import argparse
import json
import sys

# Check arguments
# ---------------

parser = argparse.ArgumentParser(description='In the given JSON file, produced by GitHub GraphQL API request file; count and return the number of vulnerabilities nodes.')
required_args = parser.add_argument_group('Required arguments')
required_args.add_argument('-f', '--file', help='The JSON file to process', required=True)
args = parser.parse_args()

file_name = args.file

# Extraction
# ----------

with open(file_name, 'r', encoding='utf-8') as f:
    entries = json.load(f)
    f.close()

vulnerabilitiy_nodes = entries["data"]["repository"]["vulnerabilityAlerts"]["nodes"]
vulnerabilitiy_nodes_count=len(vulnerabilitiy_nodes)

print(vulnerabilitiy_nodes_count)
sys.exit(0)