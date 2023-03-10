# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

# Allow debug message or not
$LOG_DEBUG = false

# GitHub organization
# -------------------

# You have to create a personal access token on: https://github.com/settings/tokens
$GITHUB_PERSONAL_ACCESS_TOKEN = ""

# Name of the organization name you want to deal with so as to request the GitHub API
$GITHUB_ORGANIZATION_NAME = ""

# Accurate list of users which are admins (i.e. GitHub organization owners), with login separated by ;
$GITHUB_ORGANIZATION_ADMINS = ""

# Repositories' content
# ---------------------

# Accurate list of file names without extensions each project should have, separated by ;
$GIT_PROJECT_MANDATORY_FILES = ""

# Static configuration
# --------------------

# Delay to apply between each request, makes thread sleep
$REQUEST_DELAY_IN_SECONDS = 0.5

# Results returned in one page (GitHub pagination), max 100
$RESULTS_PER_PAGE = 100

# Expected numer of pages to use to load all elements (i.e. if 250 projects, we need 3 pages with 100 items per page)
$EXPECTED_PAGE_COUNT = 3

# Result files
# ------------

# Directory name for output files (not used in every scripts yet, beware)
$OUTPUT_DIRECTORY_NAME = "data"

# File name to store all memmbers of the organization
$FILENAME_MEMBERS = "organization-members.csv"

# File name to store each memmber of the organization with 2FA disabled
$FILENAME_MEMBERS_2FA_DISABLED = "organization-members-2FA-disabled.csv"

# File name to store each memmber of the organization without defined company
$FILENAME_MEMBERS_UNDEFINED_COMPANY = "organization-members-undefined-company.csv"

# File name to store projects without team
$FILENAME_PROJECTS_WITHOUT_TEAM = "organization-projects-without-team.csv"

# File name to store users with bad email adresses
$FILENAME_USERS_WITH_BAD_EMAILS = "organization-users-bad-emails.csv"

# File name to store users with bad fullnames
$FILENAME_USERS_WITH_BAD_FULLNAMES = "organization-users-bad-fullnames.csv"

# File name to store repositories with seems to be unconform
$FILENAME_PROJECTS_WITH_UNCONFORM_REPOSITORIES = "organization-projects-unconform-repositories.csv"

# File name to store repositories without defined licenses
$FILENAME_PROJECTS_WITHOUT_LICENSES = "organization-projects-without-licenses.csv"

# File name to store empty repositories
$FILENAME_EMPTY_PROJECTS = "organization-empty-projects.csv"

# Repositories
# ------------

# Location to store all clones of repositories (absolute paths, no interpretation with ~ etc)
$REPOSITORIES_CLONE_LOCATION_PATH = ""

# Field for URL to use for repositories cloning (within clone_url for HTTP and SSH_URL for SSH) - GitHub API response
$REPOSITORIES_CLONE_URL_JSON_KEY = "ssh_url"

# Flag to rise if GitHub archived projects must not be scanned for leaks or vulnerabilities ('true' or 'false')
$EXCLUDE_GITHUB_ARCHIVED_PROJECTS_FOR_SCANS = true