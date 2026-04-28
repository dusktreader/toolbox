"""
CLI for refreshing project metadata on the toolbox site.

Reads projects.yaml, fetches version and release data from PyPI and GitHub,
then writes category index pages and project detail pages wholesale.
"""


import time
from pathlib import Path

import typer
import yaml

from toolbox.api import build_client, get_github_token, resolve_project
from toolbox.inject import inject_table
from toolbox.models import ProjectInfo
from toolbox.tables import build_category_page, build_detail_page, build_highlights_table

app = typer.Typer(help="Refresh project metadata for dusktreader's toolbox site.")

DOCS_DIR = Path("docs")
PROJECTS_FILE = Path("projects.yaml")

# Projects featured on the home page highlights table, as (category, repo) pairs.
HIGHLIGHTS = [
    ("libraries", "flask-praetorian"),
    ("libraries", "py-buzz"),
    ("libraries", "typerdrive"),
    ("libraries", "snick"),
    ("cli-tools", "smart-letters"),
]


def _resolve_all(registry: dict) -> dict[str, list[ProjectInfo]]:
    """
    Resolve every project in the registry, grouped by category.

    Returns a dict mapping category names (like `libraries`) to lists of
    resolved `ProjectInfo` objects. A single HTTP client is shared across all
    requests.
    """
    token = get_github_token()
    if not token:
        typer.echo(
            "WARNING: gh CLI not found or not authenticated. "
            "GitHub API calls will be unauthenticated (60 req/hr limit)."
        )

    resolved: dict[str, list[ProjectInfo]] = {}

    with build_client(token) as client:
        for cat_name, entries in registry.items():
            typer.echo(f"Processing {cat_name} ({len(entries)} projects)...")

            projects: list[ProjectInfo] = []
            for entry in entries:
                typer.echo(f"  Fetching {entry['repo']}...", nl=False)
                project = resolve_project(client, entry)
                v = project.version or "no version"
                r = project.release_count
                typer.echo(f" {v} ({r} releases)")
                projects.append(project)
                time.sleep(0.1)  # Be polite to APIs

            resolved[cat_name] = projects

    return resolved


def _write_category_pages(resolved: dict[str, list[ProjectInfo]]) -> None:
    """Write each category index page wholesale."""
    for cat_name, projects in resolved.items():
        index_path = DOCS_DIR / cat_name / "index.md"
        index_path.write_text(build_category_page(cat_name, projects))
        typer.echo(f"  Wrote {index_path}")


def _write_project_pages(resolved: dict[str, list[ProjectInfo]]) -> None:
    """Write each project detail page wholesale."""
    for cat_name, projects in resolved.items():
        for project in projects:
            page_path = DOCS_DIR / cat_name / f"{project.repo}.md"
            page_path.write_text(build_detail_page(project))


def _inject_highlights(resolved: dict[str, list[ProjectInfo]]) -> None:
    """
    Update the highlights table on the home page.

    Reuses already-resolved project data instead of making redundant API calls.
    """
    typer.echo("Updating home page highlights...")

    highlight_projects: list[ProjectInfo] = []
    detail_pages: list[str] = []

    for cat_name, repo_name in HIGHLIGHTS:
        projects = resolved.get(cat_name, [])
        match = next((p for p in projects if p.repo == repo_name), None)
        if match:
            highlight_projects.append(match)
            detail_pages.append(f"{cat_name}/{repo_name}.md")

    if not highlight_projects:
        typer.echo("  WARNING: no highlight projects found")
        return

    table = build_highlights_table(highlight_projects, detail_pages)
    index_path = DOCS_DIR / "index.md"
    if index_path.exists():
        inject_table(index_path, "highlights", table)
        typer.echo(f"  Updated {index_path}")


@app.command()
def refresh(
    projects_file: Path = typer.Option(
        PROJECTS_FILE,
        "--projects",
        "-p",
        help="Path to the projects.yaml registry file.",
    ),
    docs_dir: Path = typer.Option(
        DOCS_DIR,
        "--docs",
        "-d",
        help="Path to the docs directory.",
    ),
) -> None:
    """Fetch project data from PyPI and GitHub and update the site markdown."""
    global DOCS_DIR, PROJECTS_FILE
    DOCS_DIR = docs_dir
    PROJECTS_FILE = projects_file

    if not PROJECTS_FILE.exists():
        typer.echo(f"Error: {PROJECTS_FILE} not found", err=True)
        raise typer.Exit(code=1)

    registry = yaml.safe_load(PROJECTS_FILE.read_text())
    resolved = _resolve_all(registry)
    _write_category_pages(resolved)
    _write_project_pages(resolved)
    _inject_highlights(resolved)

    typer.echo("Done.")


def main() -> None:
    """Entry point for the CLI."""
    app()
