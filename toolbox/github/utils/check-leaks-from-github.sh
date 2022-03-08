#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2021-2022 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Since...............: 07/03/2022
# Description.........: Received from arguments a GitHub organisation name, a cloning key and a target folder to dump repositories and check if there are leaks thanks to gitleaks

#set -euxo pipefail
VERSION="1.0.0"

# Config
# ------

EXIT_OK=0
EXIT_BAD_ARGUMENTS=1
EXIT_BAD_SETUP=2

URL_EXTRACTER_FILE="./utils/extract-repos-field-from-json.py"
LEAKS_PARSER="./utils/count-leaks-nodes.py"
GITLEAKS_FINAL_REPORT="$$_gitleaks-final_report-count.csv"

# Functions
# ---------

UsageAndExit(){
    echo "check-leaks-from-github.sh - Version $VERSION"
	echo "USAGE:"
	echo "bash check-leaks-from-github.sh ORGANISATION KEY TOKEN FOLDER_NAME"
    echo "with ORGANISATION: GitHub organisation name"
    echo "with KEY: JSON key to use for cloning URL"
    echo "with FOLDER_NAME: name of folder where repositories will be cloned"
    echo "About exit codes:"
	echo -e "\t 0................: Normal exit"
	echo -e "\t 1................: Bad arguments given to the script"
    echo -e "\t 2................: Bad setup for the script or undefined LEAKS_PARSER file"
	exit $EXIT_OK
}

# Check setup
# -----------

if [ "$#" -eq 0 ]; then
    UsageAndExit
    exit $EXIT_OK
fi

if [ "$#" -ne 3 ]; then
    echo "ERROR: Bad arguments number. Exits now"
    UsageAndExit
    exit $EXIT_BAD_ARGUMENTS
fi

if [ ! -f "$URL_EXTRACTER_FILE" ]; then
    echo "ERROR: Bad set up for URL extracter. Exits now"
    UsageAndExit
    exit $EXIT_BAD_SETUP
fi

if [ ! -f "$LEAKS_PARSER" ]; then
    echo "ERROR: Bad set up for leaks parser. Exits now"
    UsageAndExit
    exit $EXIT_BAD_SETUP
fi

organisation_name=$1
if [ -z "$organisation_name" -o "$organisation_name" == "" ]; then
	echo "ERROR: No organisation name defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

cloning_url_key=$2
if [ -z "$cloning_url_key" -o "$organisation_name" == "" ]; then
	echo "ERROR: No JSON key for URL. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

dump_folder_name=$3
if [ -z "$dump_folder_name" -o "$organisation_name" == "" ]; then
	echo "ERROR: No dump folder name defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

# Run
# ---

echo "---------------------------------------------"
echo "check-leaks-from-github.sh - Version $VERSION"
echo "---------------------------------------------"

# Step 1 - Authenticate to GitHub using gh

echo "Authenticating to GitHub using gh client..."
gh auth login
echo "Authentication done."

# Step 2 - Get repositories URL

echo "Get repositories URL..."
repositories_list_raw_temp_file=".repos-raw.json"
repositories_list_clean_temp_file=".repos-clean.json"
gh api -X GET "orgs/$organisation_name/repos" -F per_page=500 --paginate > $repositories_list_raw_temp_file 
cat $repositories_list_raw_temp_file | sed -e "s/\]\[/,/g" > $repositories_list_clean_temp_file # Need to replace '][' by ',' because of pagination
rm -f $repositories_list_raw_temp_file
echo "All repositories URL got."

# Step 3 - Extract cloning URL

url_for_cloning=".url-for-cloning.txt"
echo "Extract cloning from results (using '$cloning_url_key' as JSON key)..."
python3 "$URL_EXTRACTER_FILE" --field $cloning_url_key --source $repositories_list_clean_temp_file > $url_for_cloning
rm -f $repositories_list_clean_temp_file
echo "Extraction done."

# Step 4 - Create workspace directory

