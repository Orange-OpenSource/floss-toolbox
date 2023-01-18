#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Since...............: 08/03/2021
# Description.........:  Make a dry-run of the project to check if everything is ready to use
# Version.............: 2.00

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

echo -e "\nCheck if main folder exists..."
CheckIfDirectoryExists "diver"

echo -e "\nCheck scripts..."
CheckIfFileExists "diver/extract-emails-from-history.sh"
CheckIfFileExists "diver/find-contributors-in-files.sh"
CheckIfFileExists "diver/find-contributors-in-git-logs.sh"
CheckIfFileExists "diver/find-credentials-in-files.sh"
CheckIfFileExists "diver/find-credits-in-files.sh"
CheckIfFileExists "diver/find-missing-developers-in-git-commits.sh"
CheckIfFileExists "diver/list-contributors-in-history.sh"

echo -e "\nCheck utilitary scripts..."
CheckIfFileExists "diver/utils/extract-contributors-lists.rb"
CheckIfFileExists "diver/utils/find-contributors-in-git-logs.rb"
CheckIfFileExists "diver/utils/find-hotwords-in-files.sh"
CheckIfFileExists "diver/utils/find-missing-developers-in-git-commits.rb"

echo -e "\nCheck for generated files folder..."
CheckIfDirectoryExists "diver/data"

# GitHub features
# ---------------

echo -e "\n----------------------------------"
echo "Assertions for the GITHUB features"
echo "----------------------------------"

echo -e "\nCheck if main folder exists..."
CheckIfDirectoryExists "github"

echo -e "\nCheck files..."
CheckIfFileExists "github/configuration.rb"
CheckIfFileExists "github/GitHubWizard.sh"

CheckIfFileExists "github/utils/check-leaks-from-github.sh"
CheckIfFileExists "github/utils/check-vulnerabilities-from-github.sh"
CheckIfFileExists "github/utils/count-leaks-nodes.py"
CheckIfFileExists "github/utils/count-vulnerabilities-nodes.py"
CheckIfFileExists "github/utils/dump-git-repositories-from-github.sh"
CheckIfFileExists "github/utils/extract-repos-field-from-json.py"
CheckIfFileExists "github/utils/GitHubFacade.rb"
CheckIfFileExists "github/utils/GitHubWrapper.rb"
CheckIfFileExists "github/utils/GitWrapper.rb"
CheckIfFileExists "github/utils/IO.rb"

# GitLab features
# ---------------

echo -e "\n----------------------------------"
echo "Assertions for the GITLAB features"
echo "----------------------------------"

echo -e "\nCheck if main folder exists..."
CheckIfDirectoryExists "gitlab"
CheckIfDirectoryExists "gitlab/data"

echo -e "\nCheck files..."
CheckIfFileExists "gitlab/configuration.rb"
CheckIfFileExists "gitlab/GitLabWizard.sh"
CheckIfFileExists "gitlab/utils/dump-git-repositories-from-gitlab.sh"
CheckIfFileExists "github/utils/extract-repos-field-from-json.py" # Stored in github folder but used by dump-git-repositories-from-gitlab.sh
CheckIfFileExists "github/utils/count-leaks-nodes.py" # Stored in github folder but used by check-leaks-from-gitlab.sh

# Licenses Inventory tool
# -----------------------

echo -e "\n------------------------------------------"
echo "Assertions for the Licenses Inventory tool"
echo "------------------------------------------"

echo -e "\nCheck if main foldesr exists..."
CheckIfDirectoryExists "LicensesInventory"
CheckIfDirectoryExists "LicensesInventory/sources"
CheckIfDirectoryExists "LicensesInventory/tests"

