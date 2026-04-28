# snick

Text manipulation gadgets for indentation

[:fontawesome-brands-github:](https://github.com/dusktreader/snick "GitHub")
[:fontawesome-brands-python:](https://pypi.org/project/snick/ "PyPI")
[:material-book-open-variant:](https://dusktreader.github.io/snick/ "Docs")
·
[:material-tag-multiple:](# "Releases") 12 [:material-star:](# "Stars") 4

**Created**: 2020-11-23 · **Last Released**: 2026-04-28 · **Version**: 3.2.0

---

![snick-hero](https://raw.githubusercontent.com/dusktreader/snick/main/docs/source/images/snick-hero.png)

**Handy gadgets for taming indented text**

A small collection of practical utilities for working with indented strings and text formatting:

* **Dedent** triple-quoted strings without giving up indented code
* **Build** multi-line output line by line with `Conjoiner`
* **Format** data structures like `pprint`, but with `json.dumps`-style indentation and trailing commas
* **Strip** ANSI codes and stray whitespace from terminal output
* **Wrap and indent** text blocks for logs and reports

Built on the Python standard library — nothing extra to install.


## Quickstart

### Requirements

* Python 3.10 or greater


### Installation

Install the latest release from PyPI:

```bash
pip install snick
```


### Quick taste

```python
import snick

message = snick.dedent(
    """
    The Force will be with you.
    Always.
    """
)
print(message)
```

Running this gives:

```
The Force will be with you.
Always.
```

To learn about all the features, see the [documentation](https://dusktreader.github.io/snick/).


## Try the demo

The fastest way to see snick in action is to run the interactive demo. No
install required:

```bash
uvx --from=snick[demo] snick-demo
```

The demo walks through every feature, one function at a time. Each step shows
the source code and its output, then asks whether to continue.
