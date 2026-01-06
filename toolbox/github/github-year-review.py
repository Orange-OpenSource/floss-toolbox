#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from collections import Counter, defaultdict
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import sys
import time

# Configuration - Tool
# --------------------

VERSION = "1.1.0"

ERROR_BAD_PREREQUISITES = 1

# Configuration - Load
# --------------------

load_dotenv()

# Configuration - GitHub
# ----------------------

# To create the GitHub Personal Access Token for the organization: https://github.com/settings/personal-access-tokens
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
# Organization to scan
ORGANIZATION_NAME =  os.getenv("ORGANIZATION_NAME")

# Configuration - Tunning
# -----------------------

# Number of top programming languages in use to extract
TOP_N_PROG_LANG = os.getenv("TOP_N_PROG_LANG")
# Number of programming languages the least used to extract
TOP_N_LEAST_PROG_LANG = os.getenv("TOP_N_LEAST_PROG_LANG")
# Number of top licenses in use to extract
TOP_N_LICENSES = os.getenv("TOP_N_LICENSES")
# Number of top contributors over all years
TOP_N_CONTRIBUTORS_OVERALL = os.getenv("TOP_N_CONTRIBUTORS_OVERALL")
# Number of top contributors over the specified year
TOP_N_CONTRIBUTORS_FOR_YEAR = os.getenv("TOP_N_CONTRIBUTORS_FOR_YEAR")
# Number of top repositories with the highest commits
TOP_N_REPOS_MOST_COMMITS = os.getenv("TOP_N_REPOS_MOST_COMMITS")

# Configuration - Endpoints
# -------------------------

GITHUB_API_URL = f"https://api.github.com/orgs/{ORGANIZATION_NAME}/repos"
ORG_MEMBERS_URL = f"https://api.github.com/orgs/{ORGANIZATION_NAME}/members"
OUTSIDE_COLLABORATORS_URL = f"https://api.github.com/orgs/{ORGANIZATION_NAME}/outside_collaborators"

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_API_TOKEN}"
}

# Services
# --------

def check_prerequisites():
    """Check if all configuration elements have been laoded through .env file.
    If not, exists.
    """
    if GITHUB_API_TOKEN is None:
        print("❌ Error: GitHub token is not defined. Please set the GITHUB_API_TOKEN environment variable.")
        sys.exit(ERROR_BAD_PREREQUISITES)

    if ORGANIZATION_NAME is None or ORGANIZATION_NAME.strip() == "":
        print("❌ Error: Organization name is not defined. Please set the ORGANIZATION_NAME variable.")
        sys.exit(ERROR_BAD_PREREQUISITES)

    if TOP_N_PROG_LANG is None or TOP_N_PROG_LANG.strip() == "":
        print("❌ Error: TOP_N_PROG_LANG is not defined. Please set the TOP_N_PROG_LANG variable.")
        sys.exit(ERROR_BAD_PREREQUISITES)

    if TOP_N_LEAST_PROG_LANG is None or TOP_N_LEAST_PROG_LANG.strip() == "":
        print("❌ Error: TOP_N_LEAST_PROG_LANG name is not defined. Please set the TOP_N_LEAST_PROG_LANG variable.")
        sys.exit(ERROR_BAD_PREREQUISITES)

    if TOP_N_LICENSES is None or TOP_N_LICENSES.strip() == "":
        print("❌ Error: TOP_N_LICENSES name is not defined. Please set the TOP_N_LICENSES variable.")
        sys.exit(ERROR_BAD_PREREQUISITES)

    if TOP_N_CONTRIBUTORS_OVERALL is None or TOP_N_CONTRIBUTORS_OVERALL.strip() == "":
        print("❌ Error: TOP_N_CONTRIBUTORS_OVERALL name is not defined. Please set the TOP_N_CONTRIBUTORS_OVERALL variable.")
        sys.exit(ERROR_BAD_PREREQUISITES)

    if TOP_N_CONTRIBUTORS_FOR_YEAR is None or TOP_N_CONTRIBUTORS_FOR_YEAR.strip() == "":
        print("❌ Error: TOP_N_CONTRIBUTORS_FOR_YEAR name is not defined. Please set the TOP_N_CONTRIBUTORS_FOR_YEAR variable.")
        sys.exit(ERROR_BAD_PREREQUISITES)

    if TOP_N_REPOS_MOST_COMMITS is None or TOP_N_REPOS_MOST_COMMITS.strip() == "":
        print("❌ Error: TOP_N_REPOS_MOST_COMMITS name is not defined. Please set the TOP_N_REPOS_MOST_COMMITS variable.")
        sys.exit(ERROR_BAD_PREREQUISITES)

