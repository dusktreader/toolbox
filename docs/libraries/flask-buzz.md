# flask-buzz

py-buzz bindings for Flask applications

[:fontawesome-brands-github:](https://github.com/dusktreader/flask-buzz "GitHub")
[:fontawesome-brands-python:](https://pypi.org/project/flask-buzz/ "PyPI")
[:material-book-open-variant:](https://dusktreader.github.io/flask-buzz/ "Docs")
·
[:material-tag-multiple:](# "Releases") 21 [:material-star:](# "Stars") 3 [:material-source-fork:](# "Forks") 1

**Created**: 2017-10-04 · **Last Released**: 2025-03-28 · **Version**: 4.0.0

---

_py-buzz bindings specifically for flask applications_

This is an extension of the [py-buzz](https://github.com/dusktreader/py-buzz) package.

It adds extra functionality especially for flask. Predominately, it adds the ability to register an error handler with
Flask that will automatically package any handled `FlaskBuzz` exceptions in a nicely formatted JSON response with the
appropriate `status_code` and message. There is also a method to explicitly `jsonify` a FlaskBuzz error with some
control over what is included in the error body.

## Super-quick Start

Requires: Python 3.10 to 3.13

Install through pip:

```bash
pip install flask-buzz
```

Minimal usage example: [examples/basic.py](https://github.com/dusktreader/flask-buzz/tree/master/examples/basic.py)


## Documentation

The complete documentation can be found at the
[flask-buzz home page](https://dusktreader.github.io/flask-buzz)
