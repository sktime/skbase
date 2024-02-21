<a href="https://skbase.readthedocs.io/en/latest/"><img src="https://github.com/sktime/skbase/blob/main/docs/source/images/skbase-logo-with-name.png" width="175" align="right" /></a>

# Welcome to skbase

> A framework factory for scikit-learn-like and sktime-like parametric objects

`skbase` provides base classes for creating scikit-learn-like parametric objects,
along with tools to make it easier to build your own packages that follow these design patterns.

:rocket: Version 0.7.2 is now available. Check out our
[release notes](https://skbase.readthedocs.io/en/latest/changelog.html).

| Overview | |
|---|---|
| **CI/CD** | [![Tests](https://github.com/sktime/skbase/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/sktime/skbase/actions/workflows/test.yml) [![codecov](https://codecov.io/gh/sktime/skbase/branch/main/graph/badge.svg?token=2J424NLO82)](https://codecov.io/gh/sktime/skbase) [![Documentation Status](https://readthedocs.org/projects/skbase/badge/?version=latest)](https://skbase.readthedocs.io/en/latest/?badge=latest) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sktime/skbase/main.svg)](https://results.pre-commit.ci/latest/github/sktime/skbase/main) |
| **Code** |  [![!pypi](https://img.shields.io/pypi/v/scikit-base?color=orange)](https://pypi.org/project/scikit-base/)  [![!python-versions](https://img.shields.io/pypi/pyversions/scikit-base)](https://www.python.org/) [![!black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit) |
| **Downloads**| [![Downloads](https://static.pepy.tech/personalized-badge/scikit-base?period=week&units=international_system&left_color=grey&right_color=blue&left_text=weekly%20(pypi))](https://pepy.tech/project/scikit-base) [![Downloads](https://static.pepy.tech/personalized-badge/scikit-base?period=month&units=international_system&left_color=grey&right_color=blue&left_text=monthly%20(pypi))](https://pepy.tech/project/scikit-base) [![Downloads](https://static.pepy.tech/personalized-badge/scikit-base?period=total&units=international_system&left_color=grey&right_color=blue&left_text=cumulative%20(pypi))](https://pepy.tech/project/scikit-base) |

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-13-orange.svg?style=flat-square)](#contributors)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Documentation and Tutorials

To learn more about the package check out:

* our [documentation](https://skbase.readthedocs.io/en/latest/)
* our [introductory tutorial](https://github.com/sktime/sktime-tutorial-pydata-seattle-2023) (jupyter notebooks and video presentation)

## :hourglass_flowing_sand: Install skbase
For trouble shooting or more information, see our
[detailed installation instructions](https://skbase.readthedocs.io/en/latest/user_documentation/installation.html).

- **Operating system**: macOS X · Linux · Windows 8.1 or higher
- **Python version**: Python 3.8, 3.9, 3.10, 3.11 and 3.12
- **Package managers**: [pip]

[pip]: https://pip.pypa.io/en/stable/

### pip
skbase releases are available as source packages and binary wheels via PyPI
and can be installed using pip. Checkout the full list of pre-compiled [wheels on PyPi](https://pypi.org/simple/skbase/).

To install the core package use:

```bash
pip install scikit-base
```

or, if you want to install with the maximum set of dependencies, use:

```bash
pip install scikit-base[all_extras]
```
