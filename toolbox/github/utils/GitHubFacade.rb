#!/usr/bin/env ruby
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2021-2022 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Version.............: 1.2.0
# Since...............: 26/04/2021
# Description.........: Received from arguments a feature to launch using GitHub API.
# Loads configuration elements from configuration.rb, writes outputs using FileManager.rb and calls GitHubWrapper.rb for requests
#
# Usage: ruby GitHubFacade.rb feature-to-launch
# where feature-to-launch in: [get-members-2fa-disabled, get-all-members, get-members-without-company, get-projects-without-team, get-users-with-bad-email, get-users-with-bad-fullname, get_not_conform_repositories, get-unconform-projects, get-projects-without-licenses, set-users-permissions-to-push, set-teams-permissions-to-push]
#
# Note that some features need to have Ruby env. varibale set (OCTOKIT_ACCESS_TOKEN), use the Shell wizard to do so.
# Shell wizard must be prefered than than using this Ruby file.
#
# Exit codes:
#    0 = ok
#    2 = no feature
#    3 = unknown feature
#    4 = no GitHub personal acces token
#    5 = no GitHub organization name
#    6 = no feature started
#    100 = bad prerequisites

require_relative '../configuration.rb'
require_relative 'GitHubWrapper.rb'
require_relative 'IO.rb'

# Exit codes
# ----------

$EXIT_OK = 0
$EXIT_NO_FEATURE = 2
$EXIT_UNKNOWN_FEATURE = 3
$EXIT_NO_GITHUB_PERSONAL_ACCESS_TOKEN = 4
$EXIT_NO_GITHUB_ORGANIZATION_NAME = 5
$EXIT_NO_FEATURE_STARTED = 6
$EXIT_BAD_SETUP = 100

# Check arguments
# ---------------

if ARGV.length <= 0
    Log.error "No defined features. Exit now."
    exit $EXIT_NO_FEATURE
end
feature_to_run=ARGV[0]

if feature_to_run != "get-members-2fa-disabled" && feature_to_run != "get-all-members" && feature_to_run != "get-members-without-company" && feature_to_run != "get-projects-without-team" && feature_to_run != "get-users-with-bad-email" && feature_to_run != "get-users-with-bad-fullname" && feature_to_run != "get-projects-conformity" && feature_to_run != "get-projects-without-licenses" && feature_to_run != "get-empty-projects" && feature_to_run != "set-users-permissions-to-push" && feature_to_run != "set-teams-permissions-to-push" 
    Log.error "Unknown feature. Exit now."
    exit $EXIT_UNKNOWN_FEATURE
end

# Configuration elements
# ----------------------

if $GITHUB_PERSONAL_ACCESS_TOKEN.nil? || $GITHUB_PERSONAL_ACCESS_TOKEN.empty?
    Log.error "GITHUB_PERSONAL_ACCESS_TOKEN is not defined. Exit now."
    exit $EXIT_NO_GITHUB_PERSONAL_ACCESS_TOKEN
end

if $GITHUB_ORGANIZATION_NAME.nil? || $GITHUB_ORGANIZATION_NAME.empty?
    Log.error "GITHUB_ORGANIZATION_NAME is not defined. Exit now."
    exit $GITHUB_ORGANIZATION_NAME
end

# Run features
# ------------

Log.debug "Creating new Octokit client..."
client = GitHubWrapper.create_octokit_client($GITHUB_PERSONAL_ACCESS_TOKEN)

# FEATURE: get-members-2fa-disabled
# Get members for whom 2FA is disabled, then get more details about them and log
if feature_to_run == "get-members-2fa-disabled"
    if $FILENAME_MEMBERS_2FA_DISABLED.empty?
        Log.error "FILENAME_MEMBERS_2FA_DISABLED value is not defined. Returns now."
        exit $EXIT_BAD_SETUP
    end
    members = []
    Log.log "Getting members of organizations with 2FA disabled..."
    raw_members = GitHubWrapper.get_organization_members_with_2fa_disabled
    Log.debug "Found #{raw_members.length} members!"
    cpt = 1
    raw_members.each { |light_member| 
        Log.debug "Getting more details for #{light_member.login} (#{cpt} / #{raw_members.length})"
        member = GitHubWrapper.get_user(client, light_member.login)
        members << member
        cpt += 1
    }
    Log.debug "Writting in log file #{$FILENAME_MEMBERS_2FA_DISABLED}..."
    FileManager.write_members_in_permanent_file(members, $FILENAME_MEMBERS_2FA_DISABLED)
    Log.log "Task completed! Exits now."
    exit $EXIT_OK
