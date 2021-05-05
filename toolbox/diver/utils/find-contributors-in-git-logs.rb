#!/usr/bin/env ruby
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2021 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Version.............: 1.0.0
# Since...............: 11/05/2020
# Description.........: Checks if the LOG_FILE if words in WORDS_FILE exist or not.
# Use the principle the LOG_FILE is a temporary file containg results of `git log` command.
# Will split the massive log into a bunch of small commits logs using "commit" word delimiter.
# Use the principle the WORDS_FILE contains word seperated by ';' and line break.
#
# Usage: ruby find-contributors-in-git-logs.rb WORDS_FILE LOGS_FILE"
#

VERSION = "1.0.0"

DEBUG = false
COMMIT_DELIMITER = "commit" 

# ---------
# Functions
# ---------

# Displays the usage of the script
def usage()
    STDOUT.puts "USAGE: ruby find-contributors-in-git-logs.rb WORDS_FILE LOGS_FILE"
end

# Logs a message in standard output
# @param message The message to log
# 
def log(message)
    STDOUT.puts message
end

# Logs a message in error output
# @param message The message to log
#
def error(message)
    STDERR.puts message
end

# Logs a message in standard output if DEBUG flag is set to true
# @param message The message to log
def debug(message)
    if DEBUG
        log message
    end
end

# Extractssfrom the commit bundle the hash.
# Assumes the bundle is a whole commit log and the hash is in the first line.
# @param commit The commit bundle to parse
# @return The commit hash
def extract_commit_hash(commit)
    return commit.lines.first.strip!
end

# -------------
# Get arguments
# -------------

if ARGV.length == 1 && ARGV[0] == "--help"
    usage
    exit
end

if ARGV.length == 1 && ARGV[0] == "--version"
    log "VERSION: #{VERSION}"
    exit
end

if ARGV.length != 2
    error "ERROR: Expected only 2 arguments"
    usage
    exit
end

words_file = ARGV[0]
git_log_file = ARGV[1]

# ---------------
# Check arguments
# ---------------

debug "Should process words of file '#{words_file}' for log file '#{git_log_file}' with delimiter  '#{COMMIT_DELIMITER}'"

if words_file.to_s.empty?
    error "The file to use '#{words_file}' is not defined"
    exit
end

if !File.exist?(words_file)
    error "The file to use '#{words_file}' does not exist"
    exit
end

if !File.file?(words_file)
    error "The object at '#{words_file}' is not a file"
    exit
end

if git_log_file.to_s.empty?
    error "The file to use '#{git_log_file}' is not defined"
    exit
end

if !File.exist?(git_log_file)
    error "The file to use '#{git_log_file}' does not exist"
    exit
end

if !File.file?(git_log_file)
    error "The object at '#{git_log_file}' is not a file"
    exit
end

debug "Will process words of file '#{words_file}' for log file '#{git_log_file}' with delimiter  '#{COMMIT_DELIMITER}'"

# ---------------
# Processes files
# -----------

git_log_file_splits = File.read(git_log_file).split(COMMIT_DELIMITER)

words_file_splits = File.read(words_file).split(/[\n;]/)

# --------------------------------
# Process commits splits and words
# --------------------------------

git_log_file_splits.each do |commit|
   
    words_file_splits.each do |word|

        if commit.downcase.include? word.downcase
            commit_hash = extract_commit_hash commit
            log "Hit for commit '#{commit_hash}' with word '#{word}'"
        end

    end

end
