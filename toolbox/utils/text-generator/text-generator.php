#!/usr/bin/env php
<?php
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

# Since...............: 29/02/2024
# Description.........: Generates a text based on a template and a list of variables to replace
# Version.............: 1.0.0

// -------------
// Configuration
// -------------

// Script version
$VERSION = "1.0.0";

// Error codes
$EXIT_OK = 0;
$ERROR_BAD_ARGUMENTS = 1;
$ERROR_BAD_ARGUMENT_TEMPLATE = 2;
$ERROR_BAD_ARGUMENT_VARIABLES = 3;
$ERROR_MISSING_VARIABLE_VALUE = 4;
$ERROR_DURING_OUTPUT = 5;

$VARIABLE_PREFIX = "%";
$VARIABLE_SUFFIX = "%";

$TEXT_FILE_OUTPUT_SUFFIX = ".result";

// ---------------
// Check arguments
// ---------------

echo "$argv[0] - Version $VERSION".PHP_EOL;

if ($argc != 3) {
    echo "Usage: text-generator.php TEMPLATE VALUES.php".PHP_EOL;
    echo "Error: Bad arguments, two are required, and not $argc".PHP_EOL;
    exit($ERROR_BAD_ARGUMENTS);
}

// --------------------------
// Get template and variables
// --------------------------

$template_file = $argv[1];
if (!file_exists($template_file)) {
    echo "Error: The argument '$template_file' is not a file".PHP_EOL;
    exit($ERROR_BAD_ARGUMENT_TEMPLATE);
}

$variables_file = $argv[2];
if (!file_exists($variables_file)) {
    echo "Error: The argument '$variables_file' is not a file".PHP_EOL;
    exit($ERROR_BAD_ARGUMENT_VARIABLES);
}

echo "Will use template at '$template_file' and replace all values using '$variables_file' file".PHP_EOL;
$text = file_get_contents($template_file);
$variables = parse_ini_file($variables_file);

// ---------------------------------------
// Replace in template variables by values
// ---------------------------------------

$newText = $text;
foreach($variables as $key => $value) {
    if ($value !== "") {
        echo "Replacing all occurences of '$key' by '$value'".PHP_EOL;
        $newText = str_replace($VARIABLE_PREFIX . $key . $VARIABLE_SUFFIX, $value, $newText);        
    } else {
        echo "Error: No value associated to key '$key'".PHP_EOL;
        exit($ERROR_MISSING_VARIABLE_VALUE);
    }
}

// ------
// Output
// ------

$destinationName = "$template_file" . $TEXT_FILE_OUTPUT_SUFFIX;
$writeResult = file_put_contents("$template_file.result", $newText);
if (!$writeResult) {
    echo "Error: Something wrong occured during writing process".PHP_EOL;
    exit($ERROR_DURING_OUTPUT);
} else {
    echo "The final file has been created / update at '$destinationName'".PHP_EOL;
    exit($EXIT_OK);
}
?>
