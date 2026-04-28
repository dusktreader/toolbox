# py-buzz

Python exceptions with extras

[:fontawesome-brands-github:](https://github.com/dusktreader/py-buzz "GitHub")
[:fontawesome-brands-python:](https://pypi.org/project/py-buzz/ "PyPI")
[:material-book-open-variant:](https://dusktreader.github.io/py-buzz/ "Docs")
·
[:material-tag-multiple:](# "Releases") 49 [:material-star:](# "Stars") 18 [:material-source-fork:](# "Forks") 4

**Created**: 2016-12-20 · **Last Released**: 2026-04-11 · **Version**: 8.1.2

---

![py-buzz-logo](https://raw.githubusercontent.com/dusktreader/py-buzz/main/docs/source/images/buzz-logo-text.png)

**That's not flying, _it's falling with style_: Exceptions with extras**

![asciicast](https://raw.githubusercontent.com/dusktreader/py-buzz/main/docs/source/images/py-buzz.gif)

py-buzz is fully equipped with a suite of exception tools that will save you
from writing the same code over and over again in your python projects. These
include:

* checking many conditions and reporting which ones failed (`check_expressions()`)
* catching exceptions wrapping them in clearer exception types with better error messages (`handle_errors()`)
* retrying operations with exponential backoff until they succeed (`retry()`)
* checking that values are defined and raising errors if not (`enforce_defined()`)
* checking that values are a certain type and raising errors if not (`ensure_type()`)
* checking conditions and raising errors on failure (`require_condition()`)

py-buzz also provides an exception class, Buzz, that can be used  as a base class
for custom exceptions within a project.

## Super-quick Start

* Only requires Python 3.10 or later
* Installed with pip (`$ pip install py-buzz`)
* Each feature demonstrated in an executable demo "extra"

## Documentation

The complete documentation can be found at the [py-buzz documentation page](https://dusktreader.github.io/py-buzz/)
