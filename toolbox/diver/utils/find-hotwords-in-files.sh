#!/bin/bash
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Version.............: 1.2.0
# Since...............: 11/05/2020
# Description.........: Looks for words in a directory's files (credentials, names, email addresses, whatever you want)
#
# Usage: bash find-hotwords-in-files.sh --words path/to/words/file --directory path/to/project
#

VERSION="1.2.0"
SCRIPT_NAME="find-hotwords-in-files"

# -------------
# Configuration
# -------------

# Exits immediately if:
# - any command has non-zero exit status (-e)
# - undefined variable in use (-u)
# and do not mask errors in pipelines (-o pipefail)
set -euo pipefail

NORMAL_EXIT_CODE=0
BAD_ARGUMENTS_EXIT_CODE=1
BAD_PARAMETERS_EXIT_CODE=2

# Prefix for generated files
GENERATED_FILES_PREFIX="$$-hotwords"

# Folder fo generated files
TEMP_FOLDER="./data"

# File listing the files which have not been processed
UNCHECKED_FILE="$TEMP_FOLDER/$GENERATED_FILES_PREFIX-unchecked-files.txt"

# File listing the files which have words hits
HITS_FILE="$TEMP_FOLDER/$GENERATED_FILES_PREFIX-files-hits.txt"

# Report file with metrics
REPORT_METRIC_FILE="$TEMP_FOLDER/$GENERATED_FILES_PREFIX-report.txt"

# ---------
# Functions
# ---------

# \fn DisplayUsages
# \brief Displays an help message and exists
DisplayUsages(){
    echo "***************************************"
    echo "$SCRIPT_NAME - Version $VERSION"
    echo "***************************************"
    echo "USAGE:"
    echo "bash $SCRIPT_NAME.sh --help"
    echo "bash $SCRIPT_NAME.sh --words WORDS --directory TARGET"
    echo -e "\t --words.........: Path to file containing words seperated by ; and line break"
    echo -e "\t --directory.....: Path to target folder to analyse"
}

# \fn NormalExit
# \brief Exits with NORMAL_EXIT_CODE code
NormalExit(){
    exit $NORMAL_EXIT_CODE
}

# \fn BadArgumentsExit
# \brief Exits with BAD_ARGUMENTS_EXIT_CODE code
BadArgumentsExit(){
    exit $BAD_ARGUMENTS_EXIT_CODE
}

# \fn BadParametersExit
# \brief Exits with BAD_PARAMETERS_EXIT_CODE code
BadParametersExit(){
    exit $BAD_PARAMETERS_EXIT_CODE
}

# \fn ReadWordsFromFile
# \brief Returns words separated by ; and \n in the given file assuming it's defined and readable
# \param The path to the file to proces
ReadWordsFromFile() {
    words_file=$1
    tr ';' '\n' < $words_file
}

# \fn CleanText
# \brief Convert the given text (word, text of file) (must be defined) in lower case (but keep special characters)
# \param The content to convert in lower case
CleanText() {
    echo "$1" | tr '[:upper:]' '[:lower:]'
}

# \fn PrepareFiles
# \brief If existing removes the work files and then creates them
PrepareFiles() {
    if [ -f $UNCHECKED_FILE ]; then
        rm $UNCHECKED_FILE
    fi
    touch $UNCHECKED_FILE
    if [ -f $HITS_FILE ]; then
        rm $HITS_FILE
    fi
    touch $HITS_FILE
    if [ -f $REPORT_METRIC_FILE ]; then
        rm $REPORT_METRIC_FILE
    fi
    touch $REPORT_METRIC_FILE
}

# \fn LogUncheckedFile
# \brief Logs in UNCHECKED_FILE an unchecked file given in parameter (must be defined)
# \param The file path/name to log
LogUncheckedFile() {
    echo "$1" >> $UNCHECKED_FILE
}

# \fn LogWordHitForFile
# \brief Logs in HITS_FILE the found word ($1) in the given extract ($2) in the given file ($3), parameters must be defined
# \param The word
# \param The index / location number (e.g. $2-th word in the file)
# \param Extract of the text where the word has been found
# \param The file where the word has been found
LogWordHitForFile() {
    echo -e "\n[ENTRY]" >> $HITS_FILE
    echo -e "Word........:\t $1" >> $HITS_FILE
    echo -e "File........:\t $4" >> $HITS_FILE
    echo -e "Index.......:\t $2" >> $HITS_FILE
    echo -e "Extract.....:\t $3" >> $HITS_FILE
}

# ----------------
# Step 0 - Prepare
# ----------------

