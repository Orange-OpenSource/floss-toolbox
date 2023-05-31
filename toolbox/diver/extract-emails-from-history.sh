#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Version.............: 1.0.2
# Since...............: 06/10/2021
# Description.........: Using the Git history, provide a list of contributors
#
# Usage: bash extract-emails-from-history.sh --project path/to/project --loglimit LIMIT
#
# Exit codes:
#       0 - normal exit
#       1 - problem with given parameters
#       2 - problem with preconditions (e.g. files to use by the script)
#       3 - problem with a command
#

set -euo pipefail

VERSION="1.0.2"
SCRIPT_NAME="extract-emails-from-history"

# -------------
# Configuration
# -------------

NORMAL_EXIT_CODE=0
BAD_ARGUMENTS_EXIT_CODE=1
BAD_PRECONDITION_EXIT_CODE=2
UNEXPECTED_RESULT_EXIT_CODE=3

# Folder fo generated files
TEMP_FOLDER="./data"

# Prefix for generated files
GENERATED_FILES_PREFIX="$$-list-of-contributors"

# File listing the commits which have words hits
HITS_FILE="$TEMP_FOLDER/$GENERATED_FILES_PREFIX-commits-hits.txt"

# Report file with metrics
REPORT_METRIC_FILE="$TEMP_FOLDER/$GENERATED_FILES_PREFIX-report.txt"

# Temporary log file for "git log" command
# Assuming this file is handled in a subfolder (project to analyse) and filled by the "git log" command
GIT_LOG_TEMP_FILE="$GENERATED_FILES_PREFIX-git-log.temp.txt"

# Path to Ruby-written script which will deal fastly in few lines with the git commits messages file
GIT_LOG_RUBY_PARSER="./utils/extract-contributors-lists.rb"

# Files to store the extracted email addresses
EXTRACTED_EMAILS_FILE="$TEMP_FOLDER/$$-extracted-emails.txt"
EXTRACTED_EMAILS_FILE_TEMP="$TEMP_FOLDER/$$-extracted-emails.temp.txt"

# ---------
# Functions
# ---------

# \fn DisplayUsages
# \brief Displays an help message and exists
DisplayUsages(){
    echo "***********************************************"
    echo "$SCRIPT_NAME - Version $VERSION"
    echo "***********************************************"
    echo "USAGE:"
    echo "bash $SCRIPT_NAME.sh --project PROJECT --loglimit LIMIT"
    echo -e "\t --project........: PROJECT must point to a git-based directory whith the commits to analyse, placee it in _data_ folder"
    echo -e "\t --loglimit.......: [git log] option to define the LIMIT for commit searches, e.g. 2.weeks or 3.years"
}

# \fn NormalExit
# \brief Exits with NORMAL_EXIT_CODE code
NormalExit(){
    exit $NORMAL_EXIT_CODE
}

# \fn BadArgumentsExit
# \brief Exits with BAD_ARGUMENTS_EXIT_CODE code
BadArgumentsExit(){
    exit $BAD_ARGUMENTS_EXIT_CODE
}

# \fn BadPreconditionsExit
# \brief Exits with BAD_PRECONDITION_EXIT_CODE code
BadPreconditionsExit() {
    exit $BAD_PRECONDITION_EXIT_CODE
}

# \fn UnexpectedResultExit
# \brief Exist with UNEXPECTED_RESULT_EXIT_CODE code after removal of work files
UnexpectedResultExit(){
    CleanFiles
    exit $UNEXPECTED_RESULT_EXIT_CODE
}

# \fn CleanFiles
# \brief If existing removes the work files
CleanFiles() {
    if [ -f $HITS_FILE ]; then
        rm $HITS_FILE
    fi
    if [ -f $REPORT_METRIC_FILE ]; then
        rm $REPORT_METRIC_FILE
    fi
    if [ -f $GIT_LOG_TEMP_FILE ]; then
        rm $GIT_LOG_TEMP_FILE
    fi
    if [ -f $EXTRACTED_EMAILS_FILE_TEMP ]; then
        rm $EXTRACTED_EMAILS_FILE_TEMP
    fi
}

# \fn PrepareFiles
# \brief If existing removes the work files and then creates them
PrepareFiles() {
    CleanFiles
    touch $HITS_FILE
    touch $REPORT_METRIC_FILE
    touch $EXTRACTED_EMAILS_FILE
    touch $EXTRACTED_EMAILS_FILE_TEMP
}

# ----------------
# Step 0 - Prepare
# ----------------

# Check the args numbers and display usage if needed
if [ "$#" -ne 4 ]; then
    DisplayUsages
    NormalExit
fi

# Get target folder
if [ "$1" = "--project"  ]; then
    if [ "$2" ]; then
	    git_based_project=$2
    else
        DisplayUsages
        BadArgumentsExit
    fi