echo -e "\nCheck sources files..."
CheckIfFileExists "LicensesInventory/sources/common/__init__.py"
CheckIfFileExists "LicensesInventory/sources/common/datas.py"
CheckIfFileExists "LicensesInventory/sources/common/files.py"
CheckIfFileExists "LicensesInventory/sources/common/filters.py"
CheckIfFileExists "LicensesInventory/sources/common/names.py"
CheckIfFileExists "LicensesInventory/sources/configuration/__init__.py"
CheckIfFileExists "LicensesInventory/sources/configuration/config.py"
CheckIfFileExists "LicensesInventory/sources/dependencies/__init__.py"
CheckIfFileExists "LicensesInventory/sources/dependencies/dependencies.py"
CheckIfFileExists "LicensesInventory/sources/dependencies/parsings.py"
CheckIfFileExists "LicensesInventory/sources/search/__init__.py"
CheckIfFileExists "LicensesInventory/sources/search/downloads.py"
CheckIfFileExists "LicensesInventory/sources/search/parsings.py"
CheckIfFileExists "LicensesInventory/sources/search/search.py"
CheckIfFileExists "LicensesInventory/sources/__init__.py"
CheckIfFileExists "LicensesInventory/sources/main.py"
CheckIfFileExists "LicensesInventory/config.ini"

echo -e "\nCheck integration test files..."
CheckIfFileExists "LicensesInventory/tests/integrationtests/data/gradle/dependency_github.gradle"
CheckIfFileExists "LicensesInventory/tests/integrationtests/data/gradle/dependency_maven_central.gradle"
CheckIfFileExists "LicensesInventory/tests/integrationtests/data/gradle/license_github.json"
CheckIfFileExists "LicensesInventory/tests/integrationtests/data/gradle/license_maven_central.pom"
CheckIfFileExists "LicensesInventory/tests/integrationtests/data/gradle/version_maven_central.json"
CheckIfFileExists "LicensesInventory/tests/integrationtests/data/package_json/license_package_json.html"
CheckIfFileExists "LicensesInventory/tests/integrationtests/data/package_json/package.json"
CheckIfFileExists "LicensesInventory/tests/integrationtests/data/roast/Cargo.lock"
CheckIfFileExists "LicensesInventory/tests/integrationtests/data/config.ini"
CheckIfFileExists "LicensesInventory/tests/integrationtests/test_search.py"

echo -e "\nCheck unit test files..."
CheckIfFileExists "LicensesInventory/tests/unittests/data/config/config_no_data.ini"
CheckIfFileExists "LicensesInventory/tests/unittests/data/config/config.ini"
CheckIfFileExists "LicensesInventory/tests/unittests/data/get_content_by_name/my_gradle_file.txt"
CheckIfFileExists "LicensesInventory/tests/unittests/data/get_content_by_name/package.json"
CheckIfFileExists "LicensesInventory/tests/unittests/data/gradle/license_github.json"
CheckIfFileExists "LicensesInventory/tests/unittests/data/gradle/license_maven_central.pom"
CheckIfFileExists "LicensesInventory/tests/unittests/data/gradle/version.json"
CheckIfFileExists "LicensesInventory/tests/unittests/data/package_json/license_package_json.html"
CheckIfFileExists "LicensesInventory/tests/unittests/data/roast/license_roast.json"
CheckIfFileExists "LicensesInventory/tests/unittests/data/dependency_a.txt"
CheckIfFileExists "LicensesInventory/tests/unittests/data/dependency_b.txt"
CheckIfFileExists "LicensesInventory/tests/unittests/data/filename_by_name.test"
CheckIfFileExists "LicensesInventory/tests/unittests/data/files_read.txt"
CheckIfFileExists "LicensesInventory/tests/unittests/test_config.py"
CheckIfFileExists "LicensesInventory/tests/unittests/test_dependency.py"
CheckIfFileExists "LicensesInventory/tests/unittests/test_files_check_the_directory.py"
CheckIfFileExists "LicensesInventory/tests/unittests/test_files_get_the_filenames_by_name.py"
CheckIfFileExists "LicensesInventory/tests/unittests/test_files_write_and_read.py"
CheckIfFileExists "LicensesInventory/tests/unittests/test_filter.py"
CheckIfFileExists "LicensesInventory/tests/unittests/test_parsing_download.py"
CheckIfFileExists "LicensesInventory/tests/unittests/test_parsing.py"

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

