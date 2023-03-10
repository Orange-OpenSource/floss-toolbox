#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Since...............: 10/03/2023
# Description.........: Make a dry-run of the github module to check if everything is ready to use
# Version.............: 1.0.0

set -eu

# Couts
# -----

NUMBER_OF_CHECKS=0
NUMBER_OF_SUCCESS=0
NUMBER_OF_WARNINGS=0
NUMBER_OF_ERRORS=0

# Utils
# -----

# $1 - File name to test
CheckIfFileExists(){
    if [ ! -f "$1" ]; then
        echo "⛔  ERROR: The file '$1' does not exist"
        NUMBER_OF_ERRORS=$((NUMBER_OF_ERRORS+1))
    else
        echo "✅  Cool! The file '$1' exists"
        NUMBER_OF_SUCCESS=$((NUMBER_OF_SUCCESS+1))
    fi
    NUMBER_OF_CHECKS=$((NUMBER_OF_CHECKS+1))
}

# $1 - FiDirectory name to test
CheckIfDirectoryExists(){
    if [ ! -d "$1" ]; then
        echo "⛔  ERROR: The directory '$1' does not exist"
        NUMBER_OF_ERRORS=$((NUMBER_OF_ERRORS+1))        
    else
        echo "✅  Cool! The directory '$1' exists"    
        NUMBER_OF_SUCCESS=$((NUMBER_OF_SUCCESS+1))  
    fi
    NUMBER_OF_CHECKS=$((NUMBER_OF_CHECKS+1))
}

# $1 - Runtime name
# $2 - Command to check runtime
# $3 - Expected / suggested version
CheckIfRuntimeExists(){
    runtime_version=`$2`
    if [ $? != "0" ]; then # Exist status != 0 so runtime version check failed ; we assume the runtime is missing
        echo "❌  WARNING: It seems '$1' is not ready"
        NUMBER_OF_ERRORS=$((NUMBER_OF_ERRORS+1))        
    else 
        echo "✅  Cool! '$1' is available"
        echo -e "\t🔎  You should check if the version is at least '$3'"
        NUMBER_OF_SUCCESS=$((NUMBER_OF_SUCCESS+1))
    fi
    NUMBER_OF_CHECKS=$((NUMBER_OF_CHECKS+1))
}

# $1 - Ruby configuration file
# $2 - Key to test
CheckIfConfigurationKeyDefined(){
    CONFIG_KEY=`cat $1 | grep $2 | cut -d= -f2 | tr -d '"' | sed 's/ //g'`
    if [ "$CONFIG_KEY" == "" ]; then
        echo "❔  WARNING: It seems '$2' is not defined in $1"
        NUMBER_OF_WARNINGS=$((NUMBER_OF_WARNINGS+1))
    else
        echo "✅  Cool! '$2' is defined"
        NUMBER_OF_SUCCESS=$((NUMBER_OF_SUCCESS+1))
    fi
    NUMBER_OF_CHECKS=$((NUMBER_OF_CHECKS+1))
}

# GitHub features
# ---------------

echo -e "\n----------------------------------"
echo "Assertions for the GITHUB features"
echo "----------------------------------"

echo -e "\nCheck files..."
CheckIfFileExists "./configuration.rb"
CheckIfFileExists "./GitHubWizard.sh"

CheckIfFileExists "./utils/check-leaks-from-github.sh"
CheckIfFileExists "./utils/check-vulnerabilities-from-github.sh"
CheckIfFileExists "./utils/count-leaks-nodes.py"
CheckIfFileExists "./utils/count-vulnerabilities-nodes.py"
CheckIfFileExists "./utils/dump-git-repositories-from-github.sh"
CheckIfFileExists "./utils/extract-repos-field-from-json.py"
CheckIfFileExists "./utils/GitHubFacade.rb"
CheckIfFileExists "./utils/GitHubWrapper.rb"
CheckIfFileExists "./utils/GitWrapper.rb"
CheckIfFileExists "./utils/IO.rb"

# Runtimes and tools
# ------------------

echo -e "\n-----------------------"
echo "Assertions for runtimes"
echo "-----------------------"

