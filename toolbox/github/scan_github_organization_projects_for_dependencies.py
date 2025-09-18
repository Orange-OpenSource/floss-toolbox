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

"""
Script to scan all public repositories of a given GitHub organization
for the presence of dependencies defined in a side file.

- The list of dependencies must be provided as a text file, given
  as a command-line argument, with one dependency name per line.
- The script checks for common dependency files (package.json, requirements.txt, etc.)
  in the root of each repository. It does not check the dependencies versions.
- Requires a GitHub API token set in the environment variable GITHUB_TOKEN.

WARNING: This is just a non-invasive and side tool to check repositories online.
You should of course prefer use of tools plugged in your repos to look for vulnerabilities and keep
updated dependencies, for example:
- CodeQL: https://codeql.github.com/
- Syft: https://github.com/anchore/syft
- Grype: https://github.com/anchore/grype
- Dependabot: https://docs.github.com/en/code-security/getting-started/dependabot-quickstart-guide
- Renovate: https://github.com/renovatebot/renovate

The tool also checks the last state of the repository of the default branch. It does not look inside Git history.

WARNING: You may face API rate limits

How to set the GITHUB_TOKEN environment variable:
    On Linux/macOS:
        export GITHUB_TOKEN=your_personal_access_token
    On Windows (Command Prompt):
        set GITHUB_TOKEN=your_personal_access_token
    On Windows (PowerShell):
        $env:GITHUB_TOKEN="your_personal_access_token"

GitHub token permissions required:
    - For public repositories: The "public_repo" scope is sufficient.
    - For best results, generate a token with "public_repo" and "read:org" scopes.

Usage:
    python3.8 scan_github_organization_projects_for_dependencies.py <path/to/file_of_deps.txt>

Arguments:
    <path/to/file_of_deps.txt>    Path to the file containing dependency names (one per line), nothing ekse

Exit codes:
    0  Success
    1  GITHUB_TOKEN is not set
    2  Dependency file does not exist, is unreadable or empty    
"""

import base64
import os
import requests
import sys
import time

# ====== CONFIGURATION ======

# The GitHub organization name
GITHUB_ORGANIZATION = "Orange-OpenSource"

# Some files (and their locks) listing dependencies to look for.
# WARNING: List is not curated, files supposed to be accessible, and versions not managed
# NOTE: Comment the lines you do not want to process.
DEPENDENCY_FILES = [
    # JavaSript, Node.js (NPM, Yarn and PNPM)
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    # Rust
    #"Cargo.toml", "Cargo.lock",
    # Go
    #"go.mod", "go.sum",
    # Java, Kotlin (Maven, Gradle)
    #"pom.xml", "build.gradle", "build.gradle.kts", "gradle.lockfile",
    #"settings.gradle.kts",
    # Swift (Swift Package Manager, Cocoapods, Carthage)
    #"Package.swift", "Podfile", "Cartfile",
    #"Package.resolved", "Podfile.lock", "Cartfile.resolved",
    # Python
    #"requirements.txt","pyproject.toml", "Pipfile.lock", "conda-lock.yml", "poetry.lock",
    # Ruby
    #"Gemfile", "Gemfile.lock"
    # Flutter / Dart
    #"pubspec.yaml", "pubspec.lock"
]

# GitHub Personal Access Token to request GitHub API
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Headers containing the token for the GitHub API requests
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else "",
    "Accept": "application/vnd.github.v3+json"
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

def get_repos(org, headers):
    """
    Retrieves all public repositories for the specified organization via the GitHub API.

    Args:
        org (str): The GitHub organization name.
        headers (dict): HTTP headers including authorization.

    Returns:
        list: A list of repository metadata dictionaries.
    """
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}"
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"⚠️ Warning: Got status code {res.status_code} for repos request ({res.text}).")
            break
        data = res.json()
        if not data:
            break
        repos += data
        page += 1
    return repos

