# fastapi-buzz

py-buzz bindings for FastAPI applications

[:fontawesome-brands-github:](https://github.com/dusktreader/fastapi-buzz "GitHub")
[:fontawesome-brands-python:](https://pypi.org/project/fastapi-buzz/ "PyPI")
[:material-book-open-variant:](https://dusktreader.github.io/fastapi-buzz/ "Docs")
·
[:material-tag-multiple:](# "Releases") 1 [:material-star:](# "Stars") 1

**Created**: 2025-04-13 · **Last Released**: 2025-04-13 · **Version**: 0.1.0

---

_py-buzz bindings specifically for FastAPI applications_

This is an extension of the [py-buzz](https://github.com/dusktreader/py-buzz) package.

It adds extra functionality especially for FastAPI. Predominately, it adds the ability to register an error handler with
FastAPI that will automatically package any handled `FastAPIBuzz` exceptions in a nicely formatted JSON response with
the appropriate `status_code` and message. There is also a method to package a FastAPIBuzz error into a response with
some control over what is included in the error body.

## Super-quick Start

Requires: Python 3.10 to 3.13

Install through pip:

```bash
pip install fastapi-buzz
```

Minimal usage example: [examples/basic.py](https://github.com/dusktreader/fastapi-buzz/tree/master/examples/basic.py)


## Documentation

The complete documentation can be found at the
[fastapi-buzz home page](https://dusktreader.github.io/fastapi-buzz)