else
    DisplayUsages
    BadArgumentsExit
fi

# Get git limit
if [ "$3" = "--loglimit"  ]; then
    if [ "$4" ]; then
	    git_log_limit=$4
    else
        DisplayUsages
        BadArgumentsExit
    fi
else
    DisplayUsages
    BadArgumentsExit
fi

# Test if find script and project to analyse exist and are readable

if [ ! -f "$GIT_LOG_RUBY_PARSER" ]; then
    echo "💥 Error: $SCRIPT_NAME - $GIT_LOG_RUBY_PARSER is not a script to trigger"
    BadPreconditionsExit
fi

if [ ! -r "$GIT_LOG_RUBY_PARSER" ]; then
    echo "⛔ Error: $SCRIPT_NAME - $GIT_LOG_RUBY_PARSER script cannot be read"
    BadPreconditionsExit
fi

if [ ! -d "$git_based_project" ]; then
    echo "💥 Error: $git_based_project is not a directory to process"
    BadArgumentsExit
fi
if [ ! -r "$git_based_project" ]; then
    echo "⛔ Error: $git_based_project file cannot be read"
    BadArgumentsExit
fi

# Run!
SECONDS=0

echo "**************************************************"
echo "$SCRIPT_NAME - Version $VERSION"
echo "**************************************************"

echo -e "\n"

echo "📋 Project to analyse is $git_based_project"
echo "📋 Limit for git logs is $git_log_limit"

echo "📋 Prepare logs"
PrepareFiles

echo -e "\n"

# --------------------------------------------
# Step 1 - Get git log until the defined limit
# --------------------------------------------

echo "🍥 Retrieving git logs in temporary file named $GIT_LOG_TEMP_FILE..."

current_folder=`pwd`

cd "$git_based_project"

git_log_file="$current_folder/data/$GIT_LOG_TEMP_FILE"
if [ -f "$git_log_file" ]; then
    rm $git_log_file
fi

touch "$git_log_file"

if [ "$( git log --oneline -5 2>/dev/null | wc -l )" -eq 0 ]; then
    echo "Warning: Project '$git_based_project' is a git repository without any commit, that's weird"
    CleanFiles
    NormalExit
fi

git log --since=$git_log_limit > "$git_log_file"

if [ ! -s "$git_log_file" ]; then
    cd "$current_folder"
    echo "💥 Error: $git_log_file is empty, the git log command seems to have failed. Check the 'loglimit' parameter."
    UnexpectedResultExit
fi

cd "$current_folder"

# -------------------------
# Step 2 - Process the logs
# -------------------------

echo -e "🍥 Running Ruby script (named $GIT_LOG_RUBY_PARSER) to look in log file for contributors...\n"

# Ruby tool is in toolbox/diver/utils
# Git log file is in toolbox/diver/data
ruby $GIT_LOG_RUBY_PARSER "data/$GIT_LOG_TEMP_FILE" > $HITS_FILE

echo -e "👌 Git log has been processed\n"

# ----------------------
# Step 3 - Extract email
# ----------------------

# We suppose contributors picked from Git history are written like:
# jane doe <jane.doe@foo.bar>
# So we extract and keep text between the <>

echo -e "Extract emails from file '$HITS_FILE' and store them in '$EXTRACTED_EMAILS_FILE'\n"
while IFS= read -r line
do
  email=`echo "$line" | sed -e 's/.*\<\(.*\)\>/\1/'`
  echo "$email" >> "$EXTRACTED_EMAILS_FILE_TEMP"
done < "$HITS_FILE"
sort -t@ -k2 "$EXTRACTED_EMAILS_FILE_TEMP" | sort -u > "$EXTRACTED_EMAILS_FILE"

# ------------------------------------------------------------
# Step 4 - Metrics (words and files counts, hits, duration...)
# ------------------------------------------------------------

commits_count=`grep -o 'commit [0-9A-Za-z]*' "data/$GIT_LOG_TEMP_FILE" | wc -l`
echo "📈 Count of commits to process..............................: $commits_count" >> $REPORT_METRIC_FILE

contributors_count=`cat "$HITS_FILE" | wc -l`
echo "📈 Count of contributors to process.........................: $contributors_count" >> $REPORT_METRIC_FILE

script_duration=$SECONDS
echo "📈 Elapsed time.............................................: $(($script_duration / 60))' $(($script_duration % 60))''" >> $REPORT_METRIC_FILE


# The end!

rm "$git_log_file"
echo -e "\nReports available in $REPORT_METRIC_FILE:"
cat $REPORT_METRIC_FILE

echo -e "\nEnd of $SCRIPT_NAME\n"
CleanFiles
NormalExit