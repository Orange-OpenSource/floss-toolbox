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

# Version.............: 1.0.0
# Since...............: 11/05/2020
# Description.........: Looks for credentials in a project's files
#
# Usage: bash find-credentials-in-files.sh --project path/to/project
#
# Exit codes:
#       0 - normal exit
#       1 - problem with given parameters
#       2 - problem with preconditions (e.g. files to use by the script)
#

VERSION="1.0.0"
SCRIPT_NAME="find-credentials-in-files"

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

# Script which will make the computations
FIND_SCRIPT="./utils/find-hotwords-in-files.sh"

# File listing words like contributors names, emails, commpanies... seperated by ; and line breaks
CREDENTIALS_FILE="./data/credentials-entries.txt"

# ---------
# Functions
# ---------

# \fn DisplayUsages
# \brief Displays an help message and exists
DisplayUsages(){
    echo "******************************************"
    echo "$SCRIPT_NAME - Version $VERSION"
    echo "******************************************"
    echo "USAGE:"
    echo "bash $SCRIPT_NAME.sh --target PROJECT"
    echo -e "\t - This command will run the program to look for credentials in files ($FIND_SCRIPT) using words defined in file '$CREDENTIALS_FILE'"
    echo -e "\t - PROJECT must point to a directory whith the files to analyse"
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

# ----------------
# Step 0 - Prepare
# ----------------

# Check the args numbers and display usage if needed
if [ "$#" -ne 2 ]; then
    DisplayUsages
    NormalExit
fi

# Get target folder
if [ "$1" = "--target"  ]; then
    if [ "$2" ]; then
	    project_folder=$2
    else
        DisplayUsages
        BadArgumentsExit
    fi
else
    DisplayUsages
    BadArgumentsExit
fi

echo "******************************************"
echo "$SCRIPT_NAME - Version $VERSION"
echo "******************************************"

# Test if words file, find script and project to analyse exist and are readable
if [ ! -f "$CREDENTIALS_FILE" ]; then
    echo "💥 Error: $SCRIPT_NAME - $CREDENTIALS_FILE is not a file to process"
    BadPreconditionsExit
fi

if [ ! -r "$CREDENTIALS_FILE" ]; then
    echo "⛔ Error: $SCRIPT_NAME - $CREDENTIALS_FILE file cannot be read"
    BadPreconditionsExit
fi

if [ ! -f "$FIND_SCRIPT" ]; then
    echo "💥 Error: $SCRIPT_NAME - $FIND_SCRIPT is not a script to trigger"
    BadPreconditionsExit
fi

if [ ! -r "$FIND_SCRIPT" ]; then
    echo "⛔ Error: $SCRIPT_NAME - $FIND_SCRIPT script cannot be read"
    BadPreconditionsExit
fi

# -------------------------
# Step 1 - Start the script
# -------------------------

./$FIND_SCRIPT --words "$CREDENTIALS_FILE" --directory "$project_folder"

# The end!

echo -e "\nEnd of $SCRIPT_NAME\n"
NormalExit
