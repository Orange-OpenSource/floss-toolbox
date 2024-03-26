#!/usr/bin/env ruby
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

require 'optparse'
require 'set'

VERSION = "1.0.0"

CONFORM_FILES_FILE = "data/conform-files.txt"
NOT_CONFORM_FILES_FILE = "data/not-conform-files.txt"

# ---------
# Functions
# ---------

$arguments = {}
$arguments[:debug] = false

# Just for debugging
def debug(message)
    STDOUT.puts message if $arguments[:debug]
end

# To update log files
def log(data, file)
    File.open(file, 'w') do |logfile|
        data.each { |entry| logfile.puts(entry.chomp) }
    end
end

# Forges a new file as a decorated version of a given file using some symbols to add
#
# @param path [String] The path to the file to be copy and create a new version but decorated.
# @param append_to_top [String] The string to append to the top of the file.
# @param prepend_to_each_line [String] The string to prepend to each line in the file.
# @param append_to_end [String] The string to append to the end of the file.
# @return [String] The path of the decorated file
def decorated_template(path, extension, append_to_top, prepend_to_each_line, append_to_end)
    modified_path = "#{path}#{extension}"
    File.open(path, 'r') do |original_file|
      File.open(modified_path, 'w') do |modified_file|
        modified_file.puts(append_to_top)
        original_file.each_line do |line|
          modified_file.puts(prepend_to_each_line + line.chomp)
        end
        modified_file.puts(append_to_end)
      end
    end
    return modified_path
end

# In given folder look for all files with given extension and check if eahc file contains the decorated text
#
# @param path [String] The path to the dirctory to process
# @param template [String] Path to the template file to look for
# @param conform_files [Array] Array updated between calls containing all conform files
# @param not_conform_files [Array] Array updated between calls containing all not conform files
# @param extension [String] The extension of sources files to check
# @param append_to_top [String] The string to append to the top of the file.
# @param prepend_to_each_line [String] The string to prepend to each line in the file.
# @param append_to_end [String] The string to append to the end of the file.
# @return [Int] Number of iterated files
def check_for_sources(path, template, conform_files, not_conform_files, extension, append_to_top, prepend_to_each_line, append_to_end)
    sources_files = Dir.glob("#{path}/**/*#{extension}")
    markup = extension.upcase
    if sources_files.length == 0
        debug("ℹ️   Did not find any #{extension} file, won't check for given rules")
        return 0
    end
    debug("ℹ️   Found #{sources_files.length} #{extension} files")
    decorated_template = decorated_template(template, markup, append_to_top, prepend_to_each_line, append_to_end)
    decorated_template_content = File.read(decorated_template)
    sources_files.each do |source_file|
        source_file_content = File.read(source_file)
        if source_file_content.start_with?(decorated_template_content) # Or maybe "contains" to get rid of shebang and or env definitions?
            debug("✅  #{source_file} starts with the template")
            conform_files << source_file
            not_conform_files.delete(source_file)
        else
            debug("❌  #{source_file} does not start with template")
            unless conform_files.include?(source_file)
                not_conform_files << source_file
            end
        end
    end
    return sources_files.length
end

# ------------------
# 1) Check arguments
# ------------------

OptionParser.new do |parameters|
    parameters.banner = "Usage: ruby #{__FILE__}"
    parameters.on("-f", "--folder FOLDER", String, "Path to folder to check") do |argument|
        unless argument.to_s.strip.empty?
            $arguments[:folder], $arguments[:template] = argument
        end
    end
    parameters.on("-t", "--template FILE", String, "Path to file containing header text without language decoration") do |argument|
        unless argument.to_s.strip.empty?
            $arguments[:template] = argument
        end
    end
    parameters.on("-d", "--debug", "Display more debug traces") do |argument|
        $arguments[:debug] = true
    end
    parameters.on("-v", "--version", "Prints the version of this software") do
        puts VERSION
        exit
    end
    parameters.on("-h", "--help", "Prints this help") do
        puts parameters
        exit
    end
end.parse!

if $arguments.key?(:folder) == false || $arguments.key?(:template) == false
    STDERR.puts "Missing parameters"
    STDERR.puts "Usage: ruby #{__FILE__} --help"
    abort