# Check the args numbers and display usage if needed
if [ "$#" -ne 4 ]; then
	DisplayUsages
    NormalExit
# Need some help?
elif [ "$1" = "--help" ]; then
	DisplayUsages
    NormalExit
fi

# Get words file
if [ "$1" = "--words"  ]; then
    if [ "$2" ]; then
	    words_file=$2
    else
        DisplayUsages
        BadArgumentsExit
    fi
else
    DisplayUsages
    BadArgumentsExit
fi

# Get project folder
if [ "$3" = "--directory"  ]; then
    if [ "$4" ]; then
	    project_folder=$4
    else
        DisplayUsages
        BadArgumentsExit
    fi
else
    DisplayUsages
    BadArgumentsExit
fi

# Test if words file and project to analyse exist and are readable
if [ ! -f "$words_file" ]; then
    echo "💥 $SCRIPT_NAME - Error: $worlds_file is not a file to process"
    BadArgumentsExit
fi

if [ ! -r "$words_file" ]; then
    echo "⛔ $SCRIPT_NAME - Error: $worlds_file file cannot be read"
    BadArgumentsExit
fi

if [ ! -d "$project_folder" ]; then
    echo "💥 $SCRIPT_NAME - Error: $project_folder is not a directory to analyse"
    BadArgumentsExit
fi

if [ ! -r "$project_folder" ]; then
    echo "⛔ $SCRIPT_NAME - Error: $project_folder folder cannot be read"
    BadArgumentsExit
fi

# Run!
SECONDS=0

echo "***************************************"
echo "$SCRIPT_NAME - Version $VERSION"
echo "***************************************"

echo -e "\n"

echo "📋 File of words is $words_file"
echo "📋 Project to analyse is $project_folder"

echo "📋 Prepare logs"
PrepareFiles

echo -e "\n"

# -------------------------------------
# Step 1 - Read data files to get words
# -------------------------------------

echo "🍥 Reading words in $words_file..."
words=$( ReadWordsFromFile $words_file )
words_count=`echo $words | wc -w`

# ----------------------------
# Step 2 - Read target project
# ----------------------------

echo "🍥 Reading files in $project_folder..."
echo -e "\n"

for project_file in `find "$project_folder" -type f`; do

    # Process only text files, no binaries
    file_mime_type=`file -b --mime-type "$project_file" | sed 's|/.*||'`
    if [ "$file_mime_type" = "text" ]; then

        echo "🍥 Process file $project_file"

        # ------------------------------------------------------------------------------
        # Step 4 - For each line of each file and for each word, check if words are used
        # ------------------------------------------------------------------------------

        while read -r word; do

            word=$( CleanText $word )
            echo "🔎 Analyse file $project_file with word $word"

            word_location_count=0
            for raw_project_file_line in `cat $project_file`; do

                word_location_count=$(($word_location_count + 1))
                clean_project_file_line=$( CleanText $raw_project_file_line )
                search_results=`echo $clean_project_file_line | grep $word || true` 

                if [ "$search_results" ]; then

                    echo "🥳 👉 Woop woop! The word '$word' has been found at index $word_location_count in the file $project_file"

                    # -------------------------------------------------
                    # Step 5 - Write report with file - location - word
                    # -------------------------------------------------

                    LogWordHitForFile "$word" "$word_location_count" "$search_results"  "$project_file"

                fi

            done

        done < <(echo "$words")
    
    else
        echo "🚨 Warning: The file '$project_file' is not a text file, will skip it"
        echo "$project_file" >> $UNCHECKED_FILE
    fi
    
done

echo -e "\n👌 All files have been processed\n"

# ------------------------------------------------------------
# Step 6 - Metrics (words and files counts, hits, duration...)
# ------------------------------------------------------------

echo "📈 Count of words to look for.......: $words_count" >> $REPORT_METRIC_FILE
unchecked_files_count=`cat $UNCHECKED_FILE | wc -l`
echo "📈 Count of unchecked files.........: $unchecked_files_count" >> $REPORT_METRIC_FILE
files_hits_count=`cat $HITS_FILE | grep ENTRY | wc -l`
echo "📈 Count of hits....................: $files_hits_count" >> $REPORT_METRIC_FILE

script_duration=$SECONDS
echo "📈 Elapsed time.....................: $(($script_duration / 60))' $(($script_duration % 60))''" >> $REPORT_METRIC_FILE

# The end!

echo "Reports available in $REPORT_METRIC_FILE:"
cat $REPORT_METRIC_FILE

echo -e "\nFiles hits are listed here: $HITS_FILE"

echo -e "\nEnd of $SCRIPT_NAME\n"
NormalExit