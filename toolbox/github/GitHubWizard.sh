#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Since...............: 26/04/2021
# Description.........: Received from arguments a feature to launch and gives it to the Ruby wizard.
# Parses the RUBY_CONFIGURATION_FILE to get the GitHub personal acces token to set as Ruby env. variable (OCTOKIT_ACCESS_TOKEN).

#set -euxo pipefail
VERSION="1.1.0"

# Common files
# ------------

RUBY_CONFIGURATION_FILE="./configuration.rb"
RUBY_MAIN_FILE="./utils/GitHubFacade.rb"
SHELL_REPOSITORIES_DUMPER="./utils/dump-git-repositories-from-github.sh"

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
    echo "GitHubWizard.sh - Version $VERSION"
	echo "USAGE:"
	echo "bash GitHubWizard.sh feature-to-launch"
	echo "with feature-to-launch:"
	echo -e "\t get-members-2fa-disabled................: Loads members of organization with 2FA disabled"
	echo -e "\t get-all-members.........................: Loads all members in the organization"
	echo -e "\t get-members-without-company.............: Loads organization members without company field defined"
	echo -e "\t get-projects-without-team...............: Loads projects without any assigned team"
	echo -e "\t get-users-with-bad-email................: Loads organization members with undefined emails"
    echo -e "\t get-users-with-bad-fullname.............: Loads all members without good full names"
    echo -e "\t get-projects-conformity.................: Checks projects conformity, i.e. with specific files"
    echo -e "\t get-projects-without-licenses...........: Loads projects with missing licenses"
    echo -e "\t get-empty-projects......................: Loads projects which may be empty"
    echo -e "\t set-users-permissions-to-push...........: For all projects update each user permission to 'push' except for teams and administrators"
    echo -e "\t set-teams-permissions-to-push...........: For all projects update each team permission to 'push'"
    echo -e "\t backup-all-repositories-from-org........: Dump all repositoriers in GitHub to a specific location in the disk"
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

if [ $feature_to_run != "get-members-2fa-disabled" -a $feature_to_run != "get-all-members" -a $feature_to_run != "get-members-without-company" -a $feature_to_run != "get-projects-without-team" -a $feature_to_run != "get-users-with-bad-email" -a $feature_to_run != "get-users-with-bad-fullname" -a $feature_to_run != "get-projects-conformity" -a $feature_to_run != "get-projects-without-licenses" -a $feature_to_run != "get-empty-projects" -a $feature_to_run != "set-users-permissions-to-push" -a $feature_to_run != "set-teams-permissions-to-push" -a $feature_to_run != "backup-all-repositories-from-org" ]; then
    echo "ERROR: '$feature_to_run' is unknown feature. Exit now"
    UsageAndExit
    exit $EXIT_UNKNOWN_FEATURE
fi

# Run Ruby toolbox for features with Ruby environment variable set
# ----------------------------------------------------------------

echo "----------------------------------"
echo "GitHubWizard.sh - Version $VERSION"
echo "----------------------------------"

# Common prerequisites

if [ ! -f "$RUBY_CONFIGURATION_FILE" ]; then
    echo "ERROR: RUBY_CONFIGURATION_FILE does not exist. Exits now."
    exit $EXIT_BAD_SETUP
fi

GITHUB_ORGANIZATION_NAME=`cat $RUBY_CONFIGURATION_FILE | grep GITHUB_ORGANIZATION_NAME | cut -d= -f2 | tr -d '"'`
if [ -z "$GITHUB_ORGANIZATION_NAME" ]; then
    echo "ERROR: Cannot define value for GITHUB_ORGANIZATION_NAME from RUBY_CONFIGURATION_FILE. Exits now."
    exit $EXIT_BAD_SETUP
fi

# Specific configuration and script for repositories dump

if [ $feature_to_run == "backup-all-repositories-from-org" ]; then

    if [ ! -f "$SHELL_REPOSITORIES_DUMPER" ]; then
        echo "ERROR: SHELL_REPOSITORIES_DUMPER does not exist. Exits now."
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

    echo "Start Shell script ($SHELL_REPOSITORIES_DUMPER) for feature to dump repositories of '$GITHUB_ORGANIZATION_NAME' to '$REPOSITORIES_CLONE_LOCATION_PATH'"
    start_time_seconds=`date +%s`

    ./$SHELL_REPOSITORIES_DUMPER $CLONING_URL_JSON_KEY $GITHUB_ORGANIZATION_NAME $REPOSITORIES_CLONE_LOCATION_PATH

# Need specific configuration and files for the other features

else

    if [ ! -f "$RUBY_MAIN_FILE" ]; then
        echo "ERROR: RUBY_MAIN_FILE does not exist. Exits now."
        exit $EXIT_BAD_SETUP
    fi

    GITHUB_ORGANIZATION_ADMINS=`cat $RUBY_CONFIGURATION_FILE | grep GITHUB_ORGANIZATION_ADMINS | cut -d= -f2 | tr -d '"'`
    if [ -z "$GITHUB_ORGANIZATION_ADMINS" ]; then
        echo "ERROR: Cannot define value for GITHUB_ORGANIZATION_ADMINS from RUBY_CONFIGURATION_FILE. Exits now."
        exit $EXIT_BAD_SETUP	
    fi

    GITHUB_PERSONAL_ACCES_TOKEN=`cat $RUBY_CONFIGURATION_FILE | grep GITHUB_PERSONAL_ACCESS_TOKEN | cut -d= -f2 | tr -d '"'`
    if [ -z "$GITHUB_PERSONAL_ACCES_TOKEN" ]; then
        echo "ERROR: Cannot define value for GITHUB_PERSONAL_ACCES_TOKEN from RUBY_CONFIGURATION_FILE. Exits now."
        exit $EXIT_BAD_SETUP
    fi

    echo "Start Ruby Wizard ($RUBY_MAIN_FILE) for feature '$feature_to_run'"
    start_time_seconds=`date +%s`

    OCTOKIT_ACCESS_TOKEN=$GITHUB_PERSONAL_ACCES_TOKEN ruby $RUBY_MAIN_FILE $feature_to_run

fi

# Stats & bye

return_status=$?
end_time_seconds=`date +%s`
elapsed_time_seconds=`expr $end_time_seconds - $start_time_seconds`
echo "Elapsed time: $elapsed_time_seconds seconds"

exit $return_status