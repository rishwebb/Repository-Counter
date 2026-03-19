# Repository Counter

![Repository Counter](https://img.shields.io/badge/Repository%20Counter-v1.0-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

---

<p align="center">
  <img alt="repo" src="https://raw.githubusercontent.com/rishwebb/Repository-Counter/main/.github/repo-illustration.png" width="420" onerror="this.style.display='none'" />
</p>

## ✨ What this is

`Repository Counter` is a tiny, practical Python utility that fetches and summarizes a GitHub user's repositories — grouped into Public and Private lists — using the GitHub REST API. It handles pagination, sorts results alphabetically, and prints a clean, copy-friendly summary.

The project includes a one-click launcher so you can run the tool locally with a saved token.

## 🔍 Features

- Fetch all repositories using the GitHub API (handles pagination)
- Separate repositories into Public and Private
- Sort both lists alphabetically (case-insensitive)
- Print counts and readable lists in a simple format
- Optional token support for private repo access
- Simple one-click `run.sh` launcher and local `.github_repo_summary.env` for convenience

## 💡 Quick Start

1. Clone or download this repo.

2. Add your credentials to the local env file (already included for convenience):

```bash
# .github_repo_summary.env
GITHUB_USERNAME="your-username"
GITHUB_TOKEN="your-personal-access-token"
```

> This repository includes `.gitignore` to prevent accidentally committing your token. Keep the env file private.

3. Run the script (one-click):

```bash
bash run.sh
```

Or run the Python script directly:

```bash
python3 github_repo_summary.py your-username
# or authenticated:
python3 github_repo_summary.py --token YOUR_TOKEN
```

## 🖼️ Output Format

The script prints exactly this layout:

```
Public Repos Total: 12
- repo-name-1
- repo-name-2
...

Private Repos Total: 4
- private-repo-1
- private-repo-2
...
```

If no token is provided, private repos are not shown and a note indicates authentication is required.

## ⚙️ Implementation Notes

- Uses the `requests` library and the GitHub REST API endpoints:
  - Authenticated: `https://api.github.com/user/repos`
  - Public-only: `https://api.github.com/users/{username}/repos`
- Pagination handled with `per_page=100` and looping through pages.
- Sorting is case-insensitive via `str.lower`.

## 🛡️ Security & Best Practices

- Do not commit tokens to source control.
- Use the provided `.gitignore` which excludes `.github_repo_summary.env`.
- Consider using a credential helper or OS keyring instead of a plaintext env file for long-term use.

## 📦 Files

- `github_repo_summary.py` — main Python script
- `run.sh` — one-click launcher (pauses for a keypress on interactive terminals)
- `.github_repo_summary.env` — local env file (ignored by git)
- `.gitignore` — ignores `.github_repo_summary.env` and `__pycache__/`

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome. Open an issue or submit a PR.

## 📜 License

This project is provided under the MIT License.

---

Made with ❤️ by rishwebb
