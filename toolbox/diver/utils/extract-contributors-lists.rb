#!/usr/bin/env ruby
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2021 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Version.............: 1.0.0
# Since...............: 06/10/2021
# Description.........: Extracts from the LOG_FILE contributors (authors).
# Use the principle the LOG_FILE is a temporary file containing results of `git log` command.
# Will split the massive log into a bunch of small commits logs using "commit" word delimiter.
#
# Usage: ruby extract-contributors-lists.rb.rb LOGS_FILE
#

require 'set'

VERSION = "1.0.0"

DEBUG = false
COMMIT_DELIMITER = "commit" 
AUTHOR_PATTERN = "Author:"

# ---------
# Functions
# ---------

# Displays the usage of the script
def usage()
    STDOUT.puts "USAGE: ruby extract-contributors-lists.rb LOGS_FILE"
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

# Extracts from the commit bundle the hash.
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

if ARGV.length != 1
    error "ERROR: Expected only 1 argument"
    usage
    exit
end

git_log_file = ARGV[0]

# ---------------
# Check arguments
# ---------------

debug "Should process commits in log file '#{git_log_file}' with delimiter '#{COMMIT_DELIMITER}'"

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

debug "Will process commits in log file '#{git_log_file}' with delimiter '#{COMMIT_DELIMITER}'"

# --------------
# Processes file
# --------------

git_log_file_splits = File.read(git_log_file).split(COMMIT_DELIMITER)

# ---------------
# Process commits
# ---------------

unique_contributors = Set.new

# We assume each commit message looks like:
#            
#   commit abcdefghijklmnopqrstuvwxyz
#   Author: Foo Bar <foo.bar@wizz.bzh>
#   Date:   Thu Aug 8 13:37:42 2012 +0000
# 
#       chore: #0 - did things
#       ...
#       
#       Signed-off-by: Foo Bar <foo.bar@wizz.bzh>
#       

git_log_file_splits.each do |commit|
   
    unless commit.nil? || commit.length <= 0
        
        commit_hash = extract_commit_hash commit
        commit_downcase = commit.downcase

        # -----------------------
        # Looks for author fields
        # -----------------------

        author_pattern_downcase = AUTHOR_PATTERN.downcase

        # Check if author field is available for this commit
        if commit_downcase.include? author_pattern_downcase

            # Extract the author name:
            # 1 - cut the commit message with the "author symbol" 
            # 2 - keep the next part (following text, "on the right")
            # 3 - cut using '\n' with devides each commit message line and keep the first
            # 4 - remove useless caracters like spaces
            commit_author_raw_split = commit_downcase.split(author_pattern_downcase)
            commit_author_split_right_part = commit_author_raw_split[1]
            commit_author_split_right_part_top_line = commit_author_split_right_part.split("\n")[0]
            commit_author = commit_author_split_right_part_top_line.strip

            if commit_author.length <= 0
                debug "Undefined author value for commit '#{commit_hash}'"
            else
                #log "@@@ FOUND: '#{commit_author}'"
                unique_contributors << commit_author
            end

        end

    end # End of unless commit.nil? || commit.length <= 0

end # End of git_log_file_splits.each do |commit|

# ---------------------------
# Process unique contributors
# ---------------------------

# Just print constibutors in output, assuming the Shell wrapper will pack results in a file
unique_contributors.each do |contributor|
    log contributor
end