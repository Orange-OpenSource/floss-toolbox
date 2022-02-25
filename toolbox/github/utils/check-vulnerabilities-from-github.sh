#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2021-2022 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Since...............: 25/02/2022
# Description.........: Received from arguments a GitHub organisation name and a GitHub personal token path to dump check if vulnerabilities alert exists

#set -euxo pipefail
VERSION="1.0.0"

# Config
# ------

EXIT_OK=0
EXIT_BAD_ARGUMENTS=1
EXIT_BAD_SETUP=2

URL_EXTRACTER_FILE="./utils/extract-repos-field-from-json.py"
VULNERABILITY_PARSER="./utils/count-vulnerabilities-nodes.py"
GITHB_ORGANISATION_VULNERABILITIES_RESULTS="$$_github-organisation-repositories-vulnerabilities-count.csv"

# Functions
# ---------

UsageAndExit(){
    echo "check-vulnerabilities-from-github.sh - Version $VERSION"
	echo "USAGE:"
	echo "bash check-vulnerabilities-from-github.sh ORGANISATION KEY TOKEN"
    echo "with ORGANISATION: GitHub organisation name"
    echo "with KEY: JSON key to sue use cloning URL"
    echo "with TOKEN: personal access token fir requests"
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
    echo "ERROR: Bad set up for URL extracter. Exits now"
    UsageAndExit
    exit $EXIT_BAD_SETUP
fi

if [ -f "VULNERABILITY_PARSER" ]; then
    echo "ERROR: Bad set up vulnerability parser. Exits now"
    UsageAndExit
    exit $EXIT_BAD_SETUP
fi

organisation_name=$1
if [ -z "$organisation_name" ]; then
	echo "ERROR: No organisation name defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

cloning_url_key=$2
if [ -z "$cloning_url_key" ]; then
	echo "ERROR: No JSON key for URL. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

personal_access_token=$3
if [ -z "$personal_access_token" ]; then
	echo "ERROR: No personal access token defined. Exits now."
    UsageAndExit
	exit $EXIT_BAD_ARGUMENTS
fi

# Run
# ---

echo "-------------------------------------------------------"
echo "check-vulnerabilities-from-github.sh - Version $VERSION"
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

# Step 4 - Create workspace directory

dir_before_dump=`pwd`
echo "Creating workspace directory..."
directory_name=$(date '+%Y-%m-%d')
cd "$repositories_location"
if [ -d "$directory_name" ]; then
    echo "Removing old directory with the same name"
    yes | rm -rf $directory_name
fi
mkdir $directory_name
cd $directory_name
echo "Dump directory created with name '$directory_name' at location `pwd`."

# Step 5 - For each repository, check it

number_of_url=`cat "$dir_before_dump/$url_for_cloning" | wc | awk {'print $1 '}`
cpt=1
echo "Dumping of $number_of_url repositories..."
github_request_result_file_raw=".vulnerabilities-github.txt"
github_request_result_file_json=".vulnerabilities-github.json"

echo "status;project name;count of alerts" > $GITHB_ORGANISATION_VULNERABILITIES_RESULTS
cpt_clean_repo=0
cpt_dirty_repo=0
while read url_line; do

    # Step 5.1 - Get repo name
    # We assume URL are like "git@github.com:org/repo.js.git"
    repo_name=`echo "$url_line" | cut -d"/" -f 2 | awk -F".git" '{print $1}'`
    echo "Checking ($cpt / $number_of_url) '$repo_name'..."
    cpt=$((cpt+1))

    # Step 5.2 - Request GitHub API
    graphqlScript='query { repository(name: \"'"$repo_name"'\", owner: \"'"$organisation_name"'\") {
            vulnerabilityAlerts(first: 100) {
                nodes {
                    createdAt
                    dismissedAt
                    securityVulnerability {
                        package {
                            name
                        }
                        advisory {
                            description
                        }
                    }
                }
            }
        }
    }'
    script="$(echo $graphqlScript)"

    curl -s -i -H 'Content-Type: application/json' \
    -H "Authorization: bearer $personal_access_token" \
    -X POST -d "{ \"query\": \"$script\"}" https://api.github.com/graphql -o "$github_request_result_file_raw"

    # Step 5.3 - Process result file

    # We suppose in response paylaod we have the usefull line like
    # {"data":{"repository":{"vulnerabilityAlerts":{"nodes":[]}}}}
    cat $github_request_result_file_raw | grep vulnerabilityAlerts > "$github_request_result_file_json"
    count=`python3 "../$VULNERABILITY_PARSER" --file "$github_request_result_file_json"`

    # Step 5.4 - Build final file
    if [ "$count" -eq "0" ]; then
        echo "😊;$repo_name;$count" >> $GITHB_ORGANISATION_VULNERABILITIES_RESULTS
        cpt_clean_repo=$((cpt_clean_repo+1))
    else
        echo "🚨;$repo_name;$count" >> $GITHB_ORGANISATION_VULNERABILITIES_RESULTS
        echo "🚨 WARNING: Project '$repo_name' has '$count' vulnerability alerts on GitHub!"
        cpt_dirty_repo=$((cpt_dirty_repo+1))
    fi

done < "$dir_before_dump/$url_for_cloning"

echo "GitHub organisation name.............: '$organisation_name'"
echo "Total number of projects.............: '$number_of_url'"
echo "Number of projects with alerts.......: '$cpt_dirty_repo'"
echo "Number of projects without alerts....: '$cpt_clean_repo'"

rm "$github_request_result_file_raw"
rm "$github_request_result_file_json"
cd "$dir_before_dump"
rm -f $url_for_cloning

echo "Check done!"
