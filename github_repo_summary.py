#!/usr/bin/env python3
"""Display a GitHub repository summary (public/private) for a user."""

import argparse
import os
import sys
from typing import Dict, List, Optional

import requests

GITHUB_API_BASE = "https://api.github.com"
PER_PAGE = 100


def fetch_repos(url: str, headers: Dict[str, str]) -> List[dict]:
    """Fetch all repository pages from a GitHub API endpoint."""
    repos: List[dict] = []
    page = 1

    while True:
        response = requests.get(
            url,
            headers=headers,
            params={"per_page": PER_PAGE, "page": page},
            timeout=20,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"GitHub API request failed ({response.status_code}): {response.text}"
            )

        page_items = response.json()
        if not page_items:
            break

        repos.extend(page_items)

        if len(page_items) < PER_PAGE:
            break

        page += 1

    return repos


def get_authenticated_username(headers: Dict[str, str]) -> str:
    """Get the username tied to the provided token."""
    response = requests.get(f"{GITHUB_API_BASE}/user", headers=headers, timeout=20)
    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch authenticated user ({response.status_code}): {response.text}"
        )

    data = response.json()
    return data.get("login", "")


def split_and_sort_repos(repos: List[dict]) -> tuple[List[str], List[str]]:
    """Split repository names into public/private lists and sort alphabetically."""
    public_repos: List[str] = []
    private_repos: List[str] = []

    for repo in repos:
        repo_name = repo.get("name", "")
        if not repo_name:
            continue

        if repo.get("private", False):
            private_repos.append(repo_name)
        else:
            public_repos.append(repo_name)

    public_repos.sort(key=str.lower)
    private_repos.sort(key=str.lower)
    return public_repos, private_repos


def print_summary(public_repos: List[str], private_repos: List[str], token_provided: bool) -> None:
    """Print summary in the required output format."""
    print(f"Public Repos Total: {len(public_repos)}")
    for repo_name in public_repos:
        print(f"- {repo_name}")

    print("\n")
    print(f"Private Repos Total: {len(private_repos)}")
    for repo_name in private_repos:
        print(f"- {repo_name}")

    if not token_provided:
        print("Private repos require authentication.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Display GitHub repository summary grouped into public/private repos."
        )
    )
    parser.add_argument(
        "username",
        nargs="?",
        help=(
            "GitHub username to fetch public repositories for when no token is provided. "
            "Ignored when token is provided unless used only for display checks."
        ),
    )
    parser.add_argument(
        "--token",
        default=os.getenv("GITHUB_TOKEN"),
        help="GitHub personal access token (or set GITHUB_TOKEN env var).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token: Optional[str] = args.token

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"
        endpoint = f"{GITHUB_API_BASE}/user/repos"

        try:
            auth_login = get_authenticated_username(headers)
            if args.username and args.username != auth_login:
                print(
                    f"Note: token authenticates as '{auth_login}', so summary is for that user.",
                    file=sys.stderr,
                )
        except RuntimeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
    else:
        if not args.username:
            print(
                "Error: username is required when no token is provided.",
                file=sys.stderr,
            )
            return 1

        endpoint = f"{GITHUB_API_BASE}/users/{args.username}/repos"

    try:
        repos = fetch_repos(endpoint, headers)
        public_repos, private_repos = split_and_sort_repos(repos)
        if not token:
            private_repos = []
        print_summary(public_repos, private_repos, token_provided=bool(token))
        return 0
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print(f"Network error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
