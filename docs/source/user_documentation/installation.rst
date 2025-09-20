.. _full_install:

============
Installation
============

``skbase`` currently supports:

* environments with python version 3.9, 3.10, 3.11, 3.12, or 3.13
* operating systems Mac OS X, Unix-like OS, Windows 8.1 and higher

Checkout the full list of pre-compiled wheels on
`PyPI <https://pypi.org/simple/skbase/>`_.

Release versions
================

Most users will be interested in installing a released version of ``skbase``
using one of the approaches outlined below. For common installation issues,
see the `troubleshooting release installations`_ section.

Installing ``skbase``
---------------------

``skbase`` releases are available via PyPI and can be installed via ``pip``. Users
can choose whether to install the ``skbase`` with its standard dependencies or
alternatively to install ``skbase`` with all its dependencies using the
code snippets below.

.. tab-set::

    .. tab-item:: PyPi

        .. code-block:: bash

           pip install scikit-base

    .. tab-item:: PyPi (all dependencies)

        .. code-block:: bash

           pip install scikit-base[all_extras]

    .. tab-item:: Conda

        .. note::

            We are still working on creating releases of ``skbase`` on ``conda``.
            If you would like to help, please open a pull request.

    .. tab-item:: Conda (all dependencies)

        .. note::

            We are still working on creating releases of ``skbase`` on ``conda``.
            If you would like to help, please open a pull request.


Troubleshooting release installations
-------------------------------------

Missing soft dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~

Users may run into problems, when they install the core version of ``skbase``,
but attempt to use functionality that requires soft dependencies to be installed.
To resolve this, install the missing package, or install ``skbase``
with maximum dependencies (see above).

.. _dev_install:

Development versions
====================

To install the latest development version of ``skbase``, the sequence
of steps is as follows:


1. Clone the ``skbase`` `GitHub repository`_
2. Create a new virtual environment via ``conda`` and activate it.
3. Use ``pip`` to build ``skbase`` from source and install development dependencies


Detail instructions for each step is provided below.

Step 1 - Clone GitHub repository
--------------------------------

The ``skbase`` `GitHub repository`_ should be cloned to a local directory.

To install the latest version using the ``git`` command line, use the following steps:

1. Use your command line tool to navigate to the directory where you want to clone
   ``skbase``
2. Clone the repository: :code:`git clone https://github.com/sktime/skbase.git`
3. Move into the root directory of the package's local clone: :code:`cd skbase`
4. Make sure you are on the main branch: :code:`git checkout main`
5. Make sure your local version is up-to-date: :code:`git pull`

See GitHub's `repository clone documentation`_
for additional details.

.. hint::

    If you want to checkout an earlier version of ``skbase`` you can use the
    following git command line after cloning to run: :code:`git checkout <VERSION>`

    Where ``<VERSION>`` is a valid version string that can be found by inspecting the
    repository's ``git`` tags, by running ``git tag``.

    You can also download a specific release version from the GitHub repository's
    zip archive of `releases <https://github.com/sktime/skbase/releases>`_.

Step 2 - Create a new virtual environment
-----------------------------------------

Setting a new virtual environment before building ``skbase`` ensures that
no two conflicting package versions are installed in the same environment.
You can choose your favorite env manager for this but we're showing the
steps to create one using ``conda``:

1. Use your command line tool to first confirm ``conda`` is present on your
   system: :code:`conda --version`
2. Create a new virtual environment named ``skbase-dev`` with python version ``3.9``:
   :code:`conda create -n skbase-dev python=3.9`
3. Activate this newly created environment: :code:`conda activate skbase-dev`

Step 3 - Build ``skbase`` from source
-------------------------------------

When contributing to the project, you will want to install ``skbase`` locally, along
with additional dependencies used when developing the package.

You can opt for a static install of ``skbase`` from your local source, but if you
plan to contribute to the project you may be better served by installing ``skbase``
in `editable mode`_ so that the the package updates each time the local source
code is changed.

Either way, including the "[dev,test]" modifier, makes sure that the additional
developer dependencies and test dependencies specified in the ``skbase``
pyproject.toml file are also installed.

To use either approach:

1. Use your command line tool to navigate to the root directory of your local
   copy of the ``skbase`` project
2. Copy the code snippet below that corresponds to the installation approach you
   would like to use
3. Paste the copied code snippet in your command line tool and run it

.. tab-set::

    .. tab-item:: Static installation

        .. code-block:: bash

           pip install .[dev,test]

    .. tab-item:: Install in editable mode

        .. code-block:: bash

           pip install --editable .[dev,test]

.. hint::

    In either the static or editable installation, the ``.`` may be replaced
    with a full or relative path to your local clone's root directory.

.. hint::

    Using the "[dev]" modifier installs developer dependencies, including
    ``pre-commit`` and other tools you'll want to use when developing ``skbase``.
    In most cases, you'll let ``pre-commit`` manage installation environments
    for your linting tools. However, some integrated development environments
    (for example, VS Code) will automatically apply linters (including
    reformatting) on save. This may require the linters to be installed
    directly in your development environment. If you want to easily Install all
    the linters used by ``skbase`` in your development environment use
    :code:`pip install .[dev,test,linters]`
    or :code:`pip install --editable .[dev,test,linters]` instead.

Building binary packages and installers
=======================================

The ``.whl`` package and ``.exe`` installers can be built with:

.. code-block:: bash

    pip install wheel
    python setup.py bdist_wheel

The resulting packages are generated in the ``dist/`` folder.

References
----------

The installation instruction are adapted from sktime's
`installation instructions <https://www.sktime.net/en/stable/installation.html>`_.

.. _Github repository: https://github.com/sktime/skbase
.. _repository clone documentation: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
.. _editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
