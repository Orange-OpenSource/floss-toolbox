#!/usr/bin/env python3
"""
Scan recursively all projects in a GitLab group (including subgroups)
for the presence of dependencies (anywhere in the repo tree).

- The list of dependencies must be provided as a text file, given
  as a command-line argument, with one dependency name per line.
- The script checks for common dependency files (package.json, requirements.txt, etc.) anywhere in the repository.
- Requires a GitLab personal access token set in the environment variable GITLAB_TOKEN.

Usage:
    python scan_gitlab_organization_projects_for_dependencies.py <path/to/file_of_deps.txt>

Argument:
    <path/to/file_of_deps.txt>       Path to the file containing dependency names (one per line)

Token permissions: "api" scope is required.

Exit codes:
    0  Success
    1  GITLAB_TOKEN is not set
    2  Dependency file does not exist, is unreadable or empty  
"""

import base64
import os
import requests
import sys
import time

# ====== CONFIGURATION ======

# GitLab URL
GITLAB_URL = "https://gitlab.com"

# The GitLab organization name
GITLAB_ORGANIZATION = "Orange-OpenSource"

# Some files (and their locks) listing dependencies to look for.
# WARNING: List is not curated, files supposed to be accessible, and versions not managed
# NOTE: Comment the lines you do not want to process.
DEPENDENCY_FILES = [
    # JavaSript, Node.js (NPM, Yarn and PNPM)
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    # Rust
    "Cargo.toml", "Cargo.lock",
    # Go
    "go.mod", "go.sum",
    # Java, Kotlin (Maven, Gradle)
    "pom.xml", "build.gradle", "build.gradle.kts", "gradle.lockfile",
    "settings.gradle.kts",
    # Swift (Swift Package Manager, Cocoapods, Carthage)
    "Package.swift", "Podfile", "Cartfile",
    "Package.resolved", "Podfile.lock", "Cartfile.resolved",
    # Python
    "requirements.txt","pyproject.toml", "Pipfile.lock", "conda-lock.yml", "poetry.lock",
    # Ruby
    "Gemfile", "Gemfile.lock"
    # Flutter / Dart
    "pubspec.yaml", "pubspec.lock"
]

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")

HEADERS = {
    "Private-Token": GITLAB_TOKEN if GITLAB_TOKEN else "",
}

# ======== SERVICE ========

EXIT_OK = 0
EXIT_TOKEN_ISSUE = 1
EXIT_DEPENDENCIES_ISSUE = 2

def load_dependencies(file_path):
    """
    Reads a list of dependencies from a text file.

    Args:
        file_path (str): Path to the text file containing dependency names (one per line).

    Returns:
        list: A list of non-empty, stripped dependency names.

    Raises:
        SystemExit: If the file does not exist, is unreadable or empty (EXIT_DEPENDENCIES_ISSUE).
    """
    if not os.path.isfile(file_path):
        print(f"❌ Error: The file '{file_path}' does not exist.")
        sys.exit(EXIT_DEPENDENCIES_ISSUE)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            deps = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"❌ Error reading file '{file_path}': {e}")
        sys.exit(EXIT_DEPENDENCIES_ISSUE)
    if not deps:
        print(f"❌ Error: The file '{file_path}' is empty or contains no valid dependencies.")
        sys.exit(EXIT_DEPENDENCIES_ISSUE)
    return deps

def get_all_subgroups_and_projects(group_id_or_path):
    """
    Recursively get all subgroups and projects under a group.

    Args:
        group_id_or_path (str): Path or id of the groupe to process to get projects.
    
    Returns two lists: [group_ids], [project dicts]
    """
    group_ids = []
    projects = []

    def _explore_group(group_id_or_path):
        # Add current group id
        url = f"{GITLAB_URL}/api/v4/groups/{group_id_or_path}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(f"❌  Error: group {group_id_or_path} not found ({r.status_code}) ({r.text})")
            return
        group = r.json()
        group_id = group['id']
        group_ids.append(group_id)

        # List direct subgroups
        page = 1
        while True:
            url = f"{GITLAB_URL}/api/v4/groups/{group_id}/subgroups?per_page=100&page={page}"
            r = requests.get(url, headers=HEADERS)
            if r.status_code != 200:
                print(f"⚠️ Warning: Got status code {r.status_code} for explore group request ({r.text}).")
                break
            subgs = r.json()
            if not subgs:
                break
            for sg in subgs:
                _explore_group(sg['id'])
            page += 1

        # List projects in this group
        page = 1
        while True:
            url = f"{GITLAB_URL}/api/v4/groups/{group_id}/projects?per_page=100&page={page}&include_subgroups=false"
            r = requests.get(url, headers=HEADERS)
            if r.status_code != 200:
                print(f"⚠️ Warning: Got status code {r.status_code} for explore projects request ({r.text}).")
                break
            projs = r.json()
            if not projs:
                break
            projects.extend(projs)
            page += 1

    _explore_group(group_id_or_path)
    return group_ids, projects

