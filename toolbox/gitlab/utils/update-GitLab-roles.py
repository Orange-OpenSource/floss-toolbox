#!/usr/bin/env python3.8
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

import argparse
from dotenv import load_dotenv
import requests
import os
import time

# Environment variables
# ---------------------

# Below are expected environment variables defined in .env file beside this script:
# - GITLAB_URL: the URL to the GitLab instance (e.g. "https://gitlab.com")
# - ORGANIZATION_NAME: organization name for GitLab (e.g. "Orange-OpenSource")
# - ROLE_ID_TO_CHANGE: the identifier of the role to change (e.g. "50" for "Owner")
# - CUSTOM_ROLE_ID_TO_APPLY: the identifier of the new role to apply (e.g. "2004291" for a custom role)
# - PROTECTED_USERS: the list of users for whom role must not be changed, comma separated (e.g. "bbailleux,lmarie23,pylapersonne-orange,NicolasToussaint")
# - GITLAB_PRIVATE_TOKEN: private API token for GitLab organization

# See for values of roles doc at https://docs.gitlab.com/development/permissions/predefined_roles/
# Get custom identifier for role at https://gitlab.com/groups/{ORG_NAME}/-/settings/roles_and_permissions

load_dotenv()

# Configuration
# -------------

GITLAB_URL = os.getenv('GITLAB_URL')
ORG_NAME = os.getenv('ORGANIZATION_NAME')
ROLE_ID_TO_CHANGE = int(os.getenv('ROLE_ID_TO_CHANGE'), 10)
CUSTOM_ROLE_ID_TO_APPLY = int(os.getenv('CUSTOM_ROLE_ID_TO_APPLY', 10))
GITLAB_PRIVATE_TOKEN = os.getenv('GITLAB_PRIVATE_TOKEN')
PROTECTED_USERS = os.getenv('PROTECTED_USERS', '').split(',')

headers = {
    'Private-Token': GITLAB_PRIVATE_TOKEN
}

# Environement checks
# -------------------

if not GITLAB_URL:
    raise ValueError("💥 Error: The environment variable 'GITLAB_URL' is not set or is empty.")
if not ORG_NAME:
    raise ValueError("💥 Error: The environment variable 'ORG_NAME' is not set or is empty.")    
if not ROLE_ID_TO_CHANGE:
    raise ValueError("💥 Error: The environment variable 'ROLE_ID_TO_CHANGE' is not set or is empty.")
if not CUSTOM_ROLE_ID_TO_APPLY:
    raise ValueError("💥 Error: The environment variable 'CUSTOM_ROLE_ID_TO_APPLY' is not set or is empty.")    
if not GITLAB_PRIVATE_TOKEN:
    raise ValueError("💥 Error: The environment variable 'GITLAB_PRIVATE_TOKEN' is not set or is empty.")
if not PROTECTED_USERS:
    raise ValueError("💥 Error: The environment variable 'PROTECTED_USERS' is not set or is empty.")
try:
    CUSTOM_ROLE_ID_TO_APPLY = int(CUSTOM_ROLE_ID_TO_APPLY)
except ValueError:
    raise ValueError("💥 Error: The environment variable 'CUSTOM_ROLE_ID_TO_APPLY' must be an integer.")
try:
    ROLE_ID_TO_CHANGE = int(ROLE_ID_TO_CHANGE)
except ValueError:
    raise ValueError("💥 Error: The environment variable 'ROLE_ID_TO_CHANGE' must be an integer.")

# Services API
# ------------

# Change roles for groups and projects
# ------------------------------------

def change_role(project_id, user_id):
    """
    Change the role of a member in a project by applying role with id CUSTOM_ROLE_ID_TO_APPLY.

    :param project_id: ID of the project where the role needs to be changed.
    :param user_id: ID of the user whose role needs to be changed.
    :return: True if the change was successful, otherwise False.
    """
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/members/{user_id}"
    data = {'access_level': CUSTOM_ROLE_ID_TO_APPLY}
    response = requests.put(url, headers=headers, data=data)
    if response.status_code != 200:
        print(f"❌ Failed to change role for project: {response.status_code} - {response.text}")
        return False
    else:
        return True

def change_group_role(group_id, user_id):
    """
    Change the role of a member in a group by applying role with id CUSTOM_ROLE_ID_TO_APPLY.

    :param group_id: ID of the group where the role needs to be changed.
    :param user_id: ID of the user whose role needs to be changed.
    :return: True if the change was successful, otherwise False.
    """
    url = f"{GITLAB_URL}/api/v4/groups/{group_id}/members/{user_id}"
    data = {'access_level': CUSTOM_ROLE_ID_TO_APPLY}
    response = requests.put(url, headers=headers, data=data)
    if response.status_code != 200:
        print(f"❌ Failed to change role for group: {response.status_code} - {response.text}")
        return False
    else:
        return True

# List roles to change for groups and projects
# --------------------------------------------

def list_group_role_to_change(group_id):
    """
    List all members with the role identified by ROLE_ID_TO_CHANGE to change in a group.

    :param group_id: ID of the group whose members need to be listed.
    :return: List of members with the role ROLE_ID_TO_CHANGE.
    """
    members_url = f"{GITLAB_URL}/api/v4/groups/{group_id}/members"
    response = requests.get(members_url, headers=headers)

    if response.status_code == 200:
        members = response.json()
        return [member for member in members if member['access_level'] == ROLE_ID_TO_CHANGE]
    else:
        print(f"❌ Failed to retrieve members for group '{group_id}': {response.status_code} - {response.text}")
        return []

