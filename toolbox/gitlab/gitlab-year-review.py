import requests
from collections import Counter, defaultdict
from datetime import datetime
import time
import sys
import argparse
import os

# Version of the program
VERSION = "1.0.0"

# Configuration
ORG_NAME = "your-gitlab-organization"  # Remplacez par le nom de votre organisation GitLab
GITLAB_API_URL = f"https://gitlab.com/api/v4/groups/{ORG_NAME}/projects"
GITLAB_MEMBERS_URL = f"https://gitlab.com/api/v4/groups/{ORG_NAME}/members"

# Get the GitLab token from an environment variable
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")

HEADERS = {
    "Private-Token": GITLAB_TOKEN
}

def get_projects():
    """Fetch all projects for the organization.

    Returns:
        list: A list of project dictionaries.
    """
    print("Debug: Fetching projects...")
    projects = []
    page = 1
    while True:
        response = requests.get(f"{GITLAB_API_URL}?page={page}&per_page=100", headers=HEADERS)
        if response.status_code != 200:
            print("Debug: Failed to fetch projects, status code:", response.status_code)
            break
        data = response.json()
        if not data:
            print("Debug: No more projects to fetch.")
            break
        projects.extend(data)
        print(f"Debug: Fetched {len(data)} projects from page {page}.")
        page += 1
    print("Debug: Total projects fetched:", len(projects))
    return projects

def get_commits_count(project_id, year):
    """Fetch the number of commits for a given project within a specific year.

    Parameters:
        project_id (int): The ID of the project.
        year (int): The year to filter commits.

    Returns:
        int: The number of commits in the specified year.
    """
    print(f"Debug: Fetching commits for project ID: {project_id}...")
    commits_url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/commits"
    commits_count = 0
    page = 1

    # Define the date range for the specified year
    since = f"{year}-01-01T00:00:00Z"
    until = f"{year + 1}-01-01T00:00:00Z"

    while True:
        response = requests.get(f"{commits_url}?page={page}&per_page=100&since={since}&until={until}", headers=HEADERS)
        if response.status_code != 200:
            print("Debug: Failed to fetch commits, status code:", response.status_code)
            break
        data = response.json()
        if not data:
            print("Debug: No more commits to fetch for project ID:", project_id)
            break
        commits_count += len(data)
        print(f"Debug: Fetched {len(data)} commits from page {page}.")
        page += 1
    print(f"Debug: Total commits fetched for project ID {project_id}: {commits_count}")
    return commits_count

def get_members():
    """Fetch all members of the organization.

    Returns:
        list: A list of member dictionaries.
    """
    print("Debug: Fetching organization members...")
    members = []
    page = 1
    while True:
        response = requests.get(f"{GITLAB_MEMBERS_URL}?page={page}&per_page=100", headers=HEADERS)
        if response.status_code != 200:
            print("Debug: Failed to fetch members, status code:", response.status_code)
            break
        data = response.json()
        if not data:
            print("Debug: No more members to fetch.")
            break
        members.extend(data)
        print(f"Debug: Fetched {len(data)} members from page {page}.")
        page += 1
    print("Debug: Total members fetched:", len(members))
    return members