def get_default_branch(project):
    """
    Returns the default branch name for the project dict.
    """
    return project.get("default_branch", "main")

def get_project_tree(project_id, branch):
    """
    Returns the full tree (recursive) of files in a project for a given branch.

    Args:
        project_id (str): Identifier of the proejct
        branch (str): Branch to process
    """
    file_list = []
    page = 1
    while True:
        url = f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/tree?ref={branch}&recursive=true&per_page=100&page={page}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(f"⚠️ Warning: Got status code {r.status_code} for project tree request ({r.text}).")
            break
        files = r.json()
        if not files:
            break
        file_list += files
        page += 1
    return file_list

def get_file_content(project_id, file_path, branch):
    """
    Fetch and decode the content of a file from a GitLab project.

    Args:
        project_id (str): Identifier of the proejct
        file_path (str): The path to the file in the proejct with content to get and process
        branch (str): Branch to process
    """
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/files/{requests.utils.quote(file_path, safe='')}/raw?ref={branch}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(f"⚠️ Warning: Got status code {r.status_code} for project files request ({r.text}).")
        return None
    return r.text

def find_dependencies_in_text(text, deps):
    """
    Returns a list of vulnerable dependencies found in the given text.

    Args:
        text (str): The content of a file which may contain one or several dependencies
        deps: All the dependencies to process
    """
    found = []
    for dep in deps:
        if dep in text:
            found.append(dep)
    return found

def main():
    if not GITLAB_TOKEN:
        print("❌ Error: Please set the GITLAB_TOKEN environment variable with a valid GitLab personal access token.")
        sys.exit(EXIT_TOKEN_ISSUE)

    start_time = time.time()
    dependencies_file = sys.argv[1]
    loaded_dependencies = load_dependencies(dependencies_file)
    print(f"✅ Loaded {len(loaded_dependencies)} dependencies to check.")

    print(f"🔎 Fetching all subgroups and projects in '{GITLAB_ORGANIZATION}' (this may take a while)...")
    group_ids, projects = get_all_subgroups_and_projects(GITLAB_ORGANIZATION)
    print(f"✅ Found {len(projects)} projects in {len(group_ids)} groups/subgroups.")

    repos_with_dependencies = 0

    for idx, project in enumerate(projects, 1):
        if idx % 10 == 0 or idx == 1:
            print(f"🔎 Scanning project {idx} / {len(projects)}...")
        project_id = project['id']
        project_name = project['path_with_namespace']
        project_url = project['web_url']
        branch = get_default_branch(project)
        if not branch:
            continue  # skip archived/empty projects
        tree = get_project_tree(project_id, branch)
        found_deps = {}
        for file in tree:
            if file.get("type") == "blob":
                filename = file["path"].split("/")[-1]
                if filename in DEPENDENCY_FILES:
                    content = get_file_content(project_id, file["path"], branch)
                    if content:
                        deps_in_file = find_dependencies_in_text(content, loaded_dependencies)
                        if deps_in_file:
                            found_deps[file["path"]] = deps_in_file
        if found_deps:
            repos_with_dependencies += 1
            print(f"\n🎯 Project: {project_name}\nURL: {project_url}")
            print("➡️ Dependencies found in these files:")
            for path, deps in found_deps.items():
                print(f"  {path}:")
                for dep in deps:
                    print(f"    - {dep}")

    elapsed_time = time.time() - start_time
    print("\n====== Scan summary ======")
    print(f"📝 Projects with at least one vulnerable dependency: {repos_with_dependencies}")
    print(f"⌛ Elapsed time: {elapsed_time:.2f} seconds")

# ========= MAIN =========

if __name__ == "__main__":
    main()