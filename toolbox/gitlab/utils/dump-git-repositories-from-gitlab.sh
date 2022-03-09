#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Since...............: 09/03/2022
# Description.........: Received from arguments a GitLab organisation name ID a location path to dump all repositories from this GitLab organisation to that path.

#set -euxo pipefail
VERSION="1.0.0"

# Config
# ------

EXIT_OK=0
EXIT_BAD_ARGUMENTS=1
EXIT_BAD_SETUP=2

URL_EXTRACTER_FILE="./../github/utils/extract-repos-field-from-json.py" # TODO: Extract this Python sript to common files

# Functions
# ---------

UsageAndExit(){
    echo "dump-git-repositories-from-gitlab.sh - Version $VERSION"
	echo "USAGE:"
	echo "bash dump-git-repositories-from-gitlab.sh KEY ORGANISATION DESTINATION"
    echo "with KEY: JSON key to ge cloning URL"
	echo "with ORGANISATION: GitLab organisation ID"
    echo "with PAGINATE: Number of items by page for requests"
    echo "with DESTINATION: Destination to download the clones of the ORGANISATION repositories"
    echo "with TOKEN: GitLab access token to make the request"
    echo "About exit codes:"
	echo -e "\t 0................: Normal exit"
	echo -e "\t 1................: Bad arguments given to the script"
    echo -e "\t 2................: File URL_EXTRACTER_FILE is not defined. Impossible to extract URL from API results."
	exit $EXIT_OK
}

# Check setup
# -----------

if [ "$#" -eq 0 ]; then
    UsageAndExit
    exit $EXIT_OK
fi

if [ "$#" -ne 5 ]; then
    echo "ERROR: Bad arguments number. Exits now"
    UsageAndExit
    exit $EXIT_BAD_ARGUMENTS
fi

if [ ! -f "$URL_EXTRACTER_FILE" ]; then
    echo "ERROR: Bad set up fr URL extracter. Exits now"
    UsageAndExit
    exit $EXIT_BAD_SETUP
fi

cloning_url_key=$1
if [ -z "$cloning_url_key" ]; then
	echo "ERROR: No JSON key for URL. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

organisation_id=$2
if [ -z "$organisation_id" ]; then
	echo "ERROR: No organisation ID defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

pagination=$3
if [ -z "$pagination" ]; then
	echo "ERROR: No pagination defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

repositories_location=$4
if [ -z "$repositories_location" ]; then
	echo "ERROR: No location for clones is defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

access_token=$5
if [ -z "$access_token" ]; then
	echo "ERROR: No access token is defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

# Run
# ---

echo "-------------------------------------------------------"
echo "dump-git-repositories-from-gitlab.sh - Version $VERSION"
echo "-------------------------------------------------------"

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
    curl --header "Authorization: Bearer $access_token" --location --request GET "https://gitlab.com/api/v4/groups/$organisation_id/projects?include_subgroups=true&per_page=$pagination&page=$page" >> $gitlab_projects_dump_file_raw
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

# Step 4 - For each repository, clone it

number_of_url=`cat "$dir_before_dump/$url_for_cloning" | wc | awk {'print $1 '}`
cpt=1
echo "Dumping of $number_of_url repositories..."
while read url_line; do
    echo "Cloning ($cpt / $number_of_url) '$url_line'..."
    git clone "$url_line"
    cpt=$((cpt+1))
done < "$dir_before_dump/$url_for_cloning"

echo "Dump done!"

# Step 5 - Clean up

cd $dir_before_dump

rm $gitlab_projects_dump_file_raw
rm $gitlab_projects_dump_file_clean
rm $url_for_cloning