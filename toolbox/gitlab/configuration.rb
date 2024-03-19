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

# GitLab organization
# -------------------

# You have to create a personal access token on: https://gitlab.com/-/profile/personal_access_tokens
$GILAB_PERSONAL_ACCESS_TOKEN = ""

# ID of the GitLab group, i.e. the organisation ID you want to deal with so as to request the GitLab API
$GITLAB_ORGANIZATION_ID = ""

# Requests
# --------

# Results returned in one page (GitLab pagination, max 100)
$RESULTS_PER_PAGE = 100

# Repositories
# ------------

# Location to store all clones of repositories (absolute paths, no interpretation with ~ etc)
$REPOSITORIES_CLONE_LOCATION_PATH = ""

# Field for URL to use for repositories cloning (within http_url_to_repo for HTTP and ssh_url_to_repo for SSH)
$REPOSITORIES_CLONE_URL_JSON_KEY = "ssh_url_to_repo"