echo -e "\nCheck for Ruby..."
CheckIfRuntimeExists "Ruby" "ruby -v" "2.7.1"

echo -e "\nCheck for Bash..."
CheckIfRuntimeExists "Bash" "bash --version" "3.2.5"

echo -e "\nCheck for Python3..."
CheckIfRuntimeExists "Python3" "python3 --version" "3.8.5"

echo -e "\nCheck for git..."
CheckIfRuntimeExists "git" "git --version" "2.32.0"

echo -e "\nCheck for gh (GitHub CLI)..."
CheckIfRuntimeExists "GitHub CLI (gh)" "gh --version" "1.3.1"

echo -e "\nCheck for Gitleaks..."
CheckIfRuntimeExists "Gitleaks" "gitleaks version" "8.3.0"

echo -e "\nCheck for Octokit..."
CheckIfRuntimeExists "Octokit (Ruby gem)" "gem list | grep octokit" "4.20.0"

# Configuration file
# ------------------

echo -e "\n---------------------------------"
echo "Assertions for configuration file"
echo "---------------------------------"

echo -e "\nCheck for entries in configuration file..."

CheckIfConfigurationKeyDefined "./configuration.rb" "GITHUB_PERSONAL_ACCESS_TOKEN"
CheckIfConfigurationKeyDefined "./configuration.rb" "GITHUB_ORGANIZATION_NAME"
CheckIfConfigurationKeyDefined "./configuration.rb" "GITHUB_ORGANIZATION_ADMINS"
CheckIfConfigurationKeyDefined "./configuration.rb" "GIT_PROJECT_MANDATORY_FILES"
CheckIfConfigurationKeyDefined "./configuration.rb" "REQUEST_DELAY_IN_SECONDS"
CheckIfConfigurationKeyDefined "./configuration.rb" "RESULTS_PER_PAGE"
CheckIfConfigurationKeyDefined "./configuration.rb" "EXPECTED_PAGE_COUNT"
CheckIfConfigurationKeyDefined "./configuration.rb" "OUTPUT_DIRECTORY_NAME"
CheckIfConfigurationKeyDefined "./configuration.rb" "FILENAME_MEMBERS"
CheckIfConfigurationKeyDefined "./configuration.rb" "FILENAME_MEMBERS_2FA_DISABLED"
CheckIfConfigurationKeyDefined "./configuration.rb" "FILENAME_MEMBERS_UNDEFINED_COMPANY"
CheckIfConfigurationKeyDefined "./configuration.rb" "FILENAME_PROJECTS_WITHOUT_TEAM"
CheckIfConfigurationKeyDefined "./configuration.rb" "FILENAME_USERS_WITH_BAD_EMAILS"
CheckIfConfigurationKeyDefined "./configuration.rb" "FILENAME_USERS_WITH_BAD_FULLNAMES"
CheckIfConfigurationKeyDefined "./configuration.rb" "FILENAME_PROJECTS_WITH_UNCONFORM_REPOSITORIES"
CheckIfConfigurationKeyDefined "./configuration.rb" "FILENAME_PROJECTS_WITHOUT_LICENSES"
CheckIfConfigurationKeyDefined "./configuration.rb" "FILENAME_EMPTY_PROJECTS"
CheckIfConfigurationKeyDefined "./configuration.rb" "REPOSITORIES_CLONE_LOCATION_PATH"
CheckIfConfigurationKeyDefined "./configuration.rb" "REPOSITORIES_CLONE_URL_JSON_KEY"
CheckIfConfigurationKeyDefined "./configuration.rb" "EXCLUDE_GITHUB_ARCHIVED_PROJECTS_FOR_SCANS"

echo -e "🔎  I hope configuration entries are - well - defined, be sure of that"

# Conclusion
# ----------

echo -e "\n----------"
echo "Conclusion"
echo "----------"

echo -e "\nDry-run done! See the logs above to check all points controls."
echo -e "\tNumber of controls.......: $NUMBER_OF_CHECKS"
echo -e "\tNumber of success........: $NUMBER_OF_SUCCESS"
echo -e "\tNumber of warnings.......: $NUMBER_OF_WARNINGS"
echo -e "\tNumber of errors.........: $NUMBER_OF_ERRORS"
