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

require 'git'
require_relative 'IO.rb'

##
# Ruby module providing a quite small and simple wrapper for the Git API.
# Allows to clone Git repositories.
# Version: 1.0.0
#
# Written with Git version 1.8.1
#
# More details about Git gem:
# - https://github.com/ruby-git/ruby-git
module GitWrapper

    ##
    # Clones the Git repository using the given SSH URL
    # +ssh_url+:: The SSH URL to use to clone the repository
    # +fodler_name+:: The name of the folder for the clone
    def self.clone_git_repository(ssh_url, folder_name)
        if ssh_url.nil? || ssh_url.empty?
           Log.error "SSH URL is not defined, imposible to clone Git repository. Returns now." 
           return
        end
        if folder_name.nil? || folder_name.empty?
            Log.error "Forlder for repository cloning is not defined, clone won't be done. Returns now." 
            return
        end
        Log.log "Clone Git repository using SSH URL '%s' under name '%s'" % [ssh_url, folder_name]
        Git.clone(ssh_url, folder_name)
    end

end
