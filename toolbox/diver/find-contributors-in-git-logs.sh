#!/bin/bash
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

# Version.............: 1.2.1
# Since...............: 11/05/2020
# Description.........: Looks for words (defined in dedicated file) in git logs
#
# Usage: bash find-contributors-in-git-logs.sh --words WORDS --project path/to/project --loglimit LIMIT
#
# Exit codes:
#       0 - normal exit
#       1 - problem with given parameters
#       2 - problem with preconditions (e.g. files to use by the script)
#       3 - problem with a command
#


VERSION="1.2.1"
SCRIPT_NAME="find-contributors-in-git-logs"

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
BAD_PARAMETERS_EXIT_CODE=2
UNEXPECTED_RESULT_EXIT_CODE=3

# Prefix for generated files
GENERATED_FILES_PREFIX="$$-contributors"

# Folder fo generated files
TEMP_FOLDER="./data"

# File listing the commits which have words hits
HITS_FILE="$TEMP_FOLDER/$GENERATED_FILES_PREFIX-commits-hits.txt"

# Report file with metrics
REPORT_METRIC_FILE="$TEMP_FOLDER/$GENERATED_FILES_PREFIX-report.txt"

# Temporary log file for "git log" command
# Assuming this file is handled in a subfolder (project to analyse) and filled by the "git log" command
GIT_LOG_TEMP_FILE="$GENERATED_FILES_PREFIX-git-log.temp.txt"

# Path to Ruby-written script which will deal fastly in few lines woith the git log file
GIT_LOG_RUBY_PARSER="./utils/find-contributors-in-git-logs.rb"

# ---------
# Functions
# ---------

# \fn DisplayUsages
# \brief Displays an help message and exists
DisplayUsages(){
    echo "*********************************************"
    echo "$SCRIPT_NAME - Version $VERSION"
    echo "*********************************************"
    echo "USAGE:"
    echo "bash $SCRIPT_NAME.sh --help"
    echo "bash $SCRIPT_NAME.sh --words WORDS --project path/to/project --loglimit LIMIT"
    echo -e "\t --words..........: Path to file containing words seperated by ; and line break"
    echo -e "\t --project........: Path to git-versioned folder of project to analyse"
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

# \fn BadParametersExit
# \brief Exits with BAD_PARAMETERS_EXIT_CODE code
BadParametersExit(){
    exit $BAD_PARAMETERS_EXIT_CODE
}

# \fn UnexpectedResultExit
# \brief Exist with UNEXPECTED_RESULT_EXIT_CODE code
UnexpectedResultExit(){
    exit $UNEXPECTED_RESULT_EXIT_CODE
}

# \fn ReadWordsFromFile
# \brief Returns words separated by ; and \n in the given file assuming it's defined and readable
# \param The path to the file to proces
ReadWordsFromFile() {
    words_file=$1
    tr ';' '\n' < $words_file
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
if [ "$#" -ne 6 ]; then
	DisplayUsages
    NormalExit
# Need some help?
elif [ "$1" = "--help" ]; then
	DisplayUsages
    NormalExit
fi

# Get words file
if [ "$1" = "--words"  ]; then
    if [ "$2" ]; then
	    words_file=$2
    else
        DisplayUsages
        BadArgumentsExit
    fi
else
    DisplayUsages
    BadArgumentsExit
fi

# Get project folder
if [ "$3" = "--project"  ]; then
    if [ "$4" ]; then
	    git_based_project=$4
    else
        DisplayUsages
        BadArgumentsExit
    fi
else
    DisplayUsages
    BadArgumentsExit
fi

# Get git log limit
if [ "$5" = "--loglimit"  ]; then
    if [ "$6" ]; then
	    git_log_limit=$6
    else
        DisplayUsages
        BadArgumentsExit
    fi
else
    DisplayUsages
    BadArgumentsExit
fi

# Test if words file and project to analyse exist and are readable
if [ ! -f "$words_file" ]; then
    echo "💥 Error: $words_file is not a file to process"
    BadArgumentsExit
fi
if [ ! -r "$words_file" ]; then
    echo "⛔ Error: $words_file file cannot be read"
    BadArgumentsExit
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

echo "*********************************************"
echo "$SCRIPT_NAME - Version $VERSION"
echo "*********************************************"

echo -e "\n"

echo "📋 File of words is $words_file"
echo "📋 Project to analyse is $git_based_project"
echo "📋 Limit for git logs is $git_log_limit"

echo "📋 Prepare logs"
PrepareFiles

echo -e "\n"

# ------------------------------------
# Step 1 - Read data file to get words
# ------------------------------------

echo "🍥 Reading words in $words_file..."

words=$( ReadWordsFromFile $words_file )
words_count=`echo $words | wc -w`

# --------------------------------------------
# Step 2 - Get git log until the defined limit
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
ruby $GIT_LOG_RUBY_PARSER $words_file "data/$GIT_LOG_TEMP_FILE" > $HITS_FILE

echo -e "\n👌 Git log has been processed with words\n"

# ------------------------------------------------------------
# Step 5 - Metrics (words and files counts, hits, duration...)
# ------------------------------------------------------------

echo "📈 Count of words to look for.......: $words_count" >> $REPORT_METRIC_FILE

commits_count=`grep -o 'commit [0-9A-Za-z]*' "data/$GIT_LOG_TEMP_FILE" | wc -l`
echo "📈 Count of commits to process......: $commits_count" >> $REPORT_METRIC_FILE

git_commit_hits_count=`cat $HITS_FILE | wc -l`
echo "📈 Count of hits....................: $git_commit_hits_count" >> $REPORT_METRIC_FILE

script_duration=$SECONDS
echo "📈 Elapsed time.....................: $(($script_duration / 60))' $(($script_duration % 60))''" >> $REPORT_METRIC_FILE

# The end!

echo "Reports available in $REPORT_METRIC_FILE:"
cat $REPORT_METRIC_FILE

echo -e "\nCommit hits are listed here: $HITS_FILE"

echo -e "\nEnd of $SCRIPT_NAME\n"
NormalExit