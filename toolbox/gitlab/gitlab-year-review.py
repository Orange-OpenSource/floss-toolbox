#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) Orange SA
# SPDX-License-Identifier: Apache-2.0

import argparse
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import sys
import time

# Configuration - Tool
# --------------------

VERSION = "1.0.0"

ERROR_BAD_PREREQUISITES = 1

# Configuration - Load
# --------------------

load_dotenv()

# Configuration - GitLab
# ----------------------

GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN")
ORGANIZATION_NAME = os.getenv("ORGANIZATION_NAME")

# Configuration - Endpoints
# -------------------------

GROUPS_URL = f"https://gitlab.com/api/v4/groups/{ORGANIZATION_NAME}/subgroups"
PROJECTS_URL = f"https://gitlab.com/api/v4/groups/{{group_id}}/projects"
ORG_MEMBERS_URL = f"https://gitlab.com/api/v4/groups/{ORGANIZATION_NAME}/members"

HEADERS = {
    "Private-Token": GITLAB_API_TOKEN
}

# Services
# --------

def check_prerequisites():
    """Check if all configuration elements have been loaded through .env file."""
    if GITLAB_API_TOKEN is None:
        print("❌ Error: GitLab token is not defined. Please set the GITLAB_API_TOKEN environment variable.")
        sys.exit(ERROR_BAD_PREREQUISITES)

    if ORGANIZATION_NAME is None or ORGANIZATION_NAME.strip() == "":
        print("❌ Error: Organization name is not defined. Please set the ORGANIZATION_NAME variable.")
        sys.exit(ERROR_BAD_PREREQUISITES)

def get_subgroups():
    """Fetch all subgroups for the organization."""
    print("🔨 Fetching subgroups...")
    subgroups = []
    page = 1
    while True:
        response = requests.get(f"{GROUPS_URL}?page={page}&per_page=100", headers=HEADERS)
        if response.status_code != 200:
            print("❌ Failed to fetch subgroups, status code:", response.status_code)
            break
        data = response.json()
        if not data:
            print("🔨 No more subgroups to fetch.")
            break
        subgroups.extend(data)
        print(f"🔨 Fetched {len(data)} subgroups from page {page}.")
        page += 1
    print("🔨 Total subgroups fetched:", len(subgroups))
    return subgroups

def get_projects(group_id):
    """Fetch all projects for a given subgroup."""
    print(f"🔨 Fetching projects for group ID: {group_id}...")
    projects = []
    page = 1
    while True:
        response = requests.get(f"{PROJECTS_URL.format(group_id=group_id)}?page={page}&per_page=100", headers=HEADERS)
        if response.status_code != 200:
            print("❌ Failed to fetch projects, status code:", response.status_code)
            break
        data = response.json()
        if not data:
            print("🔨 No more projects to fetch.")
            break
        projects.extend(data)
        print(f"🔨 Fetched {len(data)} projects from page {page}.")
        page += 1
    print("🔨 Total projects fetched for group ID", group_id, ":", len(projects))
    return projects

def get_members():
    """Fetch all members of the organization."""
    print("🔨 Fetching organization members...")
    members = []
    page = 1
    while True:
        response = requests.get(f"{ORG_MEMBERS_URL}?page={page}&per_page=100", headers=HEADERS)
        if response.status_code != 200:
            print("❌ Failed to fetch members, status code:", response.status_code)
            break
        data = response.json()
        if not data:
            print("🔨 No more members to fetch.")
            break
        members.extend(data)
        print(f"🔨 Fetched {len(data)} members from page {page}.")
        page += 1
    print("🔨 Total members fetched:", len(members))
    return members

def analyze_projects(projects, year):
    """Analyze projects to gather various statistics."""
    print("🔨 Analyzing projects...")
    total_projects = len(projects)
    archived_projects = sum(1 for project in projects if project.get('archived', False))
    forked_projects = sum(1 for project in projects if project.get('fork', False))
    non_forked_projects = total_projects - forked_projects 

    # Most stars and most forks
    most_stars_project = max(projects, key=lambda p: p.get('star_count', 0), default=None)
    most_forks_project = max(projects, key=lambda p: p.get('forks_count', 0), default=None)

    # Count projects created in a specific year
    year_projects = sum(1 for project in projects if datetime.strptime(project['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').year == year)

    print("🔨 Analysis complete.")
    return {
        "total_projects": total_projects,
        "archived_projects": archived_projects,
        "forked_projects": forked_projects,
        "non_forked_projects": non_forked_projects,
        "most_stars_project": most_stars_project,
        "most_forks_project": most_forks_project,
        "year_projects": year_projects,
    }

# Services - Main
# ---------------

def main():
    """Main function to execute the analysis."""
    check_prerequisites()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description=f"Analyze GitLab organization groups and projects (Version: {VERSION}).")
    parser.add_argument("--year", type=int, required=True, help="The year to analyze (e.g., 2024).")
    args = parser.parse_args()

    start_time = time.time()

    subgroups = get_subgroups()
    all_projects = []

    for subgroup in subgroups:
        projects = get_projects(subgroup['id'])
        all_projects.extend(projects)

    total_members = get_members()
    visible_members = len(total_members)

    # Analyze projects for the specified year
    analysis = analyze_projects(all_projects, args.year)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Print the analysis results
    print("\n-----------------------")
    print("Analysis results below:\n")
    print("👉 Total projects:", analysis["total_projects"], "\n")
    print("👉 Archived projects:", analysis["archived_projects"], "\n")
    print("👉 Forked projects:", analysis["forked_projects"], "\n")
    print("👉 Non-forked projects:", analysis["non_forked_projects"], "\n")
    print("👉 Most stars project:", analysis["most_stars_project"]["name"] if analysis["most_stars_project"] else "N/A", "\n")
    print("👉 Most forks project:", analysis["most_forks_project"]["name"] if analysis["most_forks_project"] else "N/A", "\n")
    print("👉 Projects created in", args.year, ":", analysis["year_projects"], "\n")
    print("👉 Total members in organization (including outside collaborators):", len(total_members), "\n")
    print("👉 Visible members:", visible_members, "\n")
    print(f"\n⌛ Elapsed Time: {elapsed_time:.2f} seconds")  # Print elapsed time

# Services - Run
# --------------

if __name__ == "__main__":
    main()
