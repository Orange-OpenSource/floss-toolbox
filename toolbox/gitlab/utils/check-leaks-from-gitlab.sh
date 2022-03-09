#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2021-2022 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Since...............: 09/03/2022
# Description.........: Check if there are leaks thanks to gitleaks in GitLab projects

#set -euxo pipefail
VERSION="1.0.0"

# Config
# ------

EXIT_OK=0
EXIT_BAD_ARGUMENTS=1
EXIT_BAD_SETUP=2

URL_EXTRACTER_FILE="./../github/utils/extract-repos-field-from-json.py" # TODO: Extract this Python sript to common files
LEAKS_PARSER="./../github/utils/count-leaks-nodes.py"                   # TODO: Extract this Python sript to common files
GITLEAKS_FINAL_REPORT="$$_gitleaks-final_report-count.csv"

# Functions
# ---------

UsageAndExit(){
    echo "check-leaks-from-gitlab.sh - Version $VERSION"
	echo "USAGE:"
	echo "bash check-leaks-from-gitlab.sh ORGANISATION_ID KEY TOKEN FOLDER_NAME PAGINATION TOKEN"
    echo "with ORGANISATION_ID: GitLab organisation ID"
    echo "with KEY: JSON key to use for cloning URL"
    echo "with PAGINATION: number if items per page"
    echo "with TOKEN: GitLab access token"
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

if [ "$#" -ne 4 ]; then
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

organisation_id=$1
if [ -z "$organisation_id" -o "$organisation_id" == "" ]; then
	echo "ERROR: No organisation ID defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

cloning_url_key=$2
if [ -z "$cloning_url_key" -o "$cloning_url_key" == "" ]; then
	echo "ERROR: No JSON key for URL. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

pagination=$3
if [ -z "$pagination" ]; then
	echo "ERROR: No pagination defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

access_token=$4
if [ -z "$access_token" ]; then
	echo "ERROR: No access token is defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

# Run
# ---

echo "---------------------------------------------"
echo "check-leaks-from-gitlab.sh - Version $VERSION"
echo "---------------------------------------------"

# Step 1 - Get all groups and subgroups projects

max_number_of_pages=10 # TODO: Remove magic number for max number of pages
echo "Get all projects of groups and subgroups with $pagination items per page and arbitrary $max_number_of_pages pages max..."

gitlab_projects_dump_file_raw="./data/.gitlab-projects-dump.raw.json"
gitlab_projects_dump_file_clean="./data/.gitlab-projects-dump.clean.json"
if [ -f "$gitlab_projects_dump_file_raw" ]; then
    rm $gitlab_projects_dump_file_raw
fi

for page in `seq 1 $max_number_of_pages`
do
    curl --silent --header "Authorization: Bearer $access_token" --location --request GET "https://gitlab.com/api/v4/groups/$organisation_id/projects?include_subgroups=true&per_page=$pagination&page=$page" >> $gitlab_projects_dump_file_raw
done

# Step 2 - Extract repositories URL

# Because of pagination (max 100 items par ages, arbitrary 10 pages here, raw pages are concatenated in one file.
# So with have pasted JSON array in one file.
# We see arrays with pattern ][. Merge all arrays be replacing cumulated JSON arrays, so replacing ][ by ,
# By for empty pages we have the empty arrays ][ replaced by cumulated , so with remove them.
# Then it remains the final array with a useless , with pattern },] replaced by }]
cat $gitlab_projects_dump_file_raw | sed -e "s/\]\[/,/g" | tr -s ',' | sed -e "s/\}\,\]/\}\]/g" > $gitlab_projects_dump_file_clean 

url_for_cloning="./data/.url-for-cloning.txt"
echo "Extract cloning from results (using '$cloning_url_key' as JSON key)..."
python3 "$URL_EXTRACTER_FILE" --field $cloning_url_key --source $gitlab_projects_dump_file_clean > $url_for_cloning
repo_count=`cat $url_for_cloning | wc -l | sed 's/ //g'`
echo "Extraction done. Found '$repo_count' items."

# Step 3 - Clone repositories

dir_before_dump=`pwd`
echo "Creating dump directory..."
directory_name=$(date '+%Y-%m-%d')
cd "$repositories_location"
if [ -d "$directory_name" ]; then
    echo "Removing old directory with the same name"
    rm -rf $directory_name
fi
mkdir $directory_name
cd $directory_name
echo "Dump directory created with name '$directory_name' at location `pwd`."

# Step 4 - For each repository, clone it and make a scan

number_of_url=`cat "$dir_before_dump/$url_for_cloning" | wc | awk {'print $1 '}`
cpt=1
echo "Dumping of $number_of_url repositories..."
while read url_line; do

    # Step 4.1 - Clone
    # WARNING: gitleaks looks inside files and git histories, so for old and big projects it will take too many time!

    echo "Cloning ($cpt / $number_of_url) '$url_line'..."
    git clone "$url_line"

    # Step 4.2 - Extract new folder name
    
    target_folder_name=`basename -s .git $(echo "$url_line")`
    echo "Cloned in folder '$target_folder_name'"

    # Step 5.3 - Look for leaks

    gitleaks_file_name="$target_folder_name".gitleaks.json
    gitleaks detect --report-format json --report-path "$gitleaks_file_name" --source "$target_folder_name" || true # gitleaks returns 1 if leaks found

    # In JSON report, a project as no leak if the result file containsan empty JSON array, i.e. only the line
    # []
    if [ -f "$gitleaks_file_name" ]; then
        pwd
        count=`python3 "../$LEAKS_PARSER" --file "$gitleaks_file_name"`

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

    rm -rf "$target_folder_name"

    cpt=$((cpt+1))

done < "$dir_before_dump/$url_for_cloning"

echo "Scanning done!"

# Step 6 - Clean up

git config --global diff.renameLimit $previous_git_diff_rename_limit # (default seems to be 0)

mv $GITLEAKS_FINAL_REPORT "$dir_before_dump"
echo "GitLab organisation ID...............: '$organisation_id'"
echo "Total number of projects.............: '$number_of_url'"
echo "Number of projects with alerts.......: '$cpt_dirty_repo'"
echo "Number of projects without alerts....: '$cpt_clean_repo'"
echo "Final report is......................: '$GITLEAKS_FINAL_REPORT'"

rm -rf "$target_folder_name"
rm -rf "$dir_before_dump/$url_for_cloning"
cd "$dir_before_dump"
rm -f $url_for_cloning

echo "Check done!"
