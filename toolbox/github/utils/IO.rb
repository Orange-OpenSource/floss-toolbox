# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

require_relative 'configuration.rb'
require 'fileutils'

##
# Ruby module providing methods for reading and writing content from/to files.
# Version: 1.0.0
module FileManager

    ##
    # Write each member attributes separated by ';' in file using this file name, in "w" mode.
    # Members are in hash returned by Octokit / GitHub API and fields are directly called from items.
    # +members+:: The group of members to write in file(login, name, email, url)
    # +file_name+:: The name of the file to use
    def self.write_members_in_permanent_file(members, file_name)
        dirname = "./#{$OUTPUT_DIRECTORY_NAME}"
        if File.directory?(dirname) == false
            FileUtils.mkdir_p(dirname)
        end
        File.open("./#{$OUTPUT_DIRECTORY_NAME}/#{file_name}", "w") do |file|
            file.write "login;name;email;url;\n"
            members.each { |member|
                file.write "#{member.login};"
                file.write "#{member.name};"
                file.write "#{member.email};"
                file.write "#{member.html_url};\n"
            }
        end
    end

    ##
    # Write each member attributes separated by ';' in file using this file name, in "w" mode.
    # Members are in array.
    # +members+:: The group of members to write in file (login, name, email, url)
    # +file_name+:: The name of the file to use
    def self.write_members_array_in_permanent_file(members, file_name)
        dirname = "./#{$OUTPUT_DIRECTORY_NAME}"
        if File.directory?(dirname) == false
            FileUtils.mkdir_p(dirname)
        end
        File.open("./#{$OUTPUT_DIRECTORY_NAME}/#{file_name}", "w") do |file|
            file.write "login;name;email;url;\n"
            members.each { |member|
                file.write "#{member["login"]};"
                file.write "#{member["name"]};"
                file.write "#{member["email"]};"
                file.write "#{member["url"]};\n"
            }
        end
    end

    ##
    # Write some project attributes separated by ';' in file using this file name, in "w" mode.
    # Projects are in array.
    # +projects+:: The group of projects to write in file (name and url)
    # +file_name+:: The name of the file to use
    def self.write_projects_in_permanent_file(projects, file_name)
        dirname = "./#{$OUTPUT_DIRECTORY_NAME}"
        if File.directory?(dirname) == false
            FileUtils.mkdir_p(dirname)
        end
        File.open("./#{$OUTPUT_DIRECTORY_NAME}/#{file_name}", "w") do |file|
            file.write "name;url;\n"
            projects.each { |project|
                file.write "#{project["name"]};"
                file.write "#{project["url"]};\n"
            }
        end
    end

    ##
    # Write projects attributes separated by ';' in file using this file name, in "w" mode, and adds more details.
    # Expects to have entries with names: name, url, LICENSE, README, THIRD-PARTY, AUTHORS
    # Projects are in array.
    # +projects+:: The group of projects to write in file (name, fulllname and url)
    # +file_name+:: The name of the file to use
    def self.write_unconform_projects_in_permanent_file(projects, file_name)
        dirname = "./#{$OUTPUT_DIRECTORY_NAME}"
        if File.directory?(dirname) == false
            FileUtils.mkdir_p(dirname)
        end
        File.open("./#{$OUTPUT_DIRECTORY_NAME}/#{file_name}", "w") do |file|
            file.write "name;url;LICENSE;README;THIRD-PARTY;AUTHORS;\n"
            projects.each { |project|
                file.write "#{project["name"]};"
                file.write "#{project["url"]};"
                file.write "#{project["LICENSE"]};"
                file.write "#{project["README"]};"
                file.write "#{project["THIRD-PARTY"]};"
                file.write "#{project["AUTHORS"]};\n"
            }
        end
    end

end

##
# Ruby module providing methods for logs
# Version: 1.0.0
module Log

    ##
    # Writes in standard output the given message
    # +message+:: The text to write
    def self.log(message)
        unless message.empty?
            puts message
        end
    end

    ##
    # Writes in error output the given message with the DEBUG: prefix
    # +message+:: The text to write
    def self.debug(message)
        if !message.empty? && $LOG_DEBUG
            STDERR.puts "DEBUG: %s" % message
        end
    end

    ##
    # Writes in error output the given message with the WARNING: prefix
    # +message+:: The text to write
    def self.warning(message)
        unless message.empty?
            STDERR.puts "WARNING: %s" % message
        end
    end

    ##
    # Writes in error output the given message with the ERROR: prefix
    # +message+:: The text to write
    def self.error(message)
        unless message.empty?
            STDERR.puts "ERROR: %s" % message
        end
    end

end