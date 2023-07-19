#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Version.............: 2.0.0
# Since...............: 18/07/2023
# Description.........: Counts lines of code for a target directory or Git repo URL

set -euo pipefail # set -euxo pipefail

VERSION="2.0.0"
SCRIPT_NAME=$(basename "$0")

# -------------
# Configuration
# -------------

NORMAL_EXIT_CODE=0
BAD_ARGUMENTS_EXIT_CODE=1
BAD_PRECONDITIONS_EXIT_CODE=2

# Folder fo generated files
TEMP_FOLDER="./data"

# Prefix for generated files
GENERATED_FILES_PREFIX="$$-lines-count"

# Report file with metrics
REPORT_METRIC_FILE="$TEMP_FOLDER/$GENERATED_FILES_PREFIX-report.txt"

# Name of clone repository if done
REPO_CLONE_NAME="$TEMP_FOLDER/repo-to-scan"

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
    echo "bash $SCRIPT_NAME [--folder TARGET | --url URL_OF_GIT_REPO]"
    echo -e "\t --folder.........: TARGET must point to a directory to scan for lines and count them (recursive)"
    echo -e "\t --url............: Clone repo at URL_OF_GIT_REPO and scan it"
    echo "EXIT CODES:"
    echo -e "\t$NORMAL_EXIT_CODE: normal exit"
    echo -e "\t$BAD_ARGUMENTS_EXIT_CODE: problem with given parameters"
    echo -e "\t$BAD_PRECONDITIONS_EXIT_CODE: preconditions issues"
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
    exit $BAD_PRECONDITIONS_EXIT_CODE
}

# \fn CleanFiles
# \brief If existing removes the work files
CleanFiles() {
    if [ -f "$REPORT_METRIC_FILE" ]; then
        rm "$REPORT_METRIC_FILE"
    fi
    if [ -d "$REPO_CLONE_NAME" ]; then
        rm -rf "$REPO_CLONE_NAME"
    fi
}

# \fn PrepareFiles
# \brief If existing removes the work files and then creates them
PrepareFiles() {
    CleanFiles
    touch $REPORT_METRIC_FILE
}

# ----------------
# Step 0 - Prepare
# ----------------

# Check the args numbers and display usage if needed
if [ "$#" -ne 2 ]; then
    DisplayUsages
    NormalExit
fi

# Get target
if [ "$1" = "--folder"  ]; then
    if [ "$2" ]; then
        directory_to_scan=$2
        repo_to_clone_url=""
        # Check if target is directory
        if [ ! -d "$directory_to_scan" ]; then
            echo "💥 Error: Target is not a directory ($directory_to_scan)."
            BadArgumentsExit
        fi
    else
        DisplayUsages
        BadArgumentsExit
    fi
elif [ "$1" = "--url"  ]; then
    if [ "$2" ]; then
        directory_to_scan=""
        repo_to_clone_url=$2
    else
        DisplayUsages
        BadArgumentsExit
    fi
else
    DisplayUsages
    BadArgumentsExit
fi

# Run!
SECONDS=0

echo "**************************************************"
echo "$SCRIPT_NAME - Version $VERSION"
echo "**************************************************"

echo "📋 Prepare logs"
PrepareFiles

# ---------------------------------
# Step 1 - If URL of repo, clone it
# ---------------------------------

if [ ! -z "$repo_to_clone_url" ]; then
    echo "📋 Repository to clone is '$repo_to_clone_url'"
    git clone "$repo_to_clone_url" "$REPO_CLONE_NAME"
    if [ "$(ls -A $REPO_CLONE_NAME)" ]; then
        echo "👌 Repository after cloning is not empty, good!"
        directory_to_scan="$REPO_CLONE_NAME"
    else
        echo "💥 Error: After cloning repository is empty, cannot compute metric"
        BadPreconditionsExit
    fi
else
    echo "📋 No repository to clone, check suplied folder"
fi

echo "📋 Directory to scan is $directory_to_scan"

# ------------------------------------------------
# Step 2 - Count lines of target and store results
# ------------------------------------------------

echo "🍥 Counting lines and store in $directory_to_scan"

if [ ! "$(ls -A $directory_to_scan)" ]; then
    echo "💥 Error: Directory to scan is empty, cannot compute metric"
    BadPreconditionsExit
fi

cloc "$directory_to_scan" > "$REPORT_METRIC_FILE"

echo -e "👌 Counting of lines is done\n"

# ------------------------------------------------------------
# Step 3 - Metrics (words and files counts, hits, duration...)
# ------------------------------------------------------------

script_duration=$SECONDS
echo "📈 Elapsed time.............................................: $(($script_duration / 60))' $(($script_duration % 60))''"

# The end!

echo -e "\nReport available in $REPORT_METRIC_FILE:"
cat $REPORT_METRIC_FILE

echo -e "\nEnd of $SCRIPT_NAME\n"
CleanFiles
NormalExit