def get_default_branch(owner, repo, headers):
    """
    Returns the default branch name for the repo.

    Args:
        owner (str): Repository owner (organization or user).
        repo (str): Repository name.
        headers (dict): HTTP headers including authorization.

    Returns:
        str: Default branch name or "main" if not found.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"⚠️ Warning: Got status code {res.status_code} for default branch request ({res.text}).")
        return "main"
    data = res.json()
    return data.get("default_branch", "main")

def get_repo_tree(owner, repo, branch, headers):
    """
    Retrieves the full (recursive) file tree of a repo at the given branch.

    Args:
        owner (str): Repository owner (organization or user).
        repo (str): Repository name.
        branch (str): Branch name (usually the default branch).
        headers (dict): HTTP headers including authorization.

    Returns:
        list: A list of file metadata dictionaries (with 'path', 'type', etc.).
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"⚠️ Warning: Got status code {res.status_code} for repo tree request.")
        return []
    data = res.json()
    return data.get("tree", [])

def get_file_content_by_path(owner, repo, file_path, headers):
    """
    Fetches and decodes the content of a file at any path in a GitHub repository using the API.

    Args:
        owner (str): GitHub organization or user name.
        repo (str): Repository name.
        file_path (str): Path to the file in the repository.
        headers (dict): HTTP headers including authorization.

    Returns:
        str or None: The decoded file content as a string, or None if not found or unreadable.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"⚠️ Warning: Got status code {res.status_code} for file content request ({res.text}).")
        return None
    content = res.json()
    if isinstance(content, dict) and 'content' in content and content.get('encoding') == 'base64':
        return base64.b64decode(content['content']).decode('utf-8', errors='ignore')
    return None

def find_dependencies_in_text(text, deps):
    """
    Returns a list of dependencies found in the given text.

    Args:
        text (str): The file content to scan.
        deps (list): List of dependency names to search for.

    Returns:
        list: Dependencies from 'deps' found in 'text'.
    """
    found = []
    for dep in deps:
        if dep in text:
            found.append(dep)
    return found

def main():
    """
    Main function to orchestrate the scanning process.

    - Checks environment and command-line arguments.
    - Loads dependencies to look for.
    - Retrieves and scans all repositories for dependencies, wherever they are in the tree.
    - Prints a progress message every 10 repositories.
    - For each repository where a dependency is found, prints the repository and detected dependencies
    - Displays the elapsed time and the number of projects with found dependencies.
    """
    if not GITHUB_TOKEN:
        print("❌ Error: Please set the GITHUB_TOKEN environment variable with a valid GitHub personal access token.")
        sys.exit(EXIT_TOKEN_ISSUE)

    if len(sys.argv) < 2:
        print("Usage: python3.8 scan_github_organization_projects_for_dependencies.py path/to/deps.txt")
        sys.exit(EXIT_DEPENDENCIES_ISSUE)

    start_time = time.time()

    dependencies_file = sys.argv[1]
    loaded_dependencies = load_dependencies(dependencies_file)
    print(f"✅ Loaded '{len(loaded_dependencies)}' dependencies to check.")
    repos = get_repos(GITHUB_ORGANIZATION, HEADERS)
    print(f"✅ Found '{len(repos)}' repositories in '{GITHUB_ORGANIZATION}'.")

    repos_with_dependencies = 0

    for idx, repo in enumerate(repos, 1):
        if idx % 10 == 0 or idx == 1:
            print(f"🔎 Scanning repository {idx} / {len(repos)}...")
        repo_name = repo["name"]
        repo_url = repo["html_url"]
        branch = get_default_branch(GITHUB_ORGANIZATION, repo_name, HEADERS)
        tree = get_repo_tree(GITHUB_ORGANIZATION, repo_name, branch, HEADERS)
        found_deps = {}
        for file in tree:
            if file["type"] == "blob":
                filename = file["path"].split("/")[-1]
                if filename in DEPENDENCY_FILES:
                    content = get_file_content_by_path(GITHUB_ORGANIZATION, repo_name, file["path"], HEADERS)
                    if content:
                        deps_in_file = find_dependencies_in_text(content, loaded_dependencies)
                        if deps_in_file:
                            found_deps[file["path"]] = deps_in_file
        if found_deps:
            repos_with_dependencies += 1
            print(f"\n🎯 Repository: {repo_name}\nURL: {repo_url}")
            print("➡️ Dependencies found in these files:")
            for path, deps in found_deps.items():
                print(f"  {path}:")
                for dep in deps:
                    print(f"    - {dep}")
    
    elapsed_time = time.time() - start_time
    print("\n====== Scan summary ======")
    print(f"📝 Repositories with at least one found dependency: {repos_with_dependencies}")
    print(f"⌛ Elapsed time: {elapsed_time:.2f} seconds")

# ========= MAIN =========

if __name__ == "__main__":
    main()