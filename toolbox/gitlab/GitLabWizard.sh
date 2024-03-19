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

# Since...............: 09/03/2022
# Description.........: Received from arguments a feature to launch.

#set -euxo pipefail
VERSION="1.0.0"

# Common files
# ------------

RUBY_CONFIGURATION_FILE="./configuration.rb"
SHELL_REPOSITORIES_DUMPER="./utils/dump-git-repositories-from-gitlab.sh"
SHELL_REPOSITORIES_LEAKS_SCANNER="./utils/check-leaks-from-gitlab.sh"

# Exit codes
# ----------

EXIT_OK=0
EXIT_BAD_ARGUMENTS=1
EXIT_NO_FEATURE=2
EXIT_UNKNOWN_FEATURE=3
EXIT_BAD_SETUP=100

# Functions
# ---------

UsageAndExit(){
    echo "GitLabWizard.sh - Version $VERSION"
    echo "USAGE:"
    echo "bash GitLabWizard.sh feature-to-launch"
    echo "with feature-to-launch:"
    echo -e "\t backup-all-repositories-from-org...............: Dump all repositories in GitHub to a specific location in the disk"
    echo -e "\t look-for-leaks.................................: Checks with gitleaks if there are leaks in all repositories"
    echo "About exit codes:"
    echo -e "\t 0................: Normal exit"
    echo -e "\t 1................: Bad arguments given to the script"
    echo -e "\t 2................: No defined feature in argument"
    echo -e "\t 3................: Feature not recognized"
    echo -e "\t 100..............: Bad prerequisites to run this script"
    exit $EXIT_OK
}

# Check arguments
# ---------------

if [ "$#" -eq 0 ]; then
    UsageAndExit
    exit $EXIT_OK
fi

if [ "$#" -ne 1 ]; then
    echo "ERROR: Bad arguments. Exit now"
    UsageAndExit
    exit $EXIT_BAD_ARGUMENTS
fi

feature_to_run=$1

if [ -z "$feature_to_run" ]; then
	echo "ERROR: No feature to run. Exit now."
    UsageAndExit
	exit $EXIT_NO_FEATURE
fi

if [ $feature_to_run != "backup-all-repositories-from-org" -a $feature_to_run != "look-for-leaks" ]; then
    echo "ERROR: '$feature_to_run' is unknown feature. Exit now"
    UsageAndExit
    exit $EXIT_UNKNOWN_FEATURE
fi

# Run toolbox for features
# ------------------------

echo "----------------------------------"
echo "GitLabWizard.sh - Version $VERSION"
echo "----------------------------------"

# Common prerequisites

if [ ! -f "$RUBY_CONFIGURATION_FILE" ]; then
    echo "ERROR: RUBY_CONFIGURATION_FILE does not exist. Exits now."
    exit $EXIT_BAD_SETUP
fi

# Features: backup-all-repositories-from-org, look-for-leaks
if [ $feature_to_run == "backup-all-repositories-from-org" -o $feature_to_run == "look-for-leaks" ]; then

    if [ ! -f "$SHELL_REPOSITORIES_DUMPER" ]; then
        echo "ERROR: SHELL_REPOSITORIES_DUMPER does not exist. Exits now."
        exit $EXIT_BAD_SETUP
    fi

    GITLAB_ORGANIZATION_ID=`cat $RUBY_CONFIGURATION_FILE | grep GITLAB_ORGANIZATION_ID | cut -d= -f2 | tr -d '"'`
    if [ -z "$GITLAB_ORGANIZATION_ID" ]; then
        echo "ERROR: Cannot define value for GITLAB_ORGANIZATION_ID from RUBY_CONFIGURATION_FILE. Exits now."
        exit $EXIT_BAD_SETUP
    fi

    GILAB_PERSONAL_ACCESS_TOKEN=`cat $RUBY_CONFIGURATION_FILE | grep GILAB_PERSONAL_ACCESS_TOKEN | cut -d= -f2 | tr -d '"'`
    if [ -z "$GILAB_PERSONAL_ACCESS_TOKEN" ]; then
        echo "ERROR: Cannot define value for GILAB_PERSONAL_ACCESS_TOKEN from RUBY_CONFIGURATION_FILE. Exits now."
        exit $EXIT_BAD_SETUP
    fi

    RESULTS_PER_PAGE=`cat $RUBY_CONFIGURATION_FILE | grep RESULTS_PER_PAGE | cut -d= -f2 | tr -d '"'`
    if [ -z "$RESULTS_PER_PAGE" ]; then
        echo "ERROR: Cannot define value for RESULTS_PER_PAGE from RUBY_CONFIGURATION_FILE. Exits now."
        exit $EXIT_BAD_SETUP
    fi

    CLONING_URL_JSON_KEY=`cat $RUBY_CONFIGURATION_FILE | grep REPOSITORIES_CLONE_URL_JSON_KEY | cut -d= -f2 | tr -d '"'`
    if [ -z "$CLONING_URL_JSON_KEY" ]; then
        echo "ERROR: Cannot define value for CLONING_URL_JSON_KEY from RUBY_CONFIGURATION_FILE. Exits now."
        exit $EXIT_BAD_SETUP
    fi

    REPOSITORIES_CLONE_LOCATION_PATH=`cat $RUBY_CONFIGURATION_FILE | grep REPOSITORIES_CLONE_LOCATION_PATH | cut -d= -f2 | tr -d '"'`
    if [ -z "$REPOSITORIES_CLONE_LOCATION_PATH" ]; then
        echo "ERROR: Cannot define value for REPOSITORIES_CLONE_LOCATION_PATH from RUBY_CONFIGURATION_FILE. Exits now."
        exit $EXIT_BAD_SETUP
    fi

    start_time_seconds=`date +%s`
    
    if [ $feature_to_run == "backup-all-repositories-from-org" ]; then
        echo "Start Shell script ($SHELL_REPOSITORIES_DUMPER) for feature to dump repositories of '$GITLAB_ORGANIZATION_ID' to '$REPOSITORIES_CLONE_LOCATION_PATH'"
        ./$SHELL_REPOSITORIES_DUMPER $CLONING_URL_JSON_KEY $GITLAB_ORGANIZATION_ID $RESULTS_PER_PAGE $REPOSITORIES_CLONE_LOCATION_PATH $GILAB_PERSONAL_ACCESS_TOKEN
    fi

    if [ $feature_to_run == "look-for-leaks" ]; then
        echo "Start Shell script ($SHELL_REPOSITORIES_LEAKS_SCANNER) to look for leaks in repositories of '$GITLAB_ORGANIZATION_ID'"
        ./$SHELL_REPOSITORIES_LEAKS_SCANNER $GITLAB_ORGANIZATION_ID $CLONING_URL_JSON_KEY $RESULTS_PER_PAGE $GILAB_PERSONAL_ACCESS_TOKEN
    fi
fi

# Stats & bye

return_status=$?
end_time_seconds=`date +%s`
elapsed_time_seconds=`expr $end_time_seconds - $start_time_seconds`
echo "Elapsed time: $elapsed_time_seconds seconds"

exit $return_status