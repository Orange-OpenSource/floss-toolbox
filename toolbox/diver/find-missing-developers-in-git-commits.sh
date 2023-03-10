#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Version.............: 1.1.1
# Since...............: 12/05/2020
# Description.........: Looks in git commits in the DCO has been used, i.e. if commits have been signed off.
# Checks also if commits authors are defined.
#
# Usage: bash find-missing-developers-in-git-commits.sh --project path/to/project --loglimit LIMIT
#
# Exit codes:
#       0 - normal exit
#       1 - problem with given parameters
#       2 - problem with preconditions (e.g. files to use by the script)
#       3 - problem with a command
#

VERSION="1.1.1"
SCRIPT_NAME="find-missing-developers-in-git-commits"

# -------------
# Configuration
# -------------

# Exits immediately if:
# - any command has non-zero exit status (-e)
# - undefined variable in use (-u)
# and do not mask errors in pipelines (-o pipefail)
set -euo pipefail

NORMAL_EXIT_CODE=0
BAD_ARGUMENTS_EXIT_CODE=1
BAD_PRECONDITION_EXIT_CODE=2
UNEXPECTED_RESULT_EXIT_CODE=3

# Folder fo generated files
TEMP_FOLDER="./data"

# Prefix for generated files
GENERATED_FILES_PREFIX="$$-missing-developers"

# File listing the commits which have words hits
HITS_FILE="$TEMP_FOLDER/$GENERATED_FILES_PREFIX-commits-hits.txt"

# Report file with metrics
REPORT_METRIC_FILE="$TEMP_FOLDER/$GENERATED_FILES_PREFIX-report.txt"

# Temporary log file for "git log" command
# Assuming this file is handled in a subfolder (project to analyse) and filled by the "git log" command
GIT_LOG_TEMP_FILE="$GENERATED_FILES_PREFIX-git-log.temp.txt"

# Path to Ruby-written script which will deal fastly in few lines with the git commits messages file
GIT_LOG_RUBY_PARSER="./utils/find-missing-developers-in-git-commits.rb"

# ---------
# Functions
# ---------

# \fn DisplayUsages
# \brief Displays an help message and exits
DisplayUsages(){
    echo "***********************************************"
    echo "$SCRIPT_NAME - Version $VERSION"
    echo "***********************************************"
    echo "USAGE:"
    echo "bash $SCRIPT_NAME.sh --project PROJECT --loglimit LIMIT"
    echo -e "\t --project........: PROJECT must point to a git-based directory whith the csommits to analyse"
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

if [ "$( git log --oneline -5 2>/dev/null | wc -l )" -eq 0 ]; then
    echo "Warning: Project '$git_based_project' is a git repository without any commit, that's weird"
    NormalExit
fi

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

echo -e "🍥 Running Ruby script to look in log file for words named $GIT_LOG_RUBY_PARSER...\n"

# Ruby tool is in toolbox/utils
# Git log file is in toolbox/data
ruby $GIT_LOG_RUBY_PARSER "data/$GIT_LOG_TEMP_FILE" > $HITS_FILE

echo -e "\n👌 Git log has been processed with words\n"

# ------------------------------------------------------------
# Step 5 - Metrics (words and files counts, hits, duration...)
# ------------------------------------------------------------

commits_count=`grep -o 'commit [0-9A-Za-z]*' "data/$GIT_LOG_TEMP_FILE" | wc -l`
echo "📈 Count of commits to process..............................: $commits_count" >> $REPORT_METRIC_FILE

git_commit_total_hits_count=`cat $HITS_FILE | wc -l`
echo "📈 Total count of hits......................................: $git_commit_total_hits_count" >> $REPORT_METRIC_FILE

# FIXME: I like cats by 4 cats are too much

# If we have hits for signed-off cases, grep and count
if [[ `cat $HITS_FILE` == *"signed-off"* ]]; then                            # "signed-off" written by the Ruby script in output for each hit
    git_commit_dco_hits_count=`cat $HITS_FILE | grep signed-off | wc -l`
else
    git_commit_dco_hits_count=0
fi
echo "📈 Count of hits for missing/undefined signed-off...........: $git_commit_dco_hits_count" >> $REPORT_METRIC_FILE

# If we have hits for authors, grep and count
if [[ `cat $HITS_FILE` == *"author"* ]]; then                            # "author" written by the Ruby script in output for each hit
    git_commit_author_hits_count=`cat $HITS_FILE | grep author | wc -l`
else
    git_commit_author_hits_count=0
fi
echo "📈 Count of hits for missing/undefined author...............: $git_commit_author_hits_count" >> $REPORT_METRIC_FILE

script_duration=$SECONDS
echo "📈 Elapsed time.............................................: $(($script_duration / 60))' $(($script_duration % 60))''" >> $REPORT_METRIC_FILE

# The end!

echo "Reports available in $REPORT_METRIC_FILE:"
cat $REPORT_METRIC_FILE

echo -e "\nCommit hits are listed here: $HITS_FILE"

echo -e "\nEnd of $SCRIPT_NAME\n"
NormalExit