end

# FEATURE: get-all-members
# Get all members of organization
if feature_to_run == "get-all-members"
    if $FILENAME_MEMBERS.empty?
        Log.error "FILENAME_MEMBERS value is not defined. Returns now."
        exit $EXIT_BAD_SETUP
    end
    members = []
    Log.log "Getting all members of organization..."
    raw_members = GitHubWrapper.get_all_organization_members
    Log.debug "Found #{raw_members.length} members!"
    cpt = 1
    raw_members.each { |light_member| 
        Log.debug "Getting more details for #{light_member.login} (#{cpt} / #{raw_members.length})"
        member = GitHubWrapper.get_user(client, light_member.login)
        members << member
        cpt += 1
    }
    Log.debug "Writting in log file #{$FILENAME_MEMBERS}..."
    FileManager.write_members_in_permanent_file(members, $FILENAME_MEMBERS)
    Log.log "Task completed! Exits now."
    exit $EXIT_OK
end

# FEATURE: get-members-without-company
# Get members of organization with undefined company
if feature_to_run == "get-members-without-company"
    if $FILENAME_MEMBERS_UNDEFINED_COMPANY.empty?
        Log.error "FILENAME_MEMBERS_UNDEFINED_COMPANY value is not defined. Returns now."
        exit $EXIT_BAD_SETUP
    end
    members = []
    Log.log "Getting members of organization without company..."
    raw_members = GitHubWrapper.get_all_organization_members
    Log.debug "Found #{raw_members.length} members in organization."
    cpt = 1
    raw_members.each { |light_member| 
        Log.debug "Checking company for #{light_member.login} (#{cpt} / #{raw_members.length})"
        member = GitHubWrapper.get_user(client, light_member.login)
        company = "#{member.company}"
        unless company.length > 0
            members << member
        end
        cpt += 1
    }
    Log.debug "Found #{members.length} members without defined company!"
    Log.debug "Writting in log file #{$FILENAME_MEMBERS_UNDEFINED_COMPANY}..."
    FileManager.write_members_in_permanent_file(members, $FILENAME_MEMBERS_UNDEFINED_COMPANY)
    Log.log "Task completed! Exits now."
    exit $EXIT_OK
end

# FEATURE: get-projects-without-team
# Get all projects of the organization which do not have any teams
if feature_to_run == "get-projects-without-team"
    if $FILENAME_PROJECTS_WITHOUT_TEAM.empty?
        Log.error "FILENAME_PROJECTS_WITHOUT_TEAM value is not defined. Returns now."
        exit $EXIT_BAD_SETUP
    end
    Log.log "Getting projects of organization without teams..."
    projects = GitHubWrapper.get_projects_without_team(client, $GITHUB_ORGANIZATION_NAME)
    Log.debug "Found #{projects.length} projects!"
    Log.debug "Writting in log file #{$FILENAME_PROJECTS_WITHOUT_TEAM}..."
    FileManager.write_projects_in_permanent_file(projects, $FILENAME_PROJECTS_WITHOUT_TEAM)
    Log.log "Task completed! Exits now."
    exit $EXIT_OK
end

# FEATURE: get-users-with-bad-email
# Get all users of the organization with bad email address (hiden, undefined...)
if feature_to_run == "get-users-with-bad-email"
    if $FILENAME_USERS_WITH_BAD_EMAILS.empty?
        Log.error "FILENAME_USERS_WITH_BAD_EMAILS value is not defined. Returns now."
        exit $EXIT_BAD_SETUP
    end
    Log.log "Getting users with bad emails..."
    users = GitHubWrapper.get_users_with_bad_email(client, $GITHUB_ORGANIZATION_NAME)
    Log.debug "Found #{users.length} users!"
    Log.debug "Writting in log file #{$FILENAME_USERS_WITH_BAD_EMAILS}..."
    FileManager.write_members_array_in_permanent_file(users, $FILENAME_USERS_WITH_BAD_EMAILS)
    Log.log "Task completed! Exits now."
    exit $EXIT_OK
end

