#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Since...............: 25/02/2022
# Description.........: Received from arguments a GitHub organisation name and a GitHub personal token path to dump check if vulnerabilities alert exists

#set -euxo pipefail
VERSION="2.0.0"

# Config
# ------

EXIT_OK=0
EXIT_BAD_ARGUMENTS=1
EXIT_BAD_SETUP=2

FIELD_EXTRACTER_FILE="./utils/extract-repos-field-from-json.py"
VULNERABILITY_PARSER="./utils/count-vulnerabilities-nodes.py"
GITHB_ORGANISATION_VULNERABILITIES_RESULTS="$$_github-organisation-repositories-vulnerabilities-count.csv"

# Functions
# ---------

UsageAndExit(){
    echo "check-vulnerabilities-from-github.sh - Version $VERSION"
	echo "USAGE:"
	echo "bash check-vulnerabilities-from-github.sh ORGANISATION KEY TOKEN EXCLUDE_ARCHIVED"
    echo "with ORGANISATION: GitHub organisation name"
    echo "with KEY: JSON key to use for cloning URL"
    echo "with TOKEN: personal access token for requests"
    echo "with EXCLUDE_ARCHIVED: true to exlude archived projects from scans, false to scan them"
    echo "About exit codes:"
	echo -e "\t 0................: Normal exit"
	echo -e "\t 1................: Bad arguments given to the script"
    echo -e "\t 2................: File FIELD_EXTRACTER_FILE or VULNERABILITY_PARSER is not defined. Impossible to extract URL from API results and parse them."
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

if [ ! -f "$FIELD_EXTRACTER_FILE" ]; then
    echo "ERROR: Bad set up for URL extracter. Exits now"
    UsageAndExit
    exit $EXIT_BAD_SETUP
fi

if [ ! -f "$VULNERABILITY_PARSER" ]; then
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

exclude_archived=$4
if [ -z "$exclude_archived" ]; then
	echo "ERROR: No flag set to say wether or not archived projects must be scanned. Exits now."
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

# Step 3 - Extract repo URL

repos_url_for_requests=".repos-url-for-requests.txt"
echo "Extract cloning from results (using '$cloning_url_key' as JSON key)..."
python3 "$FIELD_EXTRACTER_FILE" --field $cloning_url_key --source $repositories_list_clean_temp_file > $repos_url_for_requests
echo "Extraction of URL done."

# Step 4 - Extract repo archived state

# WARNING: We assume the two runs of FIELD_EXTRACTER_FILE script will be made on the same JSON file and with exactly the same iteration order.
# Thus the project with previous run having its URL at Nth position will have is archived status at that same Nth position.
# If the process of JSON file cannot confirm the iteration order is the same between runs or if another request is made with several JSON files,
# the following code block may be quite crappy.
repos_archived_state=".repos-archived-state.txt"
echo "Extract archived status from results (using 'archived' as JSON key)..."
python3 "$FIELD_EXTRACTER_FILE" --field 'archived' --source $repositories_list_clean_temp_file > $repos_archived_state
rm -f $repositories_list_clean_temp_file
echo "Extraction of archived status done."

# Step 5 - Create workspace directory

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

# Step 6 - For each repository, check it

number_of_url=`cat "$dir_before_dump/$repos_url_for_requests" | wc | awk {'print $1 '}`
cpt=1
echo "Checking of $number_of_url repositories..."
github_request_result_file_raw=".vulnerabilities-github.txt"
github_request_result_file_json=".vulnerabilities-github.json"

echo "status;project name;count of alerts" > $GITHB_ORGANISATION_VULNERABILITIES_RESULTS
cpt_clean_repo=0
cpt_archived_repo=0
cpt_archived_repo_not_scanned=0
cpt_dirty_repo=0

while read url_line; do

    # Step 6.1 - Get repo name
    # We assume URL are like "git@github.com:org/repo.js.git"
    repo_name=`echo "$url_line" | cut -d"/" -f 2 | awk -F".git" '{print $1}'`
    
    # Step 6.2 - Get repo archived status
    # We assume the line N has 'True' or 'False' value syntax and matches the project with URL at line N with previous code block
    repo_archived_status=`awk "NR==$cpt" "../$repos_archived_state"`

    echo "Checking ($cpt / $number_of_url) '$repo_name'. Is archived? $repo_archived_status"
    if [ "$repo_archived_status" == "True" ]; then
        cpt_archived_repo=$((cpt_archived_repo+1))
    fi
    
    cpt=$((cpt+1))

    # Make request of archived proejcts not excluded or if the archived proejcts are excluded and the current repo is not archived
    if [[ ( "$exclude_archived" == "false" ) || ( "$exclude_archived" != "false" && "$repo_archived_status" != "True" ) ]]; then

        # Step 6.3 - Request GitHub API
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

        # Step 6.4 - Process result file

        # We suppose in response payload we have the useful line like
        # {"data":{"repository":{"vulnerabilityAlerts":{"nodes":[]}}}}
        cat $github_request_result_file_raw | grep vulnerabilityAlerts > "$github_request_result_file_json"
        count=`python3 "../$VULNERABILITY_PARSER" --file "$github_request_result_file_json"`

    else # "$repo_archived_status" == "True" 
        count='-1'
    fi

    # Step 6.5 - Build final file

    if [ "$count" == "0" ]; then # No vulnerabilities
        echo "😊;$repo_name;$count" >> $GITHB_ORGANISATION_VULNERABILITIES_RESULTS
        cpt_clean_repo=$((cpt_clean_repo+1))
    elif [ "$count" == "-1" ]; then # No scan because of archived project
        echo "🔒;$repo_name;$count" >> $GITHB_ORGANISATION_VULNERABILITIES_RESULTS
        echo "🔒 NOTE: Project '$repo_name' is archived and the defined strategy in configuration is to ignore it"
        cpt_archived_repo_not_scanned=$((cpt_archived_repo_not_scanned+1))
    else # Vulnerabilities
        echo "🚨;$repo_name;$count" >> $GITHB_ORGANISATION_VULNERABILITIES_RESULTS
        echo "🚨 WARNING: Project '$repo_name' has '$count' vulnerability alerts on GitHub!"
        cpt_dirty_repo=$((cpt_dirty_repo+1))
    fi

done < "$dir_before_dump/$repos_url_for_requests"

echo "------------------------------------------------"
echo "GitHub organisation name .......................: '$organisation_name'"
echo "Total number of projects .......................: '$number_of_url'"
echo "Number of projects with alerts 🚨...............: '$cpt_dirty_repo'"
echo "Number of projects without alerts 😊............: '$cpt_clean_repo'"
echo "Number of archived projects not scanned 🔒......: '$cpt_archived_repo_not_scanned'"
echo "Number of archived projects ....................: '$cpt_archived_repo'"
echo "------------------------------------------------"

rm "$github_request_result_file_raw"
rm "$github_request_result_file_json"
cd "$dir_before_dump"

rm -f $repos_url_for_requests
rm -f $repos_archived_state

echo "Check done!"
