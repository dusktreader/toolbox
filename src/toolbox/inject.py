"""Inject generated content into markdown files between comment anchors."""


import re
from pathlib import Path

# Markers in markdown files that delimit generated content
TABLE_OPEN = "<!-- project-table:{key} -->"
TABLE_CLOSE = "<!-- /project-table -->"


def inject_between_markers(
    content: str,
    open_marker: str,
    close_marker: str,
    replacement: str,
) -> str:
    """
    Replace content between open and close markers in a string.

    Parameters:
        content:      Full file content.
        open_marker:  Opening comment marker.
        close_marker: Closing comment marker.
        replacement:  New content to place between markers.
    """
    pattern = re.compile(
        re.escape(open_marker) + r"\n.*?\n" + re.escape(close_marker),
        re.DOTALL,
    )
    new_block = f"{open_marker}\n{replacement}\n{close_marker}"
    result, count = pattern.subn(new_block, content)
    if count == 0:
        print(f"  WARNING: marker not found: {open_marker}")
    return result


def inject_table(file_path: Path, key: str, table: str) -> None:
    """
    Inject a generated table into a markdown file.

    Parameters:
        file_path: Path to the markdown file.
        key:       Category key used in the marker.
        table:     Generated markdown table.
    """
    content = file_path.read_text()
    open_marker = TABLE_OPEN.format(key=key)
    updated = inject_between_markers(content, open_marker, TABLE_CLOSE, table)
    file_path.write_text(updated)
