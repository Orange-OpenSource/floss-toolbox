#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Since...............: 10/03/2023
# Description.........: Make a dry-run of the diver module to check if everything is ready to use
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

# $1 - The name of the Python module to test
CheckIfPythonModuleInstalled(){
    if [ "$#" -ne 1 ]; then
        echo "❌  WARNING: It seems '$1' is not ready"
        NUMBER_OF_ERRORS=$((NUMBER_OF_ERRORS+1))  
    else
        python3 -c "import $1"
        result=$?
        if [ $result == "0" ]; then
            echo "✅  Cool! Python module '$1' is available"
            NUMBER_OF_SUCCESS=$((NUMBER_OF_SUCCESS+1))
        else
            echo "❌  WARNING: It seems Python modyle '$1' is not installed"
            NUMBER_OF_ERRORS=$((NUMBER_OF_ERRORS+1))  
        fi
    fi
    NUMBER_OF_CHECKS=$((NUMBER_OF_CHECKS+1))
}

# Diver features
# --------------

echo "---------------------------------"
echo "Assertions for the DIVER features"
echo "---------------------------------"

echo -e "\nCheck scripts..."
CheckIfFileExists "./extract-emails-from-history.sh"
CheckIfFileExists "./find-contributors-in-files.sh"
CheckIfFileExists "./find-contributors-in-git-logs.sh"
CheckIfFileExists "./find-credentials-in-files.sh"
CheckIfFileExists "./find-credits-in-files.sh"
CheckIfFileExists "./find-missing-developers-in-git-commits.sh"
CheckIfFileExists "./list-contributors-in-history.sh"
CheckIfFileExists "./lines-count.sh"

echo -e "\nCheck utilitary scripts..."
CheckIfFileExists "./utils/extract-contributors-lists.rb"
CheckIfFileExists "./utils/find-contributors-in-git-logs.rb"
CheckIfFileExists "./utils/find-hotwords-in-files.sh"
CheckIfFileExists "./utils/find-missing-developers-in-git-commits.rb"

echo -e "\nCheck for generated files folder..."
CheckIfDirectoryExists "./data"

echo -e "\nCheck other files..."
CheckIfFileExists "./README.md"

# Runtimes and tools
# ------------------

echo -e "\n-----------------------"
echo "Assertions for runtimes"
echo "-----------------------"

echo -e "\nCheck for Ruby..."
CheckIfRuntimeExists "Ruby" "ruby -v" "2.7.1"

echo -e "\nCheck for Bash..."
CheckIfRuntimeExists "Bash" "bash --version" "3.2.5"

echo -e "\nCheck for git..."
CheckIfRuntimeExists "git" "git --version" "2.32.0"

echo -e "\nCheck for cloc..."
CheckIfRuntimeExists "cloc" "cloc --version" "1.88"

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
