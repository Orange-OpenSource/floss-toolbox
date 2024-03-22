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
# Description.........: Make a dry-run of the LicensesInventory module to check if everything is ready to use
# Version.............: 2.4.0

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
        python3.8 -c "import $1"
        result=$?
        if [ $result == "0" ]; then
            echo "✅  Cool! Python module '$1' is available"
            NUMBER_OF_SUCCESS=$((NUMBER_OF_SUCCESS+1))
        else
            echo "❌  WARNING: It seems Python module '$1' is not installed"
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

echo -e "\nCheck if main folders and root items exist..."
CheckIfDirectoryExists "./sources"
CheckIfDirectoryExists "./tests"
CheckIfFileExists "config.ini"
CheckIfFileExists "requirements.txt"
CheckIfFileExists "README.md"

echo -e "\nCheck sources files..."

CheckIfFileExists "./sources/common/__init__.py"
CheckIfFileExists "./sources/common/choices.py"
CheckIfFileExists "./sources/common/comments.py"
CheckIfFileExists "./sources/common/data_in_blocks.py"
CheckIfFileExists "./sources/common/datas.py"
CheckIfFileExists "./sources/common/date_from_requests_retry_after.py"
CheckIfFileExists "./sources/common/dates_and_times.py"
CheckIfFileExists "./sources/common/files.py"
CheckIfFileExists "./sources/common/filters.py"
CheckIfFileExists "./sources/common/names.py"
CheckIfFileExists "./sources/common/prompts.py"

CheckIfFileExists "./sources/configuration/__init__.py"
CheckIfFileExists "./sources/configuration/config.py"

CheckIfFileExists "./sources/dependency/__init__.py"
CheckIfFileExists "./sources/dependency/dependencies.py"
CheckIfFileExists "./sources/dependency/parsings.py"

CheckIfFileExists "./sources/search/__init__.py"
CheckIfFileExists "./sources/search/downloads.py"
CheckIfFileExists "./sources/search/parsings.py"
CheckIfFileExists "./sources/search/search.py"

CheckIfFileExists "./sources/__init__.py"
CheckIfFileExists "./sources/main.py"
CheckIfFileExists "./sources/test_main.py"

echo -e "\nCheck integration test files..."

CheckIfDirectoryExists "./tests/integrationtests/real_data/"

CheckIfFileExists "./tests/integrationtests/real_data/2 dependencies/build.gradle.kts"
CheckIfFileExists "./tests/integrationtests/real_data/2 dependencies/Cargo.lock"
CheckIfFileExists "./tests/integrationtests/real_data/2 dependencies/go.mod"
CheckIfFileExists "./tests/integrationtests/real_data/2 dependencies/package.json"
CheckIfFileExists "./tests/integrationtests/real_data/2 dependencies/Package.swift"
CheckIfFileExists "./tests/integrationtests/real_data/2 dependencies/Podfile"
CheckIfFileExists "./tests/integrationtests/real_data/2 dependencies/pubspec.yaml"
CheckIfFileExists "./tests/integrationtests/real_data/dependencies/build.gradle.kts"
CheckIfFileExists "./tests/integrationtests/real_data/dependencies/Cargo.lock"
CheckIfFileExists "./tests/integrationtests/real_data/dependencies/go.mod"
CheckIfFileExists "./tests/integrationtests/real_data/dependencies/package.json"
CheckIfFileExists "./tests/integrationtests/real_data/dependencies/Package.swift"
CheckIfFileExists "./tests/integrationtests/real_data/dependencies/Podfile"
CheckIfFileExists "./tests/integrationtests/real_data/dependencies/pubspec.yaml"
CheckIfFileExists "./tests/integrationtests/real_data/config_2_retry_after.ini"
CheckIfFileExists "./tests/integrationtests/real_data/config_2.ini"
CheckIfFileExists "./tests/integrationtests/real_data/config_3.ini"
CheckIfFileExists "./tests/integrationtests/real_data/config_4.ini"
CheckIfFileExists "./tests/integrationtests/real_data/config.ini"

CheckIfFileExists "./tests/integrationtests/test_1_all_dependencies.py"
CheckIfFileExists "./tests/integrationtests/test_2_2_dependencies_per_platform_saving_licenses.py"
CheckIfFileExists "./tests/integrationtests/test_3_print_with_error_403.py"
CheckIfFileExists "./tests/integrationtests/test_4_2_dependencies_per_platform_saving_errors.py"

echo -e "\nCheck unit test files..."

CheckIfFileExists "./tests/unittests/data/config_ini/config_empty.ini"
CheckIfFileExists "./tests/unittests/data/config_ini/config_no_file.ini"
CheckIfFileExists "./tests/unittests/data/config_ini/config_no_path_licenses.ini"
CheckIfFileExists "./tests/unittests/data/config_ini/config_no_path_to_parse.ini"
CheckIfFileExists "./tests/unittests/data/config_ini/config.ini"

CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies/build.gradle.kts"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies/Cargo.lock"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies/go.mod"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies/package.json"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies/Package.swift"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies/Podfile"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies/pubspec.yaml"

CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_empty/build.gradle.kts"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_empty/Cargo.lock"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_empty/go.mod"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_empty/package.json"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_empty/Package.swift"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_empty/Podfile"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_empty/pubspec.yaml"

CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_on_error/errors_Cargo.lock.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_on_error/errors_go.mod.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_on_error/errors_gradle.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_on_error/errors_package.json.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_on_error/errors_Package.swift.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_on_error/errors_Podfile.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/dependencies_on_error/errors_pubspec.yaml.txt"

CheckIfFileExists "./tests/unittests/data/get_the_dependencies/licenses/licenses_cargo_lock.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/licenses/licenses_go_mod.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/licenses/licenses_gradle.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/licenses/licenses_package_json.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/licenses/licenses_package_swift.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/licenses/licenses_Podfile.txt"
CheckIfFileExists "./tests/unittests/data/get_the_dependencies/licenses/licenses_pubspec_yaml.txt"

CheckIfFileExists "./tests/unittests/data/get_the_licenses/sources/build.gradle"
CheckIfFileExists "./tests/unittests/data/get_the_licenses/sources/Cargo.lock"
CheckIfFileExists "./tests/unittests/data/get_the_licenses/sources/go.mod.txt"
CheckIfFileExists "./tests/unittests/data/get_the_licenses/sources/package.json"
CheckIfFileExists "./tests/unittests/data/get_the_licenses/sources/Package.swift"
CheckIfFileExists "./tests/unittests/data/get_the_licenses/sources/Podfile"
CheckIfFileExists "./tests/unittests/data/get_the_licenses/sources/pubspec.yaml"

CheckIfFileExists "./tests/unittests/data/save/errors_file/errors_p_a.txt"
CheckIfFileExists "./tests/unittests/data/save/errors_file/errors_p_b.txt"
CheckIfFileExists "./tests/unittests/data/save/licenses_file/licenses_p_a.txt"
CheckIfFileExists "./tests/unittests/data/save/licenses_file/licenses_p_b.txt"

CheckIfFileExists "./tests/unittests/test_1_configuration.py"
CheckIfFileExists "./tests/unittests/test_2_filters.py"
CheckIfFileExists "./tests/unittests/test_3_dependencies.py"
CheckIfFileExists "./tests/unittests/test_4_dependencies_with_exception.py"
CheckIfFileExists "./tests/unittests/test_5_downloads.py"
CheckIfFileExists "./tests/unittests/test_6_licenses.py"
CheckIfFileExists "./tests/unittests/test_7_save_the_licenses.py"
CheckIfFileExists "./tests/unittests/test_8_save_the_errors.py"

# Runtimes and tools
# ------------------

echo -e "\n-----------------------"
echo "Assertions for runtimes"
echo "-----------------------"

echo -e "\nCheck for Python3..."
CheckIfRuntimeExists "Python3" "python3.8 --version" "3.8.5"

echo -e "\nCheck for Python modules"
CheckIfPythonModuleInstalled "requests"
CheckIfPythonModuleInstalled "xmltodict"
CheckIfPythonModuleInstalled "pytest"
CheckIfPythonModuleInstalled "bs4"

# Integration tests
# -----------------

echo -e "\n------------------------------------------"
echo "Run of LicensesInventory integration tests"
echo "------------------------------------------"

echo -e "\nRunning integration tests (please, make several runs to test different user prompts)..."
read -p "✋ Press any key when you are ready"
python3.8 -m pytest -s ./tests/integrationtests/test_1_all_dependencies.py
python3.8 -m pytest -s ./tests/integrationtests/test_2_2_dependencies_per_platform_saving_licenses.py
python3.8 -m pytest -s ./tests/integrationtests/test_3_print_with_error_403.py
python3.8 -m pytest -s ./tests/integrationtests/test_4_2_dependencies_per_platform_saving_errors.py

# Unit tests
# ----------

echo -e "\n-----------------------------------"
echo "Run of LicensesInventory unit tests"
echo "-----------------------------------"

echo -e "\nRunning unit tests..."
python3.8 -m pytest ./tests/unittests/test_1_configuration.py
python3.8 -m pytest ./tests/unittests/test_2_filters.py
python3.8 -m pytest ./tests/unittests/test_3_dependencies.py
python3.8 -m pytest ./tests/unittests/test_4_dependencies_with_exception.py
python3.8 -m pytest ./tests/unittests/test_5_downloads.py
python3.8 -m pytest ./tests/unittests/test_6_licenses.py
python3.8 -m pytest ./tests/unittests/test_7_save_the_licenses.py
python3.8 -m pytest ./tests/unittests/test_8_save_the_errors.py

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