dir_before_dump=`pwd`
echo "Creating workspace directory..."
if [ -d "$dump_folder_name" ]; then
    echo "Removing old directory"
    rm -rf "$dump_folder_name"
fi
mkdir "$dump_folder_name"
directory_name=$(date '+%Y-%m-%d')
mkdir "$dump_folder_name/$directory_name"
cd "$dump_folder_name/$directory_name"
echo "Dump directory created with name '$dump_folder_name/$directory_name' at location `pwd`"

# Step 5 - For each repository, clone it and look for leaks

echo "status;project name;count of leaks" > $GITLEAKS_FINAL_REPORT

number_of_url=`cat "$dir_before_dump/$url_for_cloning" | wc | awk {'print $1 '}`
echo "WARNING: This operation can take a long time, because repositories must be cloned and gitleaks will analyze both files and git histories!"
echo "Dumping of $number_of_url repositories..."

# gitleaks may also throw following errors:
# "ERR warning: inexact rename detection was skipped due to too many files."
# "WRN warning: you may want to set your diff.renameLimit variable to at least 535 and retry the command."
# TODO: Refactor this point
previous_git_diff_rename_limit=$(git config --global diff.renameLimit) || true
echo "Previous value for git configuration key diff.renameLimit: '$previous_git_diff_rename_limit'"
git config --global diff.renameLimit 999999
echo "New value for git configuration key diff.renameLimit: '$(git config --global diff.renameLimit)'"

cpt=1
cpt_clean_repo=0
cpt_dirty_repo=0

while read url_line; do

    # Step 5.1 - Clone
    # WARNING: gitleaks looks inside files and git histories, so for old and big projects it will take too many time!

    echo "Cloning ($cpt / $number_of_url) '$url_line'..."
    git clone "$url_line"

    # Step 5.2 - Extract new folder name
    target_folder_name=`basename -s .git $(echo "$url_line")`
    echo "Cloned in folder '$target_folder_name'"

    # Step 5.3 - Look for leaks

    gitleaks_file_name="$target_folder_name".gitleaks.json
    gitleaks detect --report-format json --report-path "$gitleaks_file_name" --source "$target_folder_name" || true # gitleaks returns 1 if leaks found

    # In JSON report, a project as no leak if the result file containsan empty JSON array, i.e. only the line
    # []
    if [ -f "$gitleaks_file_name" ]; then
        count=`python3 "../../$LEAKS_PARSER" --file "$gitleaks_file_name"`

        if [ "$count" -eq "0" ]; then
            echo "✅ ;$target_folder_name;$count" >> $GITLEAKS_FINAL_REPORT
            echo "✅ Gitleaks did not find leaks for '$target_folder_name'"
            cpt_clean_repo=$((cpt_clean_repo+1))
        else
            echo "🚨;$target_folder_name;$count" >> $GITLEAKS_FINAL_REPORT
            echo "🚨 WARNING! gitleaks may have found '$count' leaks for '$target_folder_name'"
            cpt_dirty_repo=$((cpt_dirty_repo+1))
        fi
    else
        echo "💥 ERROR: The file '$gitleaks_file_name' does not exist, something has failed with gitleaks!"
    fi

    cpt=$((cpt+1))

    rm -rf "$target_folder_name"
    
done < "$dir_before_dump/$url_for_cloning"

echo "Looking done!"

# Step 6 - Clean up

git config --global diff.renameLimit $previous_git_diff_rename_limit # (default seems to be 0)

mv $GITLEAKS_FINAL_REPORT "$dir_before_dump"
echo "GitHub organisation name.............: '$organisation_name'"
echo "Total number of projects.............: '$number_of_url'"
echo "Number of projects with alerts.......: '$cpt_dirty_repo'"
echo "Number of projects without alerts....: '$cpt_clean_repo'"
echo "Final report is......................: '$GITLEAKS_FINAL_REPORT'"

rm -rf "$target_folder_name"
rm -rf "$dir_before_dump/$url_for_cloning"
cd "$dir_before_dump"
rm -f $url_for_cloning

echo "Check done!"