end

if !File.directory?($arguments[:folder])
    STDERR.puts "Error: Folder is not a directory"
end

if !File.exist?($arguments[:template])
    STDERR.puts "Error: Template file is not a file"
end

STDOUT.puts "🆗  Ok, will iterate on each source file inside '#{$arguments[:folder]}' looking for template at '#{$arguments[:template]}'"

# -----------------------
# 2) Process source files
# -----------------------

conform_files = Set.new
not_conform_files = Set.new
n = 0

# Define the rules you want to accept for each programming language.
# Do not forget several comments symbols can be used for one language.
# For intermediate or closing symbols, some additional whitespaces can be added to have things vertically aligned.

# C / C++ - With additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".c",  "/*", " * ", " */")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".cpp",  "/*", " * ", " */")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".h",  "/*", " * ", " */")

# C / C++ - Without additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".c",  "/*", "*", "*/")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".cpp",  "/*", "*", "*/")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".h",  "/*", "*", "*/")

# C# 
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".cs",  "//", "// ", "//")

# CSS - With additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".css",  "/*", " * ", " */")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".css",  "/**", " * ", " */")

# CSS - Without additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".css",  "/*", "*", "*/")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".css",  "/**", "*", "*/")

# Dart
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".dart",  "//", "// ", "//")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".dart",  "/*", " * ", " */")

# Elm
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".elm",  "--", "-- ", "--")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".elm",  "{-", "   ", "-}")

# Fortran
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".FOR",  "C", "C ", "C")

# Go - With additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".go",  "//", "// ", "//")

# Go - Without additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".go",  "//", "//", "//")

# Groovy - With additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".groovy",  "//", "// ", "//")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".groovy",  "/**", " * ", " */")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".groovy",  "/*", " * ", " */")

# HTML - With additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".html",  "<!--", " ", "-->")

# HTML - Without additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".html",  "<!--", "", "-->")

# Java - With additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".java",  "//", "// ", "//")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".java",  "/**", " * ", " */")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".java",  "/*", " * ", " */")

# JavaScript - With additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".cjs",  "//", "// ", "//")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".js",  "//", "// ", "//")

# JavaScript - Without additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".cjs",  "//", "//", "//")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".js",  "//", "//", "//")

# Kotlin - With additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".kt",  "/*", " * ", " */")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".kt",  "//", "// ", "//")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".kts",  "/*", " * ", " */")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".kts",  "//", "// ", "//")

# Lua
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".lua",  "--", "-- ", "--")

# Objective-C
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".m",  "//", "// ", "//")

# Objective-C - With additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".m",  "/*", " * ", " */")

# Objective-C - Without additional whitespaces
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".m",  "/*", "*", "*/")

# PHP
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".php",  "//", "// ", "//")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".php",  "/*", " * ", " */")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".php",  "#", "# ", "#")

# Python
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".py",  "#", "# ", "#")

# R
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".R",  "#", "# ", "#")

# Ruby
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".rb",  "#", "# ", "#")

# Rust
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".rs",  "/*", " * ", " */")

# Shell
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".sh",  "#", "# ", "#")

# Swift
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".swift",  "//", "// ", "//")

# TypeScript
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".ts",  "//", "// ", "//")
n += check_for_sources($arguments[:folder], $arguments[:template], conform_files, not_conform_files, ".tsx",  "//", "// ", "//")

# ----------
# 3) Results
# ----------

STDOUT.puts "🗒️   Dumping logs in '#{NOT_CONFORM_FILES_FILE}' and '#{CONFORM_FILES_FILE}' files"
log(not_conform_files, NOT_CONFORM_FILES_FILE)
log(conform_files, CONFORM_FILES_FILE)

number_of_files = Dir[File.join($arguments[:folder], '**', '*')].count { |file| File.file?(file) }
STDOUT.puts "💪  Made #{n} controls"
STDOUT.puts "👉  There are #{conform_files.length} unique files (out of #{number_of_files}) where template has been found"
STDOUT.puts "👉  There are #{not_conform_files.length} unique files (out of #{number_of_files}) where template was not found"

# TODO: Compute comptuation time
# NOTE/ Template : no remaining space nor empty lines
