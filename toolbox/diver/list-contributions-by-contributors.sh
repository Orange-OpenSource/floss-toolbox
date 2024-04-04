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
# Since...............: 04/04/2024
# Description.........: Using the Git history, provide a list of contributors' contributions
#
# Usage: bash list-contributors-in-history-emails-from-history.sh --project path/to/project
#
# Exit codes:
#       0 - normal exit
#       1 - problem with given parameters
#       2 - problem with preconditions (e.g. files to use by the script)
#

#set -euxo pipefail

VERSION="1.0.0"
SCRIPT_NAME=$(basename "$0")

# -------------
# Configuration
# -------------

NORMAL_EXIT_CODE=0
BAD_ARGUMENTS_EXIT_CODE=1
BAD_PRECONDITION_EXIT_CODE=2

# Folder fo generated files
TEMP_FOLDER=".floss-toolbox/data"

# Prefix for generated files
GENERATED_FILES_PREFIX="$$-contributions-of"

# ---------
# Functions
# --------

# \fn DisplayUsages
# \brief Displays an help message and exists
DisplayUsages(){
    echo "*****************************************************"
    echo "$SCRIPT_NAME - Version $VERSION"
    echo "*****************************************************"
    echo "USAGE:"
    echo "bash $SCRIPT_NAME --project PROJECT"
    echo -e "\t --project........: PROJECT must point to a git-based directory whith the commits to scan"
}

# ----------------
# Step 0 - Prepare
# ----------------

# Check the args numbers and display usage if needed
if [ "$#" -ne 2 ]; then
    DisplayUsages
    exit $NORMAL_EXIT_CODE
fi

# Get target folder
if [ "$1" = "--project"  ]; then
    if [ "$2" ]; then
	    git_based_project=$2
    else
        DisplayUsages
        exit $BAD_ARGUMENTS_EXIT_CODE
    fi
else
    DisplayUsages
    exit $BAD_ARGUMENTS_EXIT_CODE
fi

# Run!

echo "*****************************************************"
echo "$SCRIPT_NAME - Version $VERSION"
echo "*****************************************************"

echo "📋 Project to analyse is $git_based_project"
echo "📋 Prepare workspace"

# Prepare workspace

current_folder=`pwd`
workspace="$current_folder/$TEMP_FOLDER"

if [ -d "$workspace" ]; then
    yes | rm -rf "$workspace"
fi
mkdir -p "$workspace"

cd "$git_based_project"

# Check if Git repository is not empty

echo "🍥 Checking git project state..."

if [ "$( git log --oneline -5 2>/dev/null | wc -l )" -eq 0 ]; then
    echo "Warning: Project '$git_based_project' is a git repository without any commit, that's weird"
    exit $BAD_PRECONDITION_EXIT_CODE
fi

# Get all authors

echo "🍥 Retrieving git authors..."
git_authors=$(git log --format='%ae' | sort -u)

for git_author in $git_authors; do
   git log --author="$git_author" --pretty=format:"[DATE] %ad [HASH] %h [TITLE] %s" --date=short > "$workspace/$GENERATED_FILES_PREFIX-$git_author.txt"
done

# Finished!

echo "👌 Done!"

cd "$current_folder"
number_files=$(ls -l "$workspace" | grep "^-" | wc -l | tr -d '[:space:]')
echo "📈 There are $number_files generated, i.e. maybe $number_files authors with contributions"
echo "Find results in '$workspace' folder"

echo "Do you want to list all the files? (YES/no)"
read -r response
response=$(echo "$response" | tr '[:upper:]' '[:lower:]')

if [ -z $response ] || [ "$response" = "yes" ] || [ "$response" = "y" ]; then
    ls -l "$workspace" | awk '{print $9}'
    echo -e "\n"
fi

echo "Bye!"
exit $NORMAL_EXIT_CODE