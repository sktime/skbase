.. _full_install:

============
Installation
============

``baseobject`` currently supports:

* environments with python version 3.7, 3.8, 3.9 or 3.10
* operating systems Mac OS X, Unix-like OS, Windows 8.1 and higher

Checkout the full list of pre-compiled wheels on
`PyPI <https://pypi.org/simple/baseobject/>`_.

Release versions
================

Most users will be interested in installing a released version of ``baseobject``
using one of the approaches outlined below. For common installation issues,
see the `Release versions - troubleshooting`_ section.

Installing ``baseobject`` from PyPI
-----------------------------------

``baseobject`` releases are available via PyPI and can be installed via ``pip`` using:

.. code-block:: bash

    pip install baseobject

This will install ``baseobject`` with core dependencies, excluding soft dependencies.

To install ``baseobject`` with maximum dependencies, including soft dependencies,
install with the ``all_extras`` modifier:

.. code-block:: bash

    pip install baseobject[all_extras]

Installing ``baseobject`` from conda
------------------------------------

.. note::

    We are still working on creating releases of ``baseobject`` on ``conda``.
    If you would like to help, please open a pull request.

Release versions - troubleshooting
----------------------------------

Missing soft fependencies
~~~~~~~~~~~~~~~~~~~~~~~~~

Users may run into problems, when they install the core version of ``baseobject``,
but attempt to use functionality that requires soft dependencies to be installed.
To resolve this, install the missing package, or install ``baseobject``
with maximum dependencies (see above).

.. _dev_install:

Development versions
====================

To install the latest development version of ``baseobject``, the sequence
of steps is as follows:


1. Clone the ``baseobject`` `Github repository`_
2. Use ``pip`` to build ``baseobject`` from source


Detail instructions for each step is provided below.

Step 1 - Clone Github repository
--------------------------------

The ``baseobject`` `Github repository`_ should be cloned to a local directory.

To install the latest version using the ``git`` command line, use the following steps:

1. Use your command line tool to navigate to the directory where you want to clone
   ``baseobject``
2. Clone the repository: :code:`git clone https://github.com/sktime/baseobject.git`
3. Move into the root directory of the package's local clone: :code:`cd baseobject`
4. Make sure you are on the main branch: :code:`git checkout main`
5. Make sure your local version is up-to-date: :code:`git pull`

See Github's `documentation <github_docs>`_ for additional details.

.. hint::

    If you want to checkout an earlier version of ``baseobject`` you can use the
    following git command line after cloning to run: :code:`git checkout <VERSION>`

    Where ``<VERSION>`` is a valid version string that can be found by inspecting the
    repository's ``git`` tags, by running ``git tag``.

    You can also download a specific release version from the Github repository's
    zip archive of `releases <https://github.com/sktime/baseobject/releases>`_.

Step 2 - Build ``baseobject`` from source
-----------------------------------------

For a static install of ``baseobject`` from source, navigate to your local
clone's root directory run the following in your command line:

.. code-block:: bash

    pip install .

.. hint::

    In either the static or editable installation, the ``.`` may be replaced
    with a full or relative path to your local clone's root directory.

For a developer install that updates the package each time the
local source code is changed, tell ``pip`` to install  ``baseobject``
in `editable mode <ed_installs>`_, via:

.. code-block:: bash

    pip install --editable .[dev]

Including "[dev]" also makes sure that the optional *dev*
dependencies specified in the ``baseobject's`` pypyroject.toml file
are also installed.

.. hint::

    By including "[dev]" above, ``pre-commit`` and other tools you'll want to use
    when developing ``baseobject`` are also installed. In most cases, you'll
    let ``pre-commit`` manage installation environments for your linting tools.
    However, some integrated development environments (for example, VS Code)
    will automatically apply linters (including reformatting) on save. If you want
    to easily Install all the linters in your environment use
    :code:`pip install --editable .[dev,linters]`.

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
`installation instructions <https://www.sktime.org/en/stable/installation.html>`_.

.. _Github repository: https://github.com/sktime/BaseObject
.. _github_docs: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
.. _ed_installs: https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs
