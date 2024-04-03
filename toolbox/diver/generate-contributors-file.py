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
# Since...............: 03/04/2023
# Description.........: Using the Git history, generates a CONTRIBUTORS.md file

import argparse
import os
import shutil
import sys
import time

# Configuration
# -------------

NORMAL_EXIT_CODE = 0
BAD_ARGUMENTS_EXIT_CODE = 1
BAD_PRECONDITION_EXIT_CODE = 2
UNEXPECTED_RESULT_EXIT_CODE=  3

# Check arguments
# ---------------

parser = argparse.ArgumentParser(description='Using the Git history, generates a CONTRIBUTORS.md file')
required_args = parser.add_argument_group('Required arguments')
required_args.add_argument('-t', '--target', help='The path to the folder (Git based project) where scan must be done')
args = parser.parse_args()

target = args.target
if not target or not os.path.isdir(target):
    print("❌ Error: the target to scan is not defined or not a directory")
    sys.exit(BAD_ARGUMENTS_EXIT_CODE) 
else:
    print(f'🆗 Target to scan and update is: "{target}"')

# Service
# -------

start_computation_time = time.time()

# Temporary log file for "git log" command
TEMP_FOLDER = ".floss-toolbox-temp"
TEMP_FOLDER_FULL_PATH = target + "/" + TEMP_FOLDER
GIT_LOG_TEMP_FILE = "git-logs.txt"
GIT_LOG_TEMP_FILE_PATH = TEMP_FOLDER_FULL_PATH + "/" + GIT_LOG_TEMP_FILE
print(f"✏️  Creating folder '{TEMP_FOLDER}' with internal stuff in target")
os.makedirs(TEMP_FOLDER_FULL_PATH, exist_ok=True)

# Check if Git repository is empty (check if there are at least 1 commit in the logs)
command_result = os.system("git log --oneline -1 > /dev/null 2>&1 | wc -l")
if command_result == "0":
    printf("💥 Error: Target is a git repository without any commit, that's weird")
    sys.exit(BAD_PRECONDITION_EXIT_CODE)
else:
    print("🆗 It seems there are commits in this repository, cool!")

# Dump Git logs
print("✏️  Dumping Git logs")
# Create the log file, go to targetn and run the git command
# Format the output to have first name, last name (upercased) and email, sorted alphabetically ascending
# Deal also the case where we only have one value between first and last name
git_log_command = """
touch {log_file} && cd {target} && git log --all --format="%aN <%aE>" | sort | uniq | awk '{{if ($2 !~ /@/) {{print $1, toupper($2), $3}} else {{print $1, $2, $3}}}}' | sort -k2 > {log_file}
""".format(target=target, log_file=GIT_LOG_TEMP_FILE_PATH)
os.system(git_log_command)

# Add notice in file
final_file_name = "CONTRIBUTORS.new.txt"
final_file_path = target + "/" + final_file_name # .new just to prevent to override previous existing file
print(f"✏️  Preparing final file at '{final_file_path}'")
with open(GIT_LOG_TEMP_FILE_PATH, 'r') as logs_file:
    contributors = logs_file.read()

notice = """# This is the official list of people have contributed code to 
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

"""
final_content = notice + contributors

with open(final_file_path, 'w') as contributors_file:
    contributors_file.write(final_content)

print("🧹  Cleaning")
shutil.rmtree(TEMP_FOLDER_FULL_PATH)

end_computation_time = time.time()

print(f"🎉  The contributors file '{final_file_name}' has been generated (in {end_computation_time - start_computation_time} seconds)!")
print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print(f'✋ You MUST have a look on it, deal namesakes and ensure the file is well filled')
print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
sys.exit(NORMAL_EXIT_CODE)