def list_project_role_to_change(project_id):
    """
    List all members with the role identified by ROLE_ID_TO_CHANGE in a project.

    :param project_id: ID of the project whose members need to be listed.
    :return: List of members with the role ROLE_ID_TO_CHANGE.
    """
    members_url = f"{GITLAB_URL}/api/v4/projects/{project_id}/members"
    response = requests.get(members_url, headers=headers)

    if response.status_code == 200:
        members = response.json()
        return [member for member in members if member['access_level'] == ROLE_ID_TO_CHANGE]
    else:
        print(f"❌ Failed to retrieve members for project '{project_id}': {response.status_code} - {response.text}")
        return []

# Get groups and projects names
# -----------------------------

def get_group_name(group_id):
    """
    Get the name of the group by its ID.

    :param group_id: ID of the group.
    :return: Name of the group.
    """
    url = f"{GITLAB_URL}/api/v4/groups/{group_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('name')
    else:
        print(f"❌ Failed to retrieve group name for group '{group_id}': {response.status_code} - {response.text}")
        return None

def get_project_name(project_id):
    """
    Get the name of the project by its ID.

    :param project_id: ID of the project.
    :return: Name of the project.
    """
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('name')
    else:
        print(f"❌ Failed to retrieve project name for project '{project_id}': {response.status_code} - {response.text}")
        return None

# Process groups and projects
# ---------------------------

def process_group(group_id):
    """
    Process a group by retrieving its members, subgroups, and projects.

    :param group_id: ID of the group to process.
    """
    group_name = get_group_name(group_id)
    print(f"⏳ Processing group with name '{group_name}'")
    # List roles to change of the group
    group_roles_to_change = list_group_role_to_change(group_id)
    if group_roles_to_change:
        print(f"ℹ️ Roles to change in group '{group_name}' (ID: '{group_id}'): {[to_change['username'] for to_change in group_roles_to_change]}")
        for to_change in group_roles_to_change:
            if to_change['username'] not in PROTECTED_USERS:
                if change_group_role(group_id, to_change['id']):
                    print(f"✅ Changed role for '{to_change['username']}' in group '{group_name}'")
                else:
                    print(f"😱 Failed to change role for '{to_change['username']}' in group '{group_name}'")                    
            else:
                print(f"🛑 '{to_change['username']}' is a protected user and will not be changed.")

    # Retrieve subgroups
    subgroups_url = f"{GITLAB_URL}/api/v4/groups/{group_id}/subgroups"
    subgroups = requests.get(subgroups_url, headers=headers).json()

    if isinstance(subgroups, list): 
        for subgroup in subgroups:
            process_group(subgroup['id'])

    # Retrieve projects in the group
    projects_url = f"{GITLAB_URL}/api/v4/groups/{group_id}/projects"
    projects = requests.get(projects_url, headers=headers).json()

    if isinstance(projects, list):
        for project in projects:
            project_name = get_project_name(project['id']) 
            print(f"⏳ Processing project with name '{project_name}'")
            project_role_to_change = list_project_role_to_change(project['id'])
            if project_role_to_change:
                print(f"ℹ️ Roles to change in project '{project_name}' (ID: '{project['id']}'): {[to_change['username'] for to_change in project_role_to_change]}")
                for to_change in project_role_to_change:
                    if to_change['username'] not in PROTECTED_USERS:
                        if change_role(project['id'], to_change['id']):
                            print(f"✅ Changed role for '{to_change['username']}' in project '{project_name}'")
                        else:
                            print(f"😱 Failed to change role for '{to_change['username']}' in project '{project_name}'")
                    else:
                        print(f"🛑 '{to_change['username']}' is a protected user and will not be changed.")
    else:
        print(f"❌ Unexpected response format for projects in group '{group_name}': {projects}")

# Main
# -----

def main():
    """
    Main function that handles command-line arguments and initiates processing.
    """
    start_time = time.time()  # Record the start time

    print(f"❗In organization '{ORG_NAME}' on '{GITLAB_URL}' will change all roles with identifier ROLE_ID_TO_CHANGE '{ROLE_ID_TO_CHANGE}' to CUSTOM_ROLE_ID_TO_APPLY '{CUSTOM_ROLE_ID_TO_APPLY}'")
    # Wait for user input before exiting
    input("👉 Press any key to continue...")

    # Retrieve the ID of the organization
    groups_url = f"{GITLAB_URL}/api/v4/groups?search={ORG_NAME}"
    groups = requests.get(groups_url, headers=headers).json()

    if isinstance(groups, list):
        for group in groups:
            process_group(group['id'])
    else:
        print(f"❌ Unexpected response format for groups: {groups}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"⌛ Elapsed time: {elapsed_time:.2f} seconds")
    print("🧡 If you spotted a bug or have idea to improve the script, go there: https://github.com/Orange-OpenSource/floss-toolbox/issues/new/choose")
    print("👋 Bye!")

if __name__ == "__main__":
    main()
