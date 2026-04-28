"""Build markdown card lists and metadata blocks from project data."""


from toolbox.models import ProjectInfo


def build_links(project: ProjectInfo) -> str:
    """
    Build the icon-link and social stats string for a project card.

    Format: plain link icons · release count icon · star count icon · fork count icon

    Parameters:
        project: Resolved project metadata.
    """
    link_icons = [
        f'[:fontawesome-brands-github:]({project.github_url} "GitHub")',
    ]
    reg_url = project.registry_url()
    reg_icon = project.registry_icon()
    reg_label = project.registry_label()
    if reg_url and reg_icon and reg_label:
        link_icons.append(f'[{reg_icon}]({reg_url} "{reg_label}")')
    if project.docs_url:
        link_icons.append(f'[:material-book-open-variant:]({project.docs_url} "Docs")')

    count_icons = []
    if project.release_count:
        count_icons.append(f'[:material-tag-multiple:](# "Releases") {project.release_count}')
    if project.stars:
        count_icons.append(f'[:material-star:](# "Stars") {project.stars}')
    if project.forks:
        count_icons.append(f'[:material-source-fork:](# "Forks") {project.forks}')

    lines = "\n".join(link_icons)
    if count_icons:
        lines += "\n·\n" + " ".join(count_icons)
    return lines


def build_meta_line(project: ProjectInfo) -> str:
    """
    Build a compact dot-separated metadata string for a project card.

    Parameters:
        project: Resolved project metadata.
    """
    fields = []
    if project.created:
        fields.append(f"**Created**: {project.created}")
    if project.released:
        fields.append(f"**Last Released**: {project.released}")
    if project.version:
        fields.append(f"**Version**: {project.version}")
    return " · ".join(fields)


def build_card(project: ProjectInfo, detail_page: str, heading: str = "##") -> str:
    """
    Build a card for a single project.

    Parameters:
        project:     Resolved project metadata.
        detail_page: Relative path to the project's detail page.
        heading:     Markdown heading prefix (e.g. `##` or `###`).
    """
    lang_icon = project.language_icon()
    name_link = f"[{project.repo}]({detail_page})"
    links = build_links(project)
    meta = build_meta_line(project)
    lines = [f"{heading} {lang_icon} {name_link}", "", f"*{project.description}*", "", links]
    if meta:
        lines += ["", meta]
    return "\n".join(lines)


def build_table(projects: list[ProjectInfo]) -> str:
    """
    Build a card list for a category page.

    Parameters:
        projects: List of resolved project metadata.
    """
    cards = []
    for p in projects:
        detail_page = f"{p.repo}.md"
        cards.append(build_card(p, detail_page))
    return "\n\n---\n\n".join(cards)


def build_highlights_table(
    projects: list[ProjectInfo],
    detail_pages: list[str],
) -> str:
    """
    Build the highlights card list for the home page.

    Parameters:
        projects:     List of resolved project metadata.
        detail_pages: Matching list of relative paths from the docs root.
    """
    cards = []
    for project, page in zip(projects, detail_pages):
        cards.append(build_card(project, page, heading="###"))
    return "\n\n---\n\n".join(cards)


CATEGORY_TITLES = {
    "libraries": "Libraries",
    "cli-tools": "CLI Tools",
    "mkdocs-plugins": "MkDocs Plugins",
    "templates": "Templates",
    "applications": "Applications",
}

CATEGORY_DESCRIPTIONS = {
    "libraries": "Packages you install and import into your own projects.",
    "cli-tools": "Command-line tools you install and run directly.",
    "mkdocs-plugins": "Plugins that extend MkDocs documentation sites.",
    "templates": "Project templates for bootstrapping new repositories.",
    "applications": "Standalone applications and personal tools.",
}


def build_category_page(category: str, projects: list[ProjectInfo]) -> str:
    """
    Build the full markdown source for a category index page.

    Parameters:
        category: Category key (e.g. `libraries`).
        projects: Resolved projects in this category.
    """
    title = CATEGORY_TITLES.get(category, category.replace("-", " ").title())
    description = CATEGORY_DESCRIPTIONS.get(category, "")
    cards = "\n\n---\n\n".join(build_card(p, f"{p.repo}.md") for p in projects)
    return f"# {title}\n\n{description}\n\n{cards}\n"


def build_detail_page(project: ProjectInfo) -> str:
    """
    Build the full markdown source for a project detail page.

    Parameters:
        project: Resolved project metadata, including cleaned README body.
    """
    links = build_links(project)
    meta = build_meta_line(project)
    parts = [f"# {project.repo}", "", project.description, "", links]
    if meta:
        parts += ["", meta]
    parts += ["", "---", ""]
    if project.readme:
        parts.append(project.readme)
    else:
        parts.append(
            '!!! info "No content available"\n'
            f"    This project's README is not in Markdown format. "
            f"Visit the [GitHub repository]({project.github_url}) for details."
        )
    parts.append("")
    return "\n".join(parts)
