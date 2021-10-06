#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2021 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Version.............: 1.0.0
# Since...............: 06/10/2021
# Description.........: Using the Git history, provide a list of contributors
#
# Usage: bash list-contributors-in-history.sh --project path/to/project --loglimit LIMIT
#
# Exit codes:
#       0 - normal exit
#       1 - problem with given parameters
#       2 - problem with preconditions (e.g. files to use by the script)
#       3 - problem with a command
#

set -euo pipefail
# Exits immediately if:
# - any command has non-zero exit status (-e)
# - undefined variable in use (-u)
# and do not mask errors in pipelines (-o pipefail)

VERSION="1.0.0"
SCRIPT_NAME="list-contributors-in-history"

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
# \brief Exist with UNEXPECTED_RESULT_EXIT_CODE code
UnexpectedResultExit(){
    exit $UNEXPECTED_RESULT_EXIT_CODE
}

# \fn PrepareFiles
# \brief If existing removes the work files and then creates them
PrepareFiles() {
    if [ -f $HITS_FILE ]; then
        rm $HITS_FILE
    fi
    touch $HITS_FILE
    if [ -f $REPORT_METRIC_FILE ]; then
        rm $REPORT_METRIC_FILE
    fi
    touch $REPORT_METRIC_FILE
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

git_log_file="../$GIT_LOG_TEMP_FILE"
if [ -f $git_log_file ]; then
    rm $git_log_file
fi
touch $git_log_file

git log --since=$git_log_limit > $git_log_file

if [ ! -s "$git_log_file" ]; then
    cd "$current_folder"
    echo "💥 Error: $git_log_file is empty, the git log command seems to have failed. Check the 'loglimit' parameter."
    UnexpectedResultExit
fi

cd "$current_folder"

# -------------------------
# Step 3 - Process the logs
# -------------------------

echo -e "🍥 Running Ruby script (named $GIT_LOG_RUBY_PARSER) to look in log file for contributors...\n"

# Ruby tool is in toolbox/diver/utils
# Git log file is in toolbox/diver/data
ruby $GIT_LOG_RUBY_PARSER "./data/$GIT_LOG_TEMP_FILE" > $HITS_FILE

echo -e "\n👌 Git log has been processed\n"

# ------------------------------------------------------------
# Step 5 - Metrics (words and files counts, hits, duration...)
# ------------------------------------------------------------

commits_count=`grep -o 'commit [0-9A-Za-z]*' "data/$GIT_LOG_TEMP_FILE" | wc -l`
echo "📈 Count of commits to process..............................: $commits_count" >> $REPORT_METRIC_FILE

contributors_count=`cat "$HITS_FILE" | wc -l`
echo "📈 Count of contributors to process.........................: $contributors_count" >> $REPORT_METRIC_FILE

script_duration=$SECONDS
echo "📈 Elapsed time.............................................: $(($script_duration / 60))' $(($script_duration % 60))''" >> $REPORT_METRIC_FILE

# The end!

echo "Reports available in $REPORT_METRIC_FILE:"
cat $REPORT_METRIC_FILE

echo -e "\nEnd of $SCRIPT_NAME\n"
NormalExit