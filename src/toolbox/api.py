import os
import re
import subprocess

import httpx
import snick

from toolbox.models import ProjectInfo

GITHUB_OWNER = "dusktreader"
REGISTRY_FETCH_URL = {"pypi.org": "https://pypi.org/pypi/{package_name}/json"}
BADGE_PATTERN = re.compile(r"^\[?\!\[.*?\]\((https?://(img\.shields\.io|github\.com/.+/badge\.svg).*?)\)\]?(\(.*?\))?$")
BLOB_IMAGE_PATTERN = re.compile(r"https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+?\.(png|jpg|jpeg|gif|svg|webp))")


def get_github_token() -> str | None:
    """
    Retrieve a GitHub auth token.

    Checks the `GH_TOKEN` and `GITHUB_TOKEN` environment variables first,
    then falls back to the `gh auth token` CLI command.

    Returns:
        The token string if available, or None.
    """
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token

    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def build_client(github_token: str | None = None) -> httpx.Client:
    """
    Build an HTTP client, optionally authenticated for GitHub.

    Parameters:
        github_token: GitHub personal access token. If provided, it will be
                      included as a Bearer token in the `Authorization` header.
    """
    headers = {}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
    return httpx.Client(headers=headers, timeout=5.0)


def fetch_registry(client: httpx.Client, registry: str, package_name: str) -> dict:
    """
    Fetch package metadata from a package registry JSON API.

    Parameters:
        client:       Reusable HTTP client.
        registry:     Registry hostname (e.g. `pypi.org`).
        package_name: Package name on the registry.
    """
    template = REGISTRY_FETCH_URL.get(registry)
    if not template:
        raise ValueError(f"Unsupported registry: {registry!r}")
    url = template.format(package_name=package_name)
    resp = client.get(url)
    resp.raise_for_status()
    return resp.json()


def fetch_github_repo(client: httpx.Client, repo: str) -> dict:
    """
    Fetch repository metadata from the GitHub API.

    Parameters:
        client: Reusable HTTP client.
        repo:   Repository name (without owner).
    """
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}"
    resp = client.get(url)
    resp.raise_for_status()
    return resp.json()


def fetch_readme(client: httpx.Client, repo: str) -> str:
    """
    Fetch the raw README from GitHub, handling any filename or extension.

    Uses the GitHub API to discover the README download URL, then fetches
    the raw content. Only returns content for Markdown files; RST and other
    formats are skipped since they cannot be embedded directly in MkDocs pages.

    Parameters:
        client: Reusable HTTP client.
        repo:   Repository name (without owner).

    Returns:
        Raw README text.
    """
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/readme"
    resp = client.get(url, headers={"Accept": "application/vnd.github.v3+json"})
    resp.raise_for_status()
    data = resp.json()
    name = data.get("name", "")
    if not name.lower().endswith(".md"):
        raise ValueError(f"README for {repo!r} is not a Markdown file: {name!r}")
    download_url = data.get("download_url", "")
    if not download_url:
        raise ValueError(f"No download_url in README response for {repo!r}")
    raw = client.get(download_url)
    raw.raise_for_status()
    return raw.text


def clean_readme(text: str) -> str:
    """
    Strip badge lines and the leading title heading from a README.

    Removes:
    - The first `# heading` line (the repo title, already on the detail page)
    - Any line that is solely a badge image link (shields.io or GitHub Actions
      badge SVGs rendered as `[![...](url)](url)` or `![...](url)`)

    Rewrites GitHub blob image URLs to raw.githubusercontent.com so images
    render correctly outside of GitHub.

    Parameters:
        text: Raw README markdown.

    Returns:
        Cleaned markdown text with leading/trailing blank lines stripped.
    """

    lines = text.splitlines()
    out = snick.Conjoiner()
    skipped_title = False
    for line in lines:
        if not skipped_title and line.startswith("# "):
            skipped_title = True
            continue
        if BADGE_PATTERN.match(line.strip()):
            continue
        out.add(BLOB_IMAGE_PATTERN.sub(r"https://raw.githubusercontent.com/\1/\2/\3/\4", line), should_dedent=False)

    return str(out).strip()


def fetch_github_releases(client: httpx.Client, repo: str) -> list[dict]:
    """
    Fetch releases from the GitHub API.

    Parameters:
        client: Reusable HTTP client.
        repo:   Repository name (without owner).
    """
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/releases"
    resp = client.get(url)
    if resp.status_code == 404:
        return []
    resp.raise_for_status()
    return resp.json()


def fetch_github_tags(client: httpx.Client, repo: str) -> list[dict]:
    """
    Fetch tags from the GitHub API.

    Parameters:
        client: Reusable HTTP client.
        repo:   Repository name (without owner).
    """
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{repo}/tags"
    resp = client.get(url)
    if resp.status_code == 404:
        return []
    resp.raise_for_status()
    return resp.json()


def resolve_registry_info(client: httpx.Client, project: ProjectInfo) -> None:
    """
    Fill in version, release date, and release count from the package registry.

    Parameters:
        client:  Reusable HTTP client.
        project: Project to update in place.
    """
    if not project.package_name or not project.package_registry:
        return

    data = fetch_registry(client, project.package_registry, project.package_name)
    if not data:
        return

    info = data.get("info", {})
    releases = data.get("releases", {})

    project.version = info.get("version")
    project.release_count = len([v for v, files in releases.items() if files])

    if project.version and project.version in releases:
        files = releases[project.version]
        if files:
            upload_time = files[0].get("upload_time", "")
            if upload_time:
                project.released = upload_time[:10]


def resolve_github_info(client: httpx.Client, project: ProjectInfo) -> None:
    """
    Fill in version, release info, stars, and forks from GitHub.

    Only provides version data if the package registry didn't already supply it.

    Parameters:
        client:  Reusable HTTP client.
        project: Project to update in place.
    """
    repo_data = fetch_github_repo(client, project.repo)
    project.stars = repo_data.get("stargazers_count", 0)
    project.forks = repo_data.get("forks_count", 0)
    created_at = repo_data.get("created_at", "")
    if created_at:
        project.created = created_at[:10]

    releases = fetch_github_releases(client, project.repo)
    if releases:
        project.release_count = max(project.release_count, len(releases))
        if not project.version:
            latest = releases[0]
            project.version = latest.get("tag_name")
            published = latest.get("published_at", "")
            if published:
                project.released = published[:10]
        return

    if project.version:
        return

    tags = fetch_github_tags(client, project.repo)
    if tags:
        project.release_count = max(project.release_count, len(tags))
        project.version = tags[0].get("name")


def resolve_project(client: httpx.Client, entry: dict) -> ProjectInfo:
    """
    Build a ProjectInfo from a registry entry and API data.

    Parameters:
        client: Reusable HTTP client.
        entry:  Dict from projects.yaml.
    """
    project = ProjectInfo(
        repo=entry["repo"],
        language=entry["language"],
        package_name=entry.get("package_name"),
        package_registry=entry.get("package_registry"),
        description=entry["description"],
        docs_url=entry.get("docs_url"),
        github_url=f"https://github.com/{GITHUB_OWNER}/{entry['repo']}",
    )
    resolve_registry_info(client, project)
    resolve_github_info(client, project)
    try:
        project.readme = clean_readme(fetch_readme(client, project.repo))
    except (ValueError, httpx.HTTPStatusError):
        pass
    return project