def analyze_projects(projects, year, count_commits):
    """
    Analyze projects to gather various statistics.

    Parameters:
    - projects (list): A list of project dictionaries fetched from the GitLab API.
    - year (int): The year for which to analyze contributions (e.g., 2024).
    - count_commits (bool): A flag indicating whether to count commits in the analysis.

    Returns:
    dict: A dictionary containing various statistics, including:
        - total_projects (int): Total number of projects.
        - total_commits (int): Total number of commits across all projects.
        - top_contributors_overall (list): Top contributors overall.
        - top_contributors_yearly (list): Top contributors for the specified year.
        - top_languages (list): Top programming languages used.
        - most_stars_project (dict): Project with the most stars.
        - most_forks_project (dict): Project with the most forks.
        - top_licenses (list): List of licenses used in projects.
        - year_projects (int): Number of projects created in the specified year.
    """
    print("Debug: Analyzing projects...")
    total_projects = len(projects)  # Total number of projects
    total_commits = 0
    total_contributor_commits = defaultdict(int)  # Total contributions
    yearly_contributor_commits = defaultdict(int)  # Contributions for the specified year
    languages = Counter()  # Count of programming languages used
    licenses = Counter()  # Count of licenses used
    most_stars_project = None
    most_forks_project = None
    year_projects = 0

    if count_commits:
        for project in projects:
            project_id = project['id']
            # Get commits for the specified year
            commits_count = get_commits_count(project_id, year)
            total_commits += commits_count
            
            # Get all commits for total contributor calculation
            all_commits_url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/commits"
            page = 1
            while True:
                response = requests.get(f"{all_commits_url}?page={page}&per_page=100", headers=HEADERS)
                if response.status_code != 200:
                    break
                commits_data = response.json()
                if not commits_data:
                    break
                for commit in commits_data:
                    author = commit['author_name']
                    total_contributor_commits[author] += 1  # Total contributions
                    # Check if the commit is in the specified year
                    commit_date = commit['created_at']
                    if year == datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%S.%fZ').year:
                        yearly_contributor_commits[author] += 1  # Contributions for the specified year
                page += 1
            print(f"Debug: Analyzing project {project['name']} (ID: {project_id})")

            # Count languages and licenses
            if 'languages' in project:
                languages[project['languages']] += 1
            if 'license' in project and project['license']:
                licenses[project['license']['name']] += 1

            # Track the most starred and forked projects
            if most_stars_project is None or project['star_count'] > most_stars_project['star_count']:
                most_stars_project = project
            if most_forks_project is None or project['forks_count'] > most_forks_project['forks_count']:
                most_forks_project = project

            # Count projects created in the specified year
            created_at = datetime.strptime(project['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            if created_at.year == year:
                year_projects += 1

    # Get the top 5 contributors overall
    top_contributors_overall = sorted(total_contributor_commits.items(), key=lambda x: x[1], reverse=True)[:5]

    # Get the top 10 contributors for the specified year
    top_contributors_yearly = sorted(yearly_contributor_commits.items(), key=lambda x: x[1], reverse=True)[:10]

    # Get the top programming languages used
    top_languages = languages.most_common(5)

    print("Debug: Analysis complete.")
    return {
        "total_projects": total_projects,
        "total_commits": total_commits,
        "top_contributors_overall": top_contributors_overall,
        "top_contributors_yearly": top_contributors_yearly,
        "top_languages": top_languages,
        "most_stars_project": most_stars_project,
        "most_forks_project": most_forks_project,
        "top_licenses": licenses.most_common(5),
        "year_projects": year_projects,
    }

def main():
    """Main function to execute the analysis."""
    # Check if the GitLab token and organization name are defined
    if GITLAB_TOKEN is None:
        print("Error: GitLab token is not defined. Please set the GITLAB_TOKEN environment variable.")
        sys.exit(1)

    if ORG_NAME is None or ORG_NAME.strip() == "":
        print("Error: Organization name is not defined. Please set the ORG_NAME variable.")
        sys.exit(1)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description=f"Analyze GitLab organization projects (Version: {VERSION}).")
    parser.add_argument("--year", type=int, required=True, help="The year to analyze (e.g., 2024).")
    parser.add_argument("--count-commits", action='store_true', help="Enable commit counting in the analysis.")
    args = parser.parse_args()

    start_time = time.time()  # Start timing

    projects = get_projects()  # Fetch all projects
    total_members = get_members()  # Total members including outside collaborators

    # Analyze projects for the specified year
    analysis = analyze_projects(projects, args.year, args.count_commits)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Print the analysis results
    print("\nAnalysis Results:")
    print("Total Projects:", analysis["total_projects"])
    print("Total Commits Across All Projects:", analysis["total_commits"])  # Print total commits

    # Print top contributors overall
    print("\nTop Contributors Overall:")
    for contributor, commits in analysis["top_contributors_overall"]:
        print(f"{contributor}: {commits} commits")

    # Print top contributors for the specified year
    print("\nTop Contributors for the Year:")
    for contributor, commits in analysis["top_contributors_yearly"]:
        print(f"{contributor}: {commits} commits")

    # Print top programming languages used
    print("\nTop Programming Languages Used:")
    for lang, count in analysis["top_languages"]:
        print(f"{lang}: {count} projects")

    # Print most starred and most forked projects
    if analysis["most_stars_project"]:
        print(f"\nMost Stars Project: {analysis['most_stars_project']['name']} with {analysis['most_stars_project']['star_count']} stars")
    if analysis["most_forks_project"]:
        print(f"Most Forks Project: {analysis['most_forks_project']['name']} with {analysis['most_forks_project']['forks_count']} forks")

    # Print top licenses used
    print("\nTop Licenses Used:")
    for license_name, count in analysis["top_licenses"]:
        print(f"{license_name}: {count} projects")

    # Print number of projects created in the specified year
    print(f"\nProjects Created in {args.year}: {analysis['year_projects']}")

    print(f"Elapsed Time: {elapsed_time:.2f} seconds")  # Print elapsed time

if __name__ == "__main__":
    main()
