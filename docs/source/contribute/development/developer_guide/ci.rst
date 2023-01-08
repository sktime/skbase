.. _ci:

======================
Continuous integration
======================

.. _Github Actions: https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions
.. _precommit.ci: https://pre-commit.ci/

``skbase`` uses `Github Actions`_ continuous integration (CI) services
to ensure contributions meet the project's standards. See the sections below to
see how the project automatically validates code quality, and builds and tests
your changes.

Code quality checks
===================

``skbase`` uses `pre-commit.ci <https://pre-commit.ci/>`_ to help maintain the project's
:ref:`coding style <code_style>`, by automating the code quality checks spelled out in
the .pre-commit-config.yaml in the project's root directory. These checks run
automatically when you open a Pull Request or push a new commit to an existing
Pull Request.

When starting your development in your own local clone of the repository,
you should use your command line tool to run :code:`pre-commit install`. This
will setup pre-commit locally, and trigger the repositories pre-commit hooks
to run prior committing your code locally.

.. note::


    The project also continues to make use of the deprecated
    `pre-commit github action <https://github.com/pre-commit/action>`_, because
    it makes it easy cancel other continuous integration steps
    (including unit testing). This duplicates the code quality portion of the
    CI routine, but enables the longer unit testing portion of the CI routine
    to be cancelled whenever the code quality portion fails. A contribution
    that enables Github Action workflows to be cancelled when
    `pre-commit.ci <https://pre-commit.ci/>`_ fails, would be greatly appreciated.

Unit testing
============

``skbase`` uses `pytest <https://docs.pytest.org/en/latest/>`_ for unit testing.
To check if your code passes all tests locally, follow ``skbase``'s
:ref:`development installation <dev_install>` instructions, which will install
``pytest`` along with other development tools.

With ``pytest`` installed, you can navigate to your local project's root directory
and run:

   .. code:: bash

      pytest ./skbase

or if you have `make <https://www.gnu.org/software/make/>`_ installed:

   .. code:: bash

      make test

Infrastructure
==============

This section gives an overview of the infrastructure and continuous
integration services ``skbase`` uses.

+---------------+-----------------------+-------------------------------------+
| Platform      | Operation             | Project Configuration               |
+===============+=======================+=====================================+
| `GitHub       | Build/test/           | `.github/workflows/ <https://gi     |
| Actions`_     | distribute            | thub.com/sktime/skbase              |
|               | on Linux, MacOS and   | /blob/main/.github/workflows/>`_    |
|               | Windows               |                                     |
+---------------+-----------------------+-------------------------------------+
| `pre-commit.ci| Automate code quality | `.pre-commit-config.yml             |
| <https://     | validation            | <https://github.com/sktime          |
| pre-commit.ci |                       | /skbase/blob/main/                  |
| />`_          |                       | .pre-commit-config.yaml>`_          |
+---------------+-----------------------+-------------------------------------+
| `Read the     | Build/deploy          | `.readthedocs.yaml                  |
| Docs <h       | documentation         | <https://github.com/sktime          |
| ttps://readth |                       | /skbase/blob/main/                  |
| edocs.org>`__ |                       | .readthedocs.yaml>`_                |
+---------------+-----------------------+-------------------------------------+
| `Codecov      | Test coverage         | `.codecov.yml <https                |
| <https://c    |                       | ://github.com/sktime/skbase         |
| odecov.io>`__ |                       | /blob/main/.codecov.yml>`_,         |
|               |                       | `.coveragerc <htt                   |
|               |                       | ps://github.com/sktime/skbase       |
|               |                       | /blob/main/.coveragerc>`_           |
+---------------+-----------------------+-------------------------------------+

Additional scripts used for code quality, building, unit testing and
distribution can be found in
`build_tools/ <https://github.com/sktime/skbase/tree/main/build_tools>`_.
