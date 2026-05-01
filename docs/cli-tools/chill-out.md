# chill-out

Have your dependencies chill out a bit while you make sure they are safe.

[:fontawesome-brands-github:](https://github.com/dusktreader/chill-out "GitHub")
[:fontawesome-brands-python:](https://pypi.org/project/chill-out/ "PyPI")
[:material-book-open-variant:](https://dusktreader.github.io/chill-out/ "Docs")
·
[:material-tag-multiple:](# "Releases") 1

**Created**: 2026-05-01 · **Last Released**: 2026-05-01 · **Version**: 0.1.0

---

![chill-out](https://raw.githubusercontent.com/dusktreader/chill-out/main/docs/source/images/chill-400.png?raw=true)

_Have your dependencies chill out a bit while you make sure they are safe._

`chill-out` audits your lockfile for packages that are too fresh to trust. The lockfile is what actually gets installed,
so that's what matters: a `requests` declared in `pyproject.toml` is only a real risk once it shows up in `uv.lock`.
Maintainer tokens get stolen, typosquatters grab package names, and plenty of releases are just broken. **Cooldown** is
the practice of refusing any version that has been public for less than some grace period, long enough for the
community to spot trouble and react.

Supply chain attacks (compromised maintainer accounts, hijacked publishing tokens) typically surface as a brand-new
release of a package. If your cooldown window is 14 days and you run `chill-out` before every deploy, a malicious
release has to survive 14 days of public scrutiny before it can land in production. Transitives matter as much as
direct dependencies, sometimes more, because you can't vet them by hand.

GitHub's Dependabot supports cooldown windows natively, but Dependabot only runs on the schedule you give it.
`chill-out` runs on demand from your terminal, your CI, or your editor: it reads your lockfile, asks the registry when
each package was published, and tells you which entries (principals and transitives alike) are still inside the
cooldown window. When it can, it suggests an older version that is safely past its cooldown, or fixes your locked
dependencies outright to eliminate the threat.

## Super-quick start

Requires: Python 3.12+

```bash
pip install chill-out
```

In any npm or Python project:

```bash
chill-out check
```

To rewrite your manifest with safe pins:

```bash
chill-out fix
```

## Documentation

The complete documentation lives at the [chill-out home page](https://dusktreader.github.io/chill-out).

## Demo

To check out the features, run the demo directly via `uvx` without installing it!

```bash
uvx --from "chill-out[demo]" chill-out-demo
```
