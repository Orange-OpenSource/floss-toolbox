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

# Since...............: 08/03/2021
# Description.........: Make a dry-run of the project to check if everything is ready to use
# Version.............: 3.2.0

set -eu

BAD_SETUP=1

# Utils
# -----

# $1 - File name to test
CheckIfFileExists(){
    if [ ! -f "$1" ]; then
        echo "⛔  ERROR: The file '$1' does not exist"
        exit $BAD_SETUP
    else
        echo "✅  Cool! The file '$1' exists"
    fi
}

# $1 - Directory name to test
CheckIfDirectoryExists(){
    if [ ! -d "$1" ]; then
        echo "⛔  ERROR: The directory '$1' does not exist"
        exit $BAD_SETUP
    else
        echo "✅  Cool! The directory '$1' exists"    
    fi
}

# $1 - Target for dry run
RunDryRunInFolder(){
    target=$1
    CheckIfDirectoryExists $target
    CheckIfFileExists "$target/dry-run.sh"
    previousLocation=`pwd`
    cd "$target"
    ./dry-run.sh
    cd "$previousLocation"
}

# Diver features
# --------------

read -p "✋ Press any key to dry run DIVER module"

echo "---------------------------------"
echo "Assertions for the DIVER features"
echo "---------------------------------"

RunDryRunInFolder "diver"

# GitHub features
# ---------------

echo -e "\n"
read -p "✋ Press any key to dry run GITHUB module"

echo -e "\n----------------------------------"
echo "Assertions for the GITHUB features"
echo "----------------------------------"

RunDryRunInFolder "github"

# GitLab features
# ---------------

echo -e "\n"
read -p "✋ Press any key to dry run GITLAB module"

echo -e "\n----------------------------------"
echo "Assertions for the GITLAB features"
echo "----------------------------------"

RunDryRunInFolder "gitlab"

# Utils features
# --------------

echo -e "\n"
read -p "✋ Press any key to dry run utils features"

echo -e "\n---------------------------------"
echo "Assertions for the Utils features"
echo "---------------------------------"

RunDryRunInFolder "utils/text-generator"
RunDryRunInFolder "utils/third-party-generator"
RunDryRunInFolder "utils/reuse"

# Licenses Inventory tool
# -----------------------

echo -e "\n"
read -p "✋ Press any key to dry run LICENSES INVENTORY module"

echo -e "\n------------------------------------------"
echo "Assertions for the Licenses Inventory tool"
echo "------------------------------------------"

RunDryRunInFolder "LicensesInventory"

exit 0