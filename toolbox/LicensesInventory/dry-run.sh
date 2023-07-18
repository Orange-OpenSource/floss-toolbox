#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Since...............: 10/03/2023
# Description.........: Make a dry-run of the LicensesInventory module to check if everything is ready to use
# Version.............: 2.2.0

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

CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/complex/build.gradle"
CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/complex/go.mod"
CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/complex/package.json"
CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/complex/Package.swift"
CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/simple/build.gradle"
CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/simple/build.gradle.kts"
CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/simple/Cargo.lock"
CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/simple/go.mod"
CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/simple/package.json"
CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/simple/Package.swift"
CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/simple/Podfile"
CheckIfFileExists "./tests/integrationtests/data/get_the_dependencies/simple/pubspec.yaml"

CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/cargo_lock/adler.json"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/go_mod/emperror.dev_errors.html"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/gradle/androidannotations_github.json"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/gradle/appcompta_github.json"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/package_json/@babel_core.html"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/package_json/karma.html"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/package_swift/AliSoftware_OHHTTPStubs.html"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/package_swift/apple_swift_collections.html"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/package_swift/CocoaLumberjack_CocoaLumberjack_git.html"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/package_swift/krzyzanowskim_CryptoSwift_git.html"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/Podfile/AppleReachability.html"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/Podfile/ReachabilitySwift.html"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/Podfile/SwiftLint.html"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/results/pubspec_yaml/build_runner.html"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/sources/build.gradle"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/sources/Cargo.lock"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/sources/go.mod"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/sources/package.json"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/sources/Package.swift"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/sources/Podfile"
CheckIfFileExists "./tests/integrationtests/data/get_the_licenses/sources/pubspec.yaml"
CheckIfFileExists "./tests/integrationtests/data/config_empty.ini"
CheckIfFileExists "./tests/integrationtests/data/config_no_file.ini"
CheckIfFileExists "./tests/integrationtests/data/config_no_path_licenses.ini"
CheckIfFileExists "./tests/integrationtests/data/config_no_path_to_parse.ini"
CheckIfFileExists "./tests/integrationtests/data/config.ini"

CheckIfFileExists "./tests/integrationtests/test_configuration.py"
CheckIfFileExists "./tests/integrationtests/test_dependencies.py"
CheckIfFileExists "./tests/integrationtests/test_downloads.py"
CheckIfFileExists "./tests/integrationtests/test_licenses.py"

echo -e "\nCheck other files"

CheckIfFileExists "./README.md"
CheckIfFileExists "./THIRD-PARTY.txt"
CheckIfDirectoryExists "./licenses"
CheckIfFileExists "./licenses/LICENSE-beautifulsoup.txt"
CheckIfFileExists "./licenses/LICENSE-pytest.txt"
CheckIfFileExists "./licenses/LICENSE-requests.txt"
CheckIfFileExists "./licenses/LICENSE-xmltodict.txt"

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
CheckIfPythonModuleInstalled "bs4"

# Units tests
# -----------

echo -e "\n----------------------------------"
echo "Run of LicensesInventory unit test"
echo "----------------------------------"

echo -e "\nRunning integration tests..."
python3 -m pytest ./tests/integrationtests/*.py

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
