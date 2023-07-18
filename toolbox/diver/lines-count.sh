#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Version.............: 1.0.0
# Since...............: 18/07/2023
# Description.........: Counts liens of cound for a target directory
#
# Usage: bash lines-count.sh --target TARGET
#
# Exit codes:
#       0 - normal exit
#       1 - problem with given parameters
#

set -euo pipefail # set -euxo pipefail

VERSION="1.0.0"
SCRIPT_NAME="lines-count.sh"

# -------------
# Configuration
# -------------

NORMAL_EXIT_CODE=0
BAD_ARGUMENTS_EXIT_CODE=1

# Folder fo generated files
TEMP_FOLDER="./data"

# Prefix for generated files
GENERATED_FILES_PREFIX="$$-lines-count"

# Report file with metrics
REPORT_METRIC_FILE="$TEMP_FOLDER/$GENERATED_FILES_PREFIX-report.txt"

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
    echo "bash $SCRIPT_NAME --target TARGET"
    echo -e "\t --target.........: TARGET must point to a directory to scan for lines and count them (recursive)"
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

# \fn CleanFiles
# \brief If existing removes the work files
CleanFiles() {
    if [ -f $REPORT_METRIC_FILE ]; then
        rm $REPORT_METRIC_FILE
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
if [ "$1" = "--target"  ]; then
    if [ "$2" ]; then
	    directory_to_scan=$2
    else
        DisplayUsages
        BadArgumentsExit
    fi
else
    DisplayUsages
    BadArgumentsExit
fi

# Check if target is directory
if [ ! -d "$directory_to_scan" ]; then
    echo "💥 Error: Target is not a directory ($directory_to_scan)."
    BadArgumentsExit
fi

# Run!
SECONDS=0

echo "**************************************************"
echo "$SCRIPT_NAME - Version $VERSION"
echo "**************************************************"

echo -e "\n"

echo "📋 Directory to scan is to analyse is $directory_to_scan"
echo "📋 Prepare logs"
PrepareFiles

echo -e "\n"

# ------------------------------------------------
# Step 1 - Count lines of target and store results
# ------------------------------------------------

echo "🍥 Counting lines and store in $directory_to_scan"

cloc "$directory_to_scan" > "$REPORT_METRIC_FILE"

echo -e "👌 Counting of lines is done\n"

# ------------------------------------------------------------
# Step 2 - Metrics (words and files counts, hits, duration...)
# ------------------------------------------------------------

script_duration=$SECONDS
echo "📈 Elapsed time.............................................: $(($script_duration / 60))' $(($script_duration % 60))''"

# The end!

echo -e "\nReport available in $REPORT_METRIC_FILE:"
cat $REPORT_METRIC_FILE

echo -e "\nEnd of $SCRIPT_NAME\n"
CleanFiles
NormalExit