echo -e "\nCheck for Python modules"
CheckIfPythonModuleInstalled "requests"
CheckIfPythonModuleInstalled "xmltodict"
CheckIfPythonModuleInstalled "pytest"

# Configuration file
# ------------------

echo -e "\n---------------------------------"
echo "Assertions for configuration file"
echo "---------------------------------"

echo -e "\nCheck for entries in configuration file..."

CheckIfConfigurationKeyDefined "github/configuration.rb" "GITHUB_PERSONAL_ACCESS_TOKEN"
CheckIfConfigurationKeyDefined "github/configuration.rb" "GITHUB_ORGANIZATION_NAME"
CheckIfConfigurationKeyDefined "github/configuration.rb" "GITHUB_ORGANIZATION_ADMINS"
CheckIfConfigurationKeyDefined "github/configuration.rb" "GIT_PROJECT_MANDATORY_FILES"
CheckIfConfigurationKeyDefined "github/configuration.rb" "REQUEST_DELAY_IN_SECONDS"
CheckIfConfigurationKeyDefined "github/configuration.rb" "RESULTS_PER_PAGE"
CheckIfConfigurationKeyDefined "github/configuration.rb" "EXPECTED_PAGE_COUNT"
CheckIfConfigurationKeyDefined "github/configuration.rb" "OUTPUT_DIRECTORY_NAME"
CheckIfConfigurationKeyDefined "github/configuration.rb" "FILENAME_MEMBERS"
CheckIfConfigurationKeyDefined "github/configuration.rb" "FILENAME_MEMBERS_2FA_DISABLED"
CheckIfConfigurationKeyDefined "github/configuration.rb" "FILENAME_MEMBERS_UNDEFINED_COMPANY"
CheckIfConfigurationKeyDefined "github/configuration.rb" "FILENAME_PROJECTS_WITHOUT_TEAM"
CheckIfConfigurationKeyDefined "github/configuration.rb" "FILENAME_USERS_WITH_BAD_EMAILS"
CheckIfConfigurationKeyDefined "github/configuration.rb" "FILENAME_USERS_WITH_BAD_FULLNAMES"
CheckIfConfigurationKeyDefined "github/configuration.rb" "FILENAME_PROJECTS_WITH_UNCONFORM_REPOSITORIES"
CheckIfConfigurationKeyDefined "github/configuration.rb" "FILENAME_PROJECTS_WITHOUT_LICENSES"
CheckIfConfigurationKeyDefined "github/configuration.rb" "FILENAME_EMPTY_PROJECTS"
CheckIfConfigurationKeyDefined "github/configuration.rb" "REPOSITORIES_CLONE_LOCATION_PATH"
CheckIfConfigurationKeyDefined "github/configuration.rb" "REPOSITORIES_CLONE_URL_JSON_KEY"
CheckIfConfigurationKeyDefined "github/configuration.rb" "EXCLUDE_GITHUB_ARCHIVED_PROJECTS_FOR_SCANS"

CheckIfConfigurationKeyDefined "gitlab/configuration.rb" "GILAB_PERSONAL_ACCESS_TOKEN"
CheckIfConfigurationKeyDefined "gitlab/configuration.rb" "GITLAB_ORGANIZATION_ID"
CheckIfConfigurationKeyDefined "gitlab/configuration.rb" "RESULTS_PER_PAGE"
CheckIfConfigurationKeyDefined "gitlab/configuration.rb" "REPOSITORIES_CLONE_LOCATION_PATH"
CheckIfConfigurationKeyDefined "gitlab/configuration.rb" "REPOSITORIES_CLONE_URL_JSON_KEY"

echo -e "🔎  I hope configuration entries are - well - defined, be sure of that"

# Units tests
# -----------

echo -e "\n----------------------------------"
echo "Run of LicensesInventory unit test"
echo "----------------------------------"

cd "LicensesInventory/"

echo -e "\nRunning integration tests..."
python3 -m pytest tests/integrationtests/*.py

echo -e "\nRunning unit tests..."
python3 -m pytest tests/unittests/*.py

cd ".."

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
