"""Data models for project metadata."""


from dataclasses import dataclass

LANGUAGE_ICONS = {
    "python": ":fontawesome-brands-python:",
    "go": ":simple-go:",
}

REGISTRY_ICONS = {
    "pypi.org": ":fontawesome-brands-python:",
}

REGISTRY_PAGE_URL = {
    "pypi.org": "https://pypi.org/project/{package_name}/",
}

REGISTRY_LABELS = {
    "pypi.org": "PyPI",
}


@dataclass
class ProjectInfo:
    """Resolved metadata for a single project."""

    repo: str
    language: str
    package_name: str | None
    package_registry: str | None
    description: str
    docs_url: str | None
    version: str | None = None
    created: str | None = None
    released: str | None = None
    release_count: int = 0
    stars: int = 0
    forks: int = 0
    github_url: str = ""
    readme: str = ""

    def language_icon(self) -> str:
        """
        Return the icon for the project's language.

        Returns:
            A string like `:fontawesome-brands-python:`.
        """
        return LANGUAGE_ICONS.get(self.language, self.language)

    def language_badge(self) -> str:
        """
        Return an icon-and-label badge for the project's language.

        Returns:
            A string like `:fontawesome-brands-python: Python`.
        """
        icon = LANGUAGE_ICONS.get(self.language, "")
        label = self.language.capitalize()
        return f"{icon} {label}" if icon else label

    def registry_url(self) -> str | None:
        """
        Return the package registry page URL, or None if not published.

        Returns:
            A URL string, or None.
        """
        if not self.package_name or not self.package_registry:
            return None
        template = REGISTRY_PAGE_URL.get(self.package_registry)
        if not template:
            return None
        return template.format(package_name=self.package_name)

    def registry_icon(self) -> str | None:
        """
        Return the MkDocs icon string for the package registry, or None.

        Returns:
            An icon string like `:fontawesome-brands-python:`, or None.
        """
        if not self.package_registry:
            return None
        return REGISTRY_ICONS.get(self.package_registry)

    def registry_label(self) -> str | None:
        """
        Return the display label for the package registry, or None.

        Returns:
            A string like `PyPI`, or None.
        """
        if not self.package_registry:
            return None
        return REGISTRY_LABELS.get(self.package_registry)
