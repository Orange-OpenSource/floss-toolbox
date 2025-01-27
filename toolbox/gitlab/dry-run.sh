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

# Since...............: 10/03/2023
# Description.........: Make a dry-run of the gitlab module to check if everything is ready to use
# Version.............: 1.2.0

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

# $1 - Directory name to test
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

# GitLab features
# ---------------

echo -e "\n----------------------------------"
echo "Assertions for the GITLAB features"
echo "----------------------------------"

CheckIfDirectoryExists "./data"

echo -e "\nCheck files..."
CheckIfFileExists "./configuration.rb"
CheckIfFileExists "./GitLabWizard.sh"
CheckIfFileExists "./utils/dump-git-repositories-from-gitlab.sh"
CheckIfFileExists "../github/utils/extract-repos-field-from-json.py" # Stored in github folder but used by dump-git-repositories-from-gitlab.sh
CheckIfFileExists "../github/utils/count-leaks-nodes.py" # Stored in github folder but used by check-leaks-from-gitlab.sh

CheckIfFileExists "./gitlab-year-review.py"
CheckIfFileExists "./requirements.txt"
CheckIfFileExists "./.env" # Warning: not versioned but mandatory for Python script above

# Runtimes and tools
# ------------------

echo -e "\n-----------------------"
echo "Assertions for runtimes"
echo "-----------------------"

echo -e "\nCheck for Bash..."
CheckIfRuntimeExists "Bash" "bash --version" "3.2.5"

echo -e "\nCheck for Python3..."
CheckIfRuntimeExists "Python3" "python3 --version" "3.8.5"

echo -e "\nCheck for git..."
CheckIfRuntimeExists "git" "git --version" "2.32.0"

echo -e "\nCheck for Gitleaks..."
CheckIfRuntimeExists "Gitleaks" "gitleaks version" "8.3.0"

# Configuration file
# ------------------

echo -e "\n---------------------------------"
echo "Assertions for configuration file"
echo "---------------------------------"

echo -e "\nCheck for entries in configuration file..."

CheckIfConfigurationKeyDefined "./configuration.rb" "GILAB_PERSONAL_ACCESS_TOKEN"
CheckIfConfigurationKeyDefined "./configuration.rb" "GITLAB_ORGANIZATION_ID"
CheckIfConfigurationKeyDefined "./configuration.rb" "RESULTS_PER_PAGE"
CheckIfConfigurationKeyDefined "./configuration.rb" "REPOSITORIES_CLONE_LOCATION_PATH"
CheckIfConfigurationKeyDefined "./configuration.rb" "REPOSITORIES_CLONE_URL_JSON_KEY"

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
