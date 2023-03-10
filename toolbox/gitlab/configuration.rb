# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) 2020-2023 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license.
#
# Author: Pierre-Yves LAPERSONNE <pierreyves(dot)lapersonne(at)orange(dot)com> et al.

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