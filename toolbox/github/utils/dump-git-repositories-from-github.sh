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

# Since...............: 24/01/2022
# Description.........: Received from arguments a GitHub organisation name and a location path to dump all repositories from this GitHub organisation to that path.

#set -euxo pipefail
VERSION="1.0.0"

# Config
# ------

EXIT_OK=0
EXIT_BAD_ARGUMENTS=1
EXIT_BAD_SETUP=2

URL_EXTRACTER_FILE="./utils/extract-repos-field-from-json.py"

# Functions
# ---------

UsageAndExit(){
    echo "dump-git-repositories-from-github.sh - Version $VERSION"
	echo "USAGE:"
	echo "bash dump-git-repositories-from-github.sh KEY ORGANISATION DESTINATION"
    echo "with KEY: JSON key to ge cloning URL"
	echo "with ORGANISATION: GitHub organisation name"
    echo "with DESTINATION: Destination to download the clones of the ORGANISATION repositories"
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

if [ "$#" -ne 3 ]; then
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

organisation_name=$2
if [ -z "$organisation_name" ]; then
	echo "ERROR: No organisation name defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

repositories_location=$3
if [ -z "$repositories_location" ]; then
	echo "ERROR: No location for clones is defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

# Run
# ---

echo "-------------------------------------------------------"
echo "dump-git-repositories-from-github.sh - Version $VERSION"
echo "-------------------------------------------------------"

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

# Step 4 - Create dump directory
dir_before_dump=`pwd`
echo "Creating dump directory..."
directory_name=$(date '+%Y-%m-%d')
cd "$repositories_location"
if [ -d "$directory_name" ]; then
    echo "Removing old directory with the same name"
    yes | rm -rf $directory_name
fi
mkdir $directory_name
cd $directory_name
echo "Dump directory created with name '$directory_name' at location `pwd`."

# Step 5 - For each repository, clone it
number_of_url=`cat "$dir_before_dump/$url_for_cloning" | wc | awk {'print $1 '}`
cpt=1
echo "Dumping of $number_of_url repositories..."
while read url_line; do
    echo "Cloning ($cpt / $number_of_url) '$url_line'..."
    git clone "$url_line"
    cpt=$((cpt+1))
done < "$dir_before_dump/$url_for_cloning"
echo "Dump done!"

cd "$dir_before_dump"
rm -f $url_for_cloning