# FEATURE: get-users-with-bad-fulllnames
# Get all users of the organization with bad email address (hiden, undefined...)
if feature_to_run == "get-users-with-bad-fullname"
    if $FILENAME_USERS_WITH_BAD_FULLNAMES.empty?
        Log.error "FILENAME_USERS_WITH_BAD_FULLNAMES value is not defined. Returns now."
        exit $EXIT_BAD_SETUP
    end
    Log.log "Getting users with bad fullname..."
    users = GitHubWrapper.get_users_with_bad_fullname(client)
    Log.debug "Found #{users.length} users!"
    Log.debug "Writting in log file #{$FILENAME_USERS_WITH_BAD_FULLNAMES}..."
    FileManager.write_members_array_in_permanent_file(users, $FILENAME_USERS_WITH_BAD_FULLNAMES)
    Log.log "Task completed! Exits now."
    exit $EXIT_OK
end

# FEATURE: get-projects-without-licenses
# Get all projects without licenses
if feature_to_run == "get-projects-without-licenses"
    if $FILENAME_PROJECTS_WITHOUT_LICENSES.empty?
        Log.error "FILENAME_PROJECTS_WITHOUT_LICENSES value is not defined. Returns now."
        exit $EXIT_BAD_SETUP
    end
    Log.log "Getting projects without licenses..."
    projects = GitHubWrapper.get_projects_without_licenses(client, $GITHUB_ORGANIZATION_NAME)
    Log.debug "Found #{projects.length} projects!"
    Log.debug "Writting in log file #{$FILENAME_PROJECTS_WITHOUT_LICENSES}..."
    FileManager.write_projects_in_permanent_file(projects, $FILENAME_PROJECTS_WITHOUT_LICENSES)
    Log.log "Task completed! Exits now."
    exit $EXIT_OK
end

# FEATURE: get-projects-conformity
# List repositories which seems to be unconform
if feature_to_run == "get-projects-conformity"
    if $FILENAME_PROJECTS_WITH_UNCONFORM_REPOSITORIES.empty?
        Log.error "FILENAME_PROJECTS_WITH_UNCONFORM_REPOSITORIES value is not defined. Returns now."
        exit $EXIT_BAD_SETUP
    end
    Log.log "Check conformity of repositories..."
    repositories = GitHubWrapper.get_not_conform_repositories(client, $GITHUB_ORGANIZATION_NAME)
    Log.debug "Found #{repositories.length} repositories!"
    Log.debug "Writting in log file #{$FILENAME_PROJECTS_WITH_UNCONFORM_REPOSITORIES}..."
    FileManager.write_unconform_projects_in_permanent_file(repositories, $FILENAME_PROJECTS_WITH_UNCONFORM_REPOSITORIES)
    Log.log "Task completed! Exits now."
    exit $EXIT_OK
end

# FEATURE: get-empty-projects
# List projects which seems to be empty
if feature_to_run == "get-empty-projects"
    if $FILENAME_EMPTY_PROJECTS.empty?
        Log.error "FILENAME_EMPTY_PROJECTS value is not defined. Returns now."
        exit $EXIT_BAD_SETUP
    end
    Log.log "Getting repositories which seems to be empty..."
    repositories = GitHubWrapper.get_empty_repositories(client, $GITHUB_ORGANIZATION_NAME)
    Log.debug "Found #{repositories.length} repositories!"
    Log.debug "Writting in log file #{$FILENAME_EMPTY_PROJECTS}..."
    FileManager.write_projects_in_permanent_file(repositories, $FILENAME_EMPTY_PROJECTS)
    Log.log "Task completed! Exits now."
    exit $EXIT_OK
end

# FEATURE: set-users-permissions-to-push
# For all projects, change right to 'push' for each contributor except teams and GitHub administrators
if feature_to_run == "set-users-permissions-to-push"
    Log.log "Updating all repositories with new permissions for users..."
    GitHubWrapper.set_permissions_for_users(client, $GITHUB_ORGANIZATION_NAME, "push")
    Log.log "Task completed! Exits now."
    exit $EXIT_OK
end

# FEATURE: set-teams-permissions-to-push
# For all projects, change right to 'push' for each team
if feature_to_run == "set-teams-permissions-to-push"
    Log.log "Updating all repositories with new permissions for teams..."
    GitHubWrapper.set_permissions_for_teams(client, $GITHUB_ORGANIZATION_NAME, "push")
    Log.log "Task completed! Exits now."
    exit $EXIT_OK
end

exit $EXIT_NO_FEATURE_STARTED