def safe_api_request(url, headers, max_retries=3):
    """Make a safe API request with cooldown and retry logic."""
    for attempt in range(max_retries):
        try:
            time.sleep(1.0)
                
            response = requests.get(url, headers=headers)
                
            if response.status_code == 200:
                return response
            elif response.status_code == 403:
                print(f"⚠️  Rate limit hit (403), waiting 60 seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(60)
                continue
            elif response.status_code == 404:
                print(f"❌ Repository not found (404): {url}")
                return None
            else:
                print(f"❌ API error {response.status_code}: {url}")
                if attempt < max_retries - 1:
                    print(f"⚠️  Retrying in 5 seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(5)
                continue
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            if attempt < max_retries - 1:
                print(f"⚠️  Retrying in 5 seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(5)
            continue
        
    print(f"❌ Failed to fetch after {max_retries} attempts: {url}")
    return None

def get_repositories():
    """Fetch all repositories for the organization.

    Returns:
        list: A list of repository dictionaries.
    """
    print("🔨 Fetching repositories...")
    repos = []
    page = 1
    while True:

        url = f"{GITHUB_API_URL}?page={page}&per_page=100"
        response = safe_api_request(url, HEADERS)
        if response is None:
            break

        data = response.json()
        if not data:
            print("🔨 No more repositories to fetch.")
            break

        repos.extend(data)
        print(f"🔨 Fetched {len(data)} repositories from page {page}.")
        page += 1
    print("🔨 Total repositories fetched:", len(repos))
    return repos

def get_commits_count(repo_full_name, year):
    """Fetch the number of commits for a given repository within a specific year.

    Parameters:
        repo_full_name (str): The full name of the repository (e.g., "owner/repo").
        year (int): The year to filter commits.

    Returns:
        int: The number of commits in the specified year.
    """
    print(f"🔨 Fetching commits for repository: {repo_full_name}...")
    commits_url = f"https://api.github.com/repos/{repo_full_name}/commits"
    commits_count = 0
    page = 1

    # Define the date range for the specified year
    since = f"{year}-01-01T00:00:00Z"
    until = f"{year + 1}-01-01T00:00:00Z"

    while True:
        url = f"{commits_url}?page={page}&per_page=100&since={since}&until={until}"
        response = safe_api_request(url, HEADERS)
        if response is None:
            break

        data = response.json()
        if not data:
            print("🔨 No more commits to fetch for repository:", repo_full_name)
            break

        commits_count += len(data)
        print(f"🔨 Fetched {len(data)} commits from page {page}.")
        page += 1
    print(f"🔨 Total commits fetched for repository {repo_full_name}: {commits_count}")
    return commits_count

def get_members():
    """Fetch all members of the organization.

    Returns:
        list: A list of member dictionaries.
    """
    print("🔨 Fetching organization members...")
    members = []
    page = 1
    while True:
        url = f"{ORG_MEMBERS_URL}?page={page}&per_page=100"
        response = safe_api_request(url, HEADERS)
        if response is None:
            break

        data = response.json()
        if not data:
            print("🔨 No more members to fetch.")
            break

        members.extend(data)  # Add the fetched members to the list
        print(f"🔨 Fetched {len(data)} members from page {page}.")
        page += 1  # Move to the next page
    print("🔨 Total members fetched:", len(members))
    return members

def get_outside_collaborators():
    """Fetch all outside collaborators of the organization.

    Returns:
        list: A list of outside collaborator dictionaries.
    """
    print("🔨 Fetching outside collaborators...")
    collaborators = []
    page = 1
    while True:
        url = f"{OUTSIDE_COLLABORATORS_URL}?page={page}&per_page=100"
        response = safe_api_request(url, HEADERS)
        if response is None:
            break

        data = response.json()
        if not data:
            print("🔨 No more outside collaborators to fetch.")
            break  # Exit loop if no more data is returned

        collaborators.extend(data)
        print(f"🔨 Fetched {len(data)} outside collaborators from page {page}.")
        page += 1
    print("🔨 Total outside collaborators fetched:", len(collaborators))
    return collaborators

def analyze_repositories(repos, year, count_commits, allowed_domains, forbidden_repos):
    """
    Analyze repositories to gather various statistics.

    Parameters:
    - repos (list): A list of repository dictionaries fetched from the GitHub API.
    - year (int): The year for which to analyze contributions (e.g., 2025).
    - count_commits (bool): A flag indicating whether to count commits in the analysis.
    - allowed_domains (list): List of allowed email domains (e.g., ["@orange.com", "@sofrecom.com"])
    - forbidden_repos (list): List of repository names to ignore (because of too big, no contributions, etc.) (e.g., ["Orange-OpenSource/linux"])

    Returns:
    dict: A dictionary containing various statistics, including:
        - total_repos (int): Total number of repositories.
        - archived_repos (int): Number of archived repositories.
        - forked_repos (int): Number of forked repositories.
        - non_forked_repos (int): Number of non-forked repositories.
        - total_forks (int): Total number of forks across all repositories.
        - most_stars_repo (dict): Repository with the most stars.
        - most_forks_repo (dict): Repository with the most forks.
        - top_languages (list): List of the top programming languages used.
        - total_lines (dict): Total lines of code for the top programming languages.
        - top_licenses (list): List of the top licenses used in repositories.
        - year_repos (int): Number of repositories created in the specified year.
        - organization_forks_year (int): Number of forks created by the organization the given year.
        - total_commits (int): Total number of commits across all repositories.
        - top_repos (list): Top repositories by commits.
        - top_contributors_overall (list): Top contributors overall (filtered by domain).
        - top_contributors_yearly (list): Top contributors for the specified year (filtered by domain).
        - least_used_languages (list): Least used programming languages.
        - largest_projects (dict): Largest project for each programming language.
        - filtered_commits_yearly (int): Number of commits by allowed domain users for the year.
        - filtered_commits_total (int): Total number of commits by allowed domain users.
        - skipped_repos (list): List of repositories that were skipped.
    """
    print("🔨 Analyzing repositories...")
    
    print(f"🔨 Filtering contributors by domains: {allowed_domains}")
    print(f"🔨 Ignoring forbidden repositories: {forbidden_repos}")
    
    def is_allowed_email(email):
        """Check if an email belongs to allowed domains."""
        if not email:
            return False
        return any(email.lower().endswith(domain.lower()) for domain in allowed_domains)
    
    def is_forbidden_repo(repo_full_name):
        """Check if a repository is in the forbidden list."""
        return repo_full_name in forbidden_repos
        
    # Basic repository statistics
    total_repos = len(repos)
    archived_repos = sum(1 for repo in repos if repo['archived'])
    forked_repos = sum(1 for repo in repos if repo['fork'])
    non_forked_repos = total_repos - forked_repos

    # Total forks count from all repositories
    total_forks = sum(repo['forks_count'] for repo in repos)

    # Number of forks created the given year
    organization_forks_year = sum(1 for repo in repos if repo['fork'] and datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ').year == year)

    # Stars count and identifying the most starred and forked repositories
    stars_count = sum(repo['stargazers_count'] for repo in repos)
    most_stars_repo = max(repos, key=lambda r: r['stargazers_count'], default=None)
    most_forks_repo = max(repos, key=lambda r: r['forks_count'], default=None)

    # Initialize data structures for language and contributor analysis
    languages = Counter()
    largest_projects = {}
    total_contributor_commits = defaultdict(int)  # Total contributions (filtered)
    yearly_contributor_commits = defaultdict(int)  # Yearly contributions (filtered)

    # Analyze programming language
    for repo in repos:
        if repo['language']:
            languages[repo['language']] += 1
            if repo['language'] not in largest_projects or repo['size'] > largest_projects[repo['language']]['size']:
                largest_projects[repo['language']] = {'name': repo['full_name'], 'size': repo['size']}

    # Get the top programming languages used
    top_languages = languages.most_common(int(TOP_N_PROG_LANG))
    total_lines = {lang: 0 for lang, _ in top_languages}
    
    # Estimate total lines of code for top languages
    for repo in repos:
        if repo['language'] in total_lines:
            total_lines[repo['language']] += repo['size']

    # Count repositories created in the specified year
    year_repos = sum(1 for repo in repos if datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ').year == year)

    # Count forks created by the organization
    organization_forks = sum(1 for repo in repos if repo['fork'])

    # Count licenses used in the repositories
    licenses = Counter(repo['license']['name'] for repo in repos if repo['license'])
    top_licenses = licenses.most_common(int(TOP_N_LICENSES))

    # Initialize commit-related variables
    total_commits = 0  # Total commits (all contributors)
    commits_per_repo = {}  # Commits per repo (all contributors)
    filtered_commits_yearly = 0  # Commits by allowed domain users (yearly)
    filtered_commits_total = 0   # Commits by allowed domain users (total)
    skipped_repos = []  # List of skipped repositories

    # Calculate commits and contributor statistics if enabled
    if count_commits:
        for index, repo in enumerate(repos, start=1):
            # Ignore repos to ignore
            if is_forbidden_repo(repo['full_name']):
                print(f"🚫 SKIPPING forbidden repository {index}/{total_repos}: {repo['full_name']}")
                skipped_repos.append(repo['full_name'])
                continue
            
            print(f"🔨 Analyzing repository {index}/{total_repos}: {repo['full_name']} {'(FORK)' if repo['fork'] else ''} {'(ARCHIVED)' if repo['archived'] else ''}")
            
            # Define date range for the specified year
            since = f"{year}-01-01T00:00:00Z"
            until = f"{year + 1}-01-01T00:00:00Z"
            
            # Stats for specified year
            yearly_commits_url = f"https://api.github.com/repos/{repo['full_name']}/commits"
            page = 1
            yearly_commits_count = 0
            yearly_filtered_commits = 0

            print(f"🔨 Fetching yearly commits and contributors for {repo['full_name']}...")
            while True:
                url = f"{yearly_commits_url}?page={page}&per_page=100&since={since}&until={until}"
                response = safe_api_request(url, HEADERS)
                if response is None:
                    break

                commits_data = response.json()
                if not commits_data:
                    break
                
                # Stats for all years
                if author_email and is_allowed_email(author_email):
                    yearly_filtered_commits += 1
                
                # Analyse contributions by year (with domain filtering)
                for commit in commits_data:
                    if commit.get('commit') and commit['commit'].get('author'):
                        author_name = commit['commit']['author'].get('name')
                        author_email = commit['commit']['author'].get('email')
                        
                        # Email domain filtering
                        if author_email and is_allowed_email(author_email):
                            if author_name:
                                yearly_contributor_commits[f"{author_name} ({author_email})"] += 1
                            yearly_filtered_commits += 1
                page += 1

            # Store only commits count for allowed domains
            total_commits += yearly_filtered_commits
            commits_per_repo[repo['full_name']] = yearly_filtered_commits

            # Compute all commits for all contributors
            print(f"🔨 Fetching all-time contributors for {repo['full_name']}...")
            all_commits_url = f"https://api.github.com/repos/{repo['full_name']}/commits"
            page = 1
            
            while True:
                url = f"{all_commits_url}?page={page}&per_page=100"
                response = safe_api_request(url, HEADERS)
                
                if response is None:
                    break
                
                commits_data = response.json()
                if not commits_data:
                    break

                # Analyse overall contributions (with domain filtering)
                for commit in commits_data:
                    if commit.get('commit') and commit['commit'].get('author'):
                        author_name = commit['commit']['author'].get('name')
                        author_email = commit['commit']['author'].get('email')
                        
                        # Filter by email domain
                        if author_email and is_allowed_email(author_email):
                            if author_name:
                                total_contributor_commits[f"{author_name} ({author_email})"] += 1
                page += 1

    # Calculate top contributors (with filtering on domains)
    top_contributors_overall = sorted(total_contributor_commits.items(), key=lambda x: x[1], reverse=True)[:int(TOP_N_CONTRIBUTORS_OVERALL)]
    top_contributors_yearly = sorted(yearly_contributor_commits.items(), key=lambda x: x[1], reverse=True)[:int(TOP_N_CONTRIBUTORS_FOR_YEAR)]

    # Get the top repositories with the most commits (only allowed commits)
    # Filter repos with no commits from allowed domains
    filtered_commits_per_repo = {repo: commits for repo, commits in commits_per_repo.items() if commits > 0}
    top_repos = sorted(filtered_commits_per_repo.items(), key=lambda x: x[1], reverse=True)[:int(TOP_N_REPOS_MOST_COMMITS)]

    # Get the least used programming languages
    least_used_languages = sorted(languages.items(), key=lambda x: x[1])[:int(TOP_N_LEAST_PROG_LANG)]

    print("🔨 Analysis complete.")
    print(f"🔨 Total commits (all contributors): {total_commits}")
    print(f"🔨 Filtered commits yearly (allowed domains): {filtered_commits_yearly}")
    print(f"🔨 Filtered commits total (allowed domains): {filtered_commits_total}")
    print(f"🔨 Skipped repositories: {len(skipped_repos)}")
    
    return {
        "total_repos": total_repos,
        "archived_repos": archived_repos,
        "forked_repos": forked_repos,
        "non_forked_repos": non_forked_repos,
        "total_forks": total_forks,
        "most_stars_repo": most_stars_repo,
        "most_forks_repo": most_forks_repo,
        "top_languages": top_languages,
        "total_lines": total_lines,
        "top_licenses": top_licenses,
        "year_repos": year_repos,
        "organization_forks_year": organization_forks_year,
        "total_commits": total_commits,
        "top_repos": top_repos,
        "top_contributors_overall": top_contributors_overall,
        "top_contributors_yearly": top_contributors_yearly,
        "least_used_languages": least_used_languages,
        "largest_projects": largest_projects,
        "filtered_commits_yearly": filtered_commits_yearly,
        "filtered_commits_total": filtered_commits_total,
        "skipped_repos": skipped_repos
    }


def get_total_members():
    """Get the total number of members including outside collaborators.

    Returns:
        int: Total number of members in the organization.
    """
    print("🔨 Fetching total members...")
    members = get_members()
    outside_collaborators = get_outside_collaborators()
    total = len(members) + len(outside_collaborators)
    print("🔨 Total members including outside collaborators:", total)
    return total

def estimate_private_members(total_members, visible_members):
    """Estimate the number of private members in the organization.

    Parameters:
        total_members (int): Total number of members including outside collaborators.
        visible_members (int): Number of visible members.

    Returns:
        int: Estimated number of private members.
    """
    private_members = total_members - visible_members
    print("🔨 Estimated private members:", private_members)
    return private_members

# Services - Main
# ---------------

def main():
    """Main function to execute the analysis."""

    check_prerequisites()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description=f"Analyze GitHub organization repositories (Version: {VERSION}).")
    parser.add_argument("--year", type=int, required=True, help="The year to analyze (e.g., 2025).")
    parser.add_argument("--count-commits", action='store_true', help="Enable commit counting in the analysis.")
    args = parser.parse_args()

    start_time = time.time()

    repos = get_repositories()
    total_members = get_total_members()
    visible_members = len(get_members())

    # Compute only employees / subscontractors / affiliate top domain of addresses:
    # - Orange employees and external people are expected to have orange.com
    # - Sofrecom affiliate employees and external people are expected to have sofrecom.com
    # - Some interns from sciencespo.fr contributed to the project
    # - Some subcontractors from groupeonepoint.com too
    # - And also some partner from inria.fr
    allowed_domains = ["@orange.com", "@sofrecom.com", "@groupeonepoint.com", "@sciencespo.fr", "@inria.fr"]    
    # Exclude some repositories if they pollute results
    forbidden_repos = [ "Orange-OpenSource/linux"]
    
    # Analyze repositories for the specified year
    analysis = analyze_repositories(repos, args.year, args.count_commits, allowed_domains, forbidden_repos)

    # Estimate the number of private members
    private_members_count = estimate_private_members(total_members, visible_members)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Print the analysis results
    print("\n-----------------------")
    print("Analysis results below:\n")
    print("👉 Total repositories:", analysis["total_repos"], "\n")
    print("👉 Archived repositories:", analysis["archived_repos"], "\n")
    print("👉 Forked repositories:", analysis["forked_repos"], "\n")
    print("👉 Non-forked repositories:", analysis["non_forked_repos"], "\n")
    print("👉 Total forks:", analysis["total_forks"], "\n")
    print("👉 Most stars repository:", analysis["most_stars_repo"]["name"] if analysis["most_stars_repo"] else "N/A", "\n")
    print("👉 Most forks repository:", analysis["most_forks_repo"]["name"] if analysis["most_forks_repo"] else "N/A", "\n")
    print("👉 Top languages:", analysis["top_languages"], "\n")
    print("👉 Total lines of code for topl anguages:", analysis["total_lines"], "\n")
    print("👉 Top licenses:", analysis["top_licenses"], "\n")
    print("👉 Total members in organization (including outside collaborators):", total_members, "\n")
    print("👉 Visible members:", visible_members, "\n")
    print("👉 Estimated private members:", private_members_count, "\n")
    print("👉 Repositories created in", args.year, ":", analysis["year_repos"], "\n")
    print("👉 Forks created by the organization in", args.year, ":", analysis["organization_forks_year"], "\n")

    if args.count_commits:
        print("👉 Total commits across all repositories:", analysis["total_commits"]) 

        # Print top repositories by commits
        print(f"\n💪 Top {TOP_N_REPOS_MOST_COMMITS} repositories by commits:")
        for repo, commits in analysis["top_repos"]:
            print(f"\t{repo}: {commits} commits")

        # Print top 5 contributors overall
        print(f"\n💪 Top {TOP_N_CONTRIBUTORS_OVERALL} contributors overall:")
        for contributor, commits in analysis["top_contributors_overall"]:
            print(f"\t{contributor}: {commits} commits")

        # Print top 10 contributors for the specified year
        print(f"\n💪 Top {TOP_N_CONTRIBUTORS_FOR_YEAR} contributors for the year:")
        for contributor, commits in analysis["top_contributors_yearly"]:
            print(f"\t{contributor}: {commits} commits")
        print(f"\n")
    
    # Print the 3 least used programming languages
    print(f"💪 {TOP_N_LEAST_PROG_LANG} least used programming languages:")
    for lang, count in analysis["least_used_languages"]:
        print(f"\t{lang}: {count} repositories")

    # Print the largest project for each of the top programming languages
    print("\n💪 Largest project for each top programming language:")
    for lang, _ in analysis["top_languages"]:
        if lang in analysis["largest_projects"]:
            largest_project = analysis["largest_projects"][lang]
            print(f"\t{lang}: {largest_project['name']} (Size: {largest_project['size']} KB)")
        else:
            print(f"\t{lang}: Only forks available.")

    print(f"\n⌛ Elapsed Time: {elapsed_time:.2f} seconds")  # Print elapsed time

# Services - Run
# --------------

if __name__ == "__main__":
    main()