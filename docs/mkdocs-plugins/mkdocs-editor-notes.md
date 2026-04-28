# mkdocs-editor-notes

Gather editor's notes from annotated documents

[:fontawesome-brands-github:](https://github.com/dusktreader/mkdocs-editor-notes "GitHub")
[:fontawesome-brands-python:](https://pypi.org/project/mkdocs-editor-notes/ "PyPI")
[:material-book-open-variant:](https://dusktreader.github.io/mkdocs-editor-notes/ "Docs")
·
[:material-tag-multiple:](# "Releases") 1

**Created**: 2026-01-21 · **Last Released**: 2026-01-28 · **Version**: 0.1.0

---

_Provides a page of editor's notes gathered from annotated document files._


## Overview

mkdocs-editor-notes is a MkDocs plugin that allows you to embed editorial notes directly in your markdown documentation
files. These notes can be used to track todos, questions, improvements, and research items without cluttering the main
documentation.

All notes are automatically collected and displayed on a dedicated aggregator page, making it easy to see all editorial
work at a glance.


## Key Features

- **Footnote-like Syntax**: Familiar syntax similar to markdown footnotes
- **Multiple Note Types**: Supports builtin types and custom types as well.
- **Customizable Emojis**: Note types can be configured with emojis
- **Aggregator Page**: Automatic collection of all notes in one place
- **Source Linking**: Click to navigate back to note locations
- **Configurable Visibility**: Show or hide note markers in rendered pages


## Quick Example

```markdown

This sentence needs more work[^todo:polish].

The current approach might not scale[^ponder:performance].

Research needed here.[^research:alternatives]


[^todo:polish]: Add error handling and tests
[^ponder:performance]: Should we benchmark with larger datasets?
[^research:alternatives]: Look into alternative libraries
```

All these notes will appear on the `/editor-notes/` page, grouped by type, with links back to their source paragraphs.


## Super-quick Start

Requires: Python 3.12 to 3.14

Install through pip:

```bash
pip install mkdocs-editor-notes
```

Add to your `mkdocs.yml`:

```yaml
plugins:
  - editor-notes
```


## Running the Example

This repository includes a complete example MkDocs site in the `example/` directory that demonstrates the plugin's
features. You can run it locally to see the plugin in action.

### Build the example site:

```bash
make example/build
```

### Serve the example site locally:

```bash
make example/serve
```

The example site will be available at `http://localhost:10001`. Navigate to the `/editor-notes/` page to see all the
collected editorial notes from the example documentation.


## Documentation

The complete documentation can be found at the [mkdocs-editor-notes home
page](https://dusktreader.github.io/mkdocs-editor-notes)
