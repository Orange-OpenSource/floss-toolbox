# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

require_relative 'configuration.rb'
require 'fileutils'
require_relative 'GitWrapper.rb'
require_relative 'IO.rb'
require 'json'
require 'net/http'
require 'octokit'
require 'uri'

##
# Ruby module providing a quite small and simple wrapper for the GitHub API, here using only the Octokit library.
# Allows to request the GitHub project to help projects and teams management.
# Version: 1.0.0
#
# Written with Octokit version 4.20.0
#
# More details about Octokit:
# - https://octokit.github.io/octokit.rb/Octokit/
# - https://docs.github.com/en/rest/overview/libraries
# - https://github.com/octokit/octokit.rb
module GitHubWrapper

    # =======
    # Octokit
    # =======

    # Client definition
    # -----------------

    ##
    # Creates an +Octokit+ client using a GitHub personal access token (created using https://github.com/settings/tokens).
    # +personal_acces_token+:: Personal token to use to request GitHub API
    def self.create_octokit_client(personal_access_token)
        if personal_access_token.nil? || personal_access_token.empty?
            Log.error "GitHub personal access token is not defined. Imposible to create Octokit client. Returns now." 
            return
        end
        return Octokit::Client.new(:access_token => personal_access_token)
    end

    # Users
    # -----

    ##
    # Returns the current user based on the connection previously defined in the given Octokit client.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    def self.get_current_user(octokit_client)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
         end
        return octokit_client.user
    end

    ##
    # Returns details about the user with the given login.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +user_login+:: The login of the user to get details
    def self.get_user(octokit_client, user_login)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        if user_login.nil? || user_login.empty?
            #Log.error "User login is not defined. Impossible to get details about this user. Returns now." 
            return
        end
        return octokit_client.user(user_login)
    end

    ##
    # Display in standard output the current user based on the connection previously defined in the given Octokit client.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    def self.display_current_user_details(octokit_client)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        user = get_current_user(octokit_client)
        Log.log "Current user is: '%s' aka '%s' (%s)" % [user.name, user.login, user.html_url]
    end

    # Organizations
    # -------------

    ##
    # Returns the organization data using its name to find it and the Octokit client.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +organization_name+:: The name of the organization to retrieve from API
    def self.get_organization(octokit_client, organization_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        return octokit_client.org(organization_name)
    end

    ##
    # Display in standard output the organization details using the given Octokit client.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +organization_name+:: The name of the organization to retrieve from API    
    def self.display_organization_details(octokit_client, organization_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        organization = get_organization(octokit_client, organization_name)
        Log.log "Organization details: '%s' aka '%s' (%s)" % [organization.name, organization.login, organization.html_url]
    end

    ##
    # Returns all the teams assigned to the organization with this GitHub name.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +organization_name+:: The name of the organization to retrieve from API        
    def self.get_all_teams(octokit_client, organization_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        return octokit_client.organization_teams(organization_name, {:per_page => $RESULTS_PER_PAGE, :page => 1}).uniq
    end

    ##
    # Returns all the repositories assigned to the organization with this GitHub name.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +organization_name+:: The name of the organization to retrieve from API 
    def self.get_all_repositories(octokit_client, organization_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        repositories = []
        for page in 1..$EXPECTED_PAGE_COUNT
            Log.debug "Apply #{$RESULTS_PER_PAGE} results for #{page} / #{$EXPECTED_PAGE_COUNT} page"
            results = octokit_client.organization_repositories(organization_name, {:per_page => $RESULTS_PER_PAGE, :page => page})
            repositories = repositories + results
        end
        repositories = repositories.uniq
        Log.debug "Got %s results" % repositories.length
        return repositories
    end

    # Repositories
    # ------------

    ##
    # Returns the details of a repository
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +repository_full_name+:: The full name identifier of the repository to get, like 'organization/project-name'
    def self.get_repository(octokit_client, repository_full_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        return octokit_client.repository(repository_full_name)
    end

    ##
    # Display in standard output the project details using the given Octokit client.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +repository_full_name+:: The full name identifier of the repository to get, like 'organization/project-name'   
    def self.display_repository_details(octokit_client, repository_full_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        repository = get_repository(octokit_client, repository_full_name)
        Log.log "Repository details: id='%s', name='%s', fullname='%s', url='%s" % [repository.id, repository.name, repository.full_name, repository.html_url]
    end

    # Contributors, collaborators
    # ---------------------------

    ##
    # Returns the contributors of a repository with this full name, from teams, organizations or origin projects.
    # If you want only people assigned to the project, use self.get_repository_collaborators(octokit_client, repository_full_name) instead.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +repository_full_name+:: The full name identifier of the repository to get, like 'organization/project-name'
    def self.get_repository_contributors(octokit_client, repository_full_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        return octokit_client.contributors(repository_full_name, {:per_page => $RESULTS_PER_PAGE, :page => 1})
    end

    ##
    # Returns the direct collaborators of a repository with this full name.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +repository_full_name+:: The full name identifier of the repository to get, like 'organization/project-name'
    def self.get_repository_collaborators(octokit_client, repository_full_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        return octokit_client.collaborators(repository_full_name, {:per_page => $RESULTS_PER_PAGE, :page => 1, :affiliation => "direct"})
    end

    ##
    # Returns the teams of a repository with this full name.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +repository_full_name+:: The full name identifier of the repository to get, like 'organization/project-name'
    def self.get_repository_teams(octokit_client, repository_full_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        return octokit_client.repository_teams(repository_full_name, {:per_page => $RESULTS_PER_PAGE, :page => 1})
    end

    ##
    # Using the given Octokit client, for the repository which has that name, gets the permision for the user who has this login.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +repository_full_name+:: The full name identifier of the repository to get, like 'organization/project-name'
    # +user_login+:: The login of the user
    def self.get_user_permission_for_repository(octokit_client, repository_full_name, user_login)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        return octokit_client.permission_level(repository_full_name, user_login)
    end

    ##
    # Using the given Octokit client, for the repository which has that name, adds the user who has this login as a collaborator with the "pul" (i.e. read) permission level.
    # If the user was already added, just changes its permission level to "pull".
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +repository_full_name+:: The full name identifier of the repository to get, like 'organization/project-name'
    # +user_login+:: The login of the user
    def self.add_collaborator_to_repository_with_read_permission(octokit_client, repository_full_name, user_login)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        return octokit_client.add_collaborator(repository_full_name, user_login, permission: "pull")
    end

    ##
    # Using the given Octokit client, for the repository which has that name, adds the user who has this login as a collaborator with the "push" (i.e. write) permission level.
    # If the user was already added, just changes its permission level to "write".
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +repository_full_name+:: The full name identifier of the repository to get, like 'organization/project-name'
    # +user_login+:: The login of the user
    def self.add_collaborator_to_repository_with_write_permission(octokit_client, repository_full_name, user_login)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        return octokit_client.add_collaborator(repository_full_name, user_login, permission: "push")
    end

    ##
    # Using the given Octokit client, for the repository which has that name, adds the user who has this login as a collaborator with the "admin" permission level.
    # If the user was already added, just changes its permission level to "admin".
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +repository_full_name+:: The full name identifier of the repository to get, like 'organization/project-name'
    # +user_login+:: The login of the user
    def self.add_collaborator_to_repository_with_admin_permission(octokit_client, repository_full_name, user_login)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        return octokit_client.add_collaborator(repository_full_name, user_login, permission: "admin")
    end

    # Extended API
    # ------------

    ##
    # Returns all the members of the given organization
    # The Ruby environement variable OCTOKIT_ACCESS_TOKEN must be defined with the GitHub personal token as a value.
    def self.get_organization_members_with_2fa_disabled
        Octokit.auto_paginate = true
        return Octokit.org_members "#{$GITHUB_ORGANIZATION_NAME}", :filter => "2fa_disabled"
    end

    ##
    # Returns all the members of the given organization for whom the 2FA is disabled.
    # The Ruby environement variable OCTOKIT_ACCESS_TOKEN must be defined with the GitHub personal token as a value.
    def self.get_all_organization_members
        Octokit.auto_paginate = true
        return Octokit.org_members "#{$GITHUB_ORGANIZATION_NAME}"
    end

    ##
    # Returns all projects from the given organization which don't have any assigned team.
    # Applies a cooldown delay between requests to prevent to be rejecting by GitHub for API rate limits reasons.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +organization_name+:: The name of the organization to retrieve from API    
    def self.get_projects_without_team(octokit_client, organization_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        all_repositories = get_all_repositories(octokit_client, organization_name)
        count = all_repositories.length
        Log.debug "There are %s repositories to check" % count
        repositories_without_team = []
        index = 1
        all_repositories.each { |repo|
            Log.debug "Checking for repository '%s' (%s / %s)" % [repo.name, index, count]
            index += 1
            teams_url = repo.teams_url
            cool_down
            uri = URI.parse(teams_url)
            request = Net::HTTP::Get.new(uri)
            request["Authorization"] = "token #{$GITHUB_PERSONAL_ACCESS_TOKEN}"
            req_options = {
                use_ssl: uri.scheme == "https",
            }
            response = Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
                http.request(request)
            end
            cool_down
            json_response = JSON.parse(response.body)
            if json_response.length <= 0
                repositories_without_team << {"name" => "#{repo.name}", "full_name" => "#{repo.full_name}", "url" => "#{repo.html_url}"}
            end
        }
        return repositories_without_team
    end

    ##
    # Returns all users for the given organization whom don't have any defined email address.
    # Applies a cooldown delay between requests to prevent to be rejecting by GitHub API for rate limits reasons.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +organization_name+:: The name of the organization to retrieve from API      
    def self.get_users_with_bad_email(octokit_client, organization_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        members = get_all_organization_members()
        Log.debug "There are %s members to check" % members.length
        users_with_bad_emails = []
        cpt = 1
        members.each do |member|
            Log.debug "Check member '#{member.login}' (#{cpt} / #{members.length})"
            enriched_member = get_user(octokit_client, member.login)
            unless enriched_member == nil
                email = enriched_member.email
                if email == nil || email.empty?
                    users_with_bad_emails << {"login" => "#{enriched_member.login}", "name" => "#{enriched_member.name}", "url" => "#{enriched_member.html_url}"}
                end
            else
                Log.warning "Unexpected behaviour for user with name '#{member.login}'. You should have a look on it!"
            end
            cpt += 1
        end
        return users_with_bad_emails
    end

    ##
    # Check each member of the current organization and looks its fullname.
    # If the fullname field is undefined, empty or not suitable, points it.
    # Here a "non suitable" fullname does not contain only one spaces ' ' character, supposing if it contains a white space
    # we should have the first name on the left and the last name on the right.
    # If a full name has more than one space, we suppoe it might be suitable or not and need to check manually.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    def self.get_users_with_bad_fullname(octokit_client)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        members = get_all_organization_members()
        Log.debug "There are %s members to check" % members.length
        results = []
        cpt = 1
        members.each do |member|
            Log.debug "Check member '#{member.login}' (#{cpt} / #{members.length})"
            enriched_member = get_user(octokit_client, member.login)
            member_name = enriched_member.name
            if member_name == nil || member_name.empty? || !member_name.match(" ") || member_name.count(" ") > 1
                results << {"login" => "#{enriched_member.login}", "name" => "#{enriched_member.name}", "url" => "#{enriched_member.html_url}"}
            end
            cpt += 1
        end
        return results
    end

    ##
    # Get all repositories with undefined licenses
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +organization_name+:: The name of the organization to retrieve from API       
    def self.get_projects_without_licenses(octokit_client, organization_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        all_repositories = get_all_repositories(octokit_client, organization_name)
        count = all_repositories.length
        Log.debug "There are %s repositories to check" % count
        repositories_without_licenses = []
        cpt = 1
        all_repositories.each do |repository|
            Log.debug "Check repository #{repository.name} (#{cpt} / #{count})"
            if repository.license == nil
                repositories_without_licenses << {"name" => "#{repository.name}", "full_name" => "#{repository.full_name}", "url" => "#{repository.html_url}"}
            else
                license_in_use = repository.license.name
                if license_in_use == nil || license_in_use .empty?
                    repositories_without_licenses << {"name" => "#{repository.name}", "full_name" => "#{repository.full_name}", "url" => "#{repository.html_url}"}
                end
            end
            cpt += 1
        end
        return repositories_without_licenses
    end

    ##
    # Get all repositories for the organization.
    # For each of them, check if common files exists: README, LICENSE, AUTHORS, THIRD-PARTY.
    # If not, logs the unconform repository.
    # Each iteration makes a clone of the repository using SSH, and a check of the targets files supposing to be at the root.
    # Then clones are deleted.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +organization_name+:: The name of the organization to retrieve from API        
    def self.get_not_conform_repositories(octokit_client, organization_name)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        all_repositories = get_all_repositories(octokit_client, organization_name)
        repositories_count = all_repositories.length
        Log.debug "There are %s repositories to check" % repositories_count
        expected_files_name = expected_files_for_conform_projects()
        Log.debug "There are %s files to look for" % expected_files_name.length
        unconform_repositories = []
        cpt = 1
        all_repositories.each do |repository|
            repository_name = repository.name
            repository_url = repository.html_url
            repository_ssh_url = repository.ssh_url
            current_repo = {"name" => "#{repository_name}", "url" => "#{repository_url}"}
            Log.debug "Will clone repository %s out of %s" % [cpt, repositories_count]
            full_name="data/#{repository_name}"
            GitWrapper.clone_git_repository(repository_ssh_url, full_name)
            Log.debug "Checking content of '#{repository_name}' in folder '#{full_name}'"
            expected_files_name.each do |expected_file_name|
                path_name = "#{full_name}/#{expected_file_name}"
                if !File.exist?(path_name) && !File.exist?("#{path_name}.txt") && !File.exist?("#{path_name}.md")
                    current_repo[expected_file_name] = "0"
                else
                    current_repo[expected_file_name] = "1"
                end
            end
            unconform_repositories << current_repo
            FileUtils.rm_rf(full_name)
            cpt += 1
        end
        return unconform_repositories
    end

    ##
    # Get all repositories for the organization.
    # For each of them, check if they are empty or seems to be empty.
    # If not, logs the repository.
    # Each iteration makes a clone of the repository using SSH befoire counting files.
    # Then clones are deleted.
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +organization_name+:: The name of the organization to retrieve from API 
    # +limit+:: The threshold to use to say if the repository is empty or seems to be empty with just basic files (default is 1)
    def self.get_empty_repositories(octokit_client, organization_name, limit = 1)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        all_repositories = get_all_repositories(octokit_client, organization_name)
        repositories_count = all_repositories.length
        Log.debug "There are %s repositories to check" % repositories_count
        empty_repositories = []
        cpt = 1
        all_repositories.each do |repository|
            repository_name = repository.name
            repository_url = repository.html_url
            repository_ssh_url = repository.ssh_url
            Log.debug "Will clone repository %s out of %s" % [cpt, repositories_count]
            full_name="data/#{repository_name}"
            GitWrapper.clone_git_repository(repository_ssh_url, full_name)
            Log.debug "Checking content of '#{repository_name}' in foler '#{full_name}'"
            count = Dir.glob(File.join(full_name, '**', '*')).select { |file| File.file?(file) }.count
            if count <= limit
                empty_repositories << {"name" => "#{repository_name}", "url" => "#{repository_url}"}
            end
            FileUtils.rm_rf(full_name)
            cpt += 1
        end
        return empty_repositories
    end

    ##
    # For each repository for the given organization, for all users except teams and GitHub adminitrator, define permission
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +organization_name+:: The name of the organization to retrieve from API 
    # +permission+:: Must be "push" (write), "pull" (read) or "admin" (admin)
    def self.set_permissions_for_users(octokit_client, organization_name, permission)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        if permission != "push" && permission != "pull" && permission != "admin"
            Log.warning "Permission #{permission} is not managed. Returns now."
            return
        end
        owners = organization_owners
        Log.debug "Get all projects of organization '#{organization_name}'..."
        all_repositories = get_all_repositories(octokit_client, organization_name)
        Log.debug "Found #{all_repositories.length} projects!"
        all_repositories.each do |repository|
            repo_full_name = repository.full_name
            Log.debug "Get people of project #{repo_full_name}..."
            members = get_repository_collaborators(octokit_client, repo_full_name)
            if members.length <= 0
                Log.warning "No direct collaborator found for project #{repo_full_name}, maybe only teams have been added."
                next
            end
            Log.debug "Found #{members.length} people for this project."
            members.each do |member|
                member_login = member.login
                unless owners.include? member_login
                    Log.debug "Update permision to PUSH for user with login '#{member_login}' on project #{repo_full_name}"
                    add_collaborator_to_repository_with_write_permission(octokit_client, repo_full_name, member_login)
                else 
                    Log.debug "User with login '#{member_login}' is organization owner, permissions are not changed for project #{repo_full_name}"
                end
            end
        end
    end

    ##
    # For each repository for the given organization, for all teams, define permission
    # +octokit_client+:: The Octokit client to use to request the GitHub web API
    # +organization_name+:: The name of the organization to retrieve from API 
    # +permission+:: Must be "push" (write), "pull" (read) or "admin" (admin)
    def self.set_permissions_for_teams(octokit_client, organization_name, permission)
        if octokit_client.nil? 
            Log.error "Nil Octokit client. Returns now." 
            return
        end
        if permission != "push" && permission != "pull" && permission != "admin"
            Log.warning "Permission #{permission} is not managed. Returns now.s"
            return
        end
        Log.debug "Get all projects of organization '#{organization_name}'..."
        all_repositories = get_all_repositories(octokit_client, organization_name)
        Log.debug "Found #{all_repositories.length} projects!"
        all_repositories.each do |repository|
            repo_full_name = repository.full_name
            Log.debug "Get teams of project #{repo_full_name}..."
            teams = get_repository_teams(octokit_client, repo_full_name)
            if teams.length <= 0
                Log.warning "No team found for project #{repo_full_name}!"
                next
            end
            Log.debug "Found #{teams.length} teams for #{repo_full_name}"
            teams.each do |team|
                Log.debug "For team '#{team.name}' with id '#{team.id}' set permission to '#{permission}' for repository '#{repo_full_name}'"
                octokit_client.add_team_repository(team.id, repo_full_name, permission: permission)
            end
        end
    end

    private

    ##
    # Makes current thread sleep during $REQUEST_DELAY_IN_SECONDS
    def self.cool_down
        sleep($REQUEST_DELAY_IN_SECONDS)
    end

    ##
    # Returns an array of expected file names picked from configuration, using ; to split
    def self.expected_files_for_conform_projects
        $GIT_PROJECT_MANDATORY_FILES.split(";")
    end

    ##
    # Returns an array of owners picked from configuration, using ; to split
    def self.organization_owners
        $GITHUB_ORGANIZATION_ADMINS.split(";")
    end

end