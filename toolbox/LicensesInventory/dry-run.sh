#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Since...............: 10/03/2023
# Description.........: Make a dry-run of the LicensesIventory module to check if everything is ready to use
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
# Licenses Inventory tool
# -----------------------

echo -e "\n------------------------------------------"
echo "Assertions for the Licenses Inventory tool"
echo "------------------------------------------"

echo -e "\nCheck if main folders exist..."
CheckIfDirectoryExists "./sources"
CheckIfDirectoryExists "./tests"

echo -e "\nCheck sources files..."
CheckIfFileExists "./sources/common/__init__.py"
CheckIfFileExists "./sources/common/datas.py"
CheckIfFileExists "./sources/common/files.py"
CheckIfFileExists "./sources/common/filters.py"
CheckIfFileExists "./sources/common/names.py"
CheckIfFileExists "./sources/configuration/__init__.py"
CheckIfFileExists "./sources/configuration/config.py"
CheckIfFileExists "./sources/dependencies/__init__.py"
CheckIfFileExists "./sources/dependencies/dependencies.py"
CheckIfFileExists "./sources/dependencies/parsings.py"
CheckIfFileExists "./sources/search/__init__.py"
CheckIfFileExists "./sources/search/downloads.py"
CheckIfFileExists "./sources/search/parsings.py"
CheckIfFileExists "./sources/search/search.py"
CheckIfFileExists "./sources/__init__.py"
CheckIfFileExists "./sources/main.py"
CheckIfFileExists "./config.ini"

echo -e "\nCheck integration test files..."
CheckIfFileExists "./tests/integrationtests/data/gradle/dependency_github.gradle"
CheckIfFileExists "./tests/integrationtests/data/gradle/dependency_maven_central.gradle"
CheckIfFileExists "./tests/integrationtests/data/gradle/license_github.json"
CheckIfFileExists "./tests/integrationtests/data/gradle/license_maven_central.pom"
CheckIfFileExists "./tests/integrationtests/data/gradle/version_maven_central.json"
CheckIfFileExists "./tests/integrationtests/data/package_json/license_package_json.html"
CheckIfFileExists "./tests/integrationtests/data/package_json/package.json"
CheckIfFileExists "./tests/integrationtests/data/roast/Cargo.lock"
CheckIfFileExists "./tests/integrationtests/data/config.ini"
CheckIfFileExists "./tests/integrationtests/test_search.py"

echo -e "\nCheck unit test files..."
CheckIfFileExists "./tests/unittests/data/config/config_no_data.ini"
CheckIfFileExists "./tests/unittests/data/config/config.ini"
CheckIfFileExists "./tests/unittests/data/get_content_by_name/my_gradle_file.txt"
CheckIfFileExists "./tests/unittests/data/get_content_by_name/package.json"
CheckIfFileExists "./tests/unittests/data/gradle/license_github.json"
CheckIfFileExists "./tests/unittests/data/gradle/license_maven_central.pom"
CheckIfFileExists "./tests/unittests/data/gradle/version.json"
CheckIfFileExists "./tests/unittests/data/package_json/license_package_json.html"
CheckIfFileExists "./tests/unittests/data/roast/license_roast.json"
CheckIfFileExists "./tests/unittests/data/dependency_a.txt"
CheckIfFileExists "./tests/unittests/data/dependency_b.txt"
CheckIfFileExists "./tests/unittests/data/filename_by_name.test"
CheckIfFileExists "./tests/unittests/data/files_read.txt"
CheckIfFileExists "./tests/unittests/test_config.py"
CheckIfFileExists "./tests/unittests/test_dependency.py"
CheckIfFileExists "./tests/unittests/test_files_check_the_directory.py"
CheckIfFileExists "./tests/unittests/test_files_get_the_filenames_by_name.py"
CheckIfFileExists "./tests/unittests/test_files_write_and_read.py"
CheckIfFileExists "./tests/unittests/test_filter.py"
CheckIfFileExists "./tests/unittests/test_parsing_download.py"
CheckIfFileExists "./tests/unittests/test_parsing.py"

# Runtimes and tools
# ------------------

echo -e "\n-----------------------"
echo "Assertions for runtimes"
echo "-----------------------"

echo -e "\nCheck for Python3..."
CheckIfRuntimeExists "Python3" "python3 --version" "3.8.5"

echo -e "\nCheck for Python modules"
CheckIfPythonModuleInstalled "requests"
CheckIfPythonModuleInstalled "xmltodict"
CheckIfPythonModuleInstalled "pytest"

# Units tests
# -----------

echo -e "\n----------------------------------"
echo "Run of LicensesInventory unit test"
echo "----------------------------------"

echo -e "\nRunning integration tests..."
python3 -m pytest ./tests/integrationtests/*.py

echo -e "\nRunning unit tests..."
python3 -m pytest ./tests/unittests/*.py

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
