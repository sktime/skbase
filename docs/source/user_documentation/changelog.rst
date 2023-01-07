=========
Changelog
=========

All notable changes to this project beggining with version 0.1.0 will be
documented in this file. The format is based on
`Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_ and we adhere
to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_. The source
code for all `releases <https://github.com/sktime/baseobject/releases>`_
is available on GitHub.

You can also subscribe to ``skbase``'s
`PyPi release <https://libraries.io/pypi/baseobject>`_.

For planned changes and upcoming releases, see our :ref:`roadmap`.

[0.3.0] - 2023-01-07
====================

Highlights
----------

- Reorganized package functionality into submodules focused on specific
  functionality (:pr:`78`):

  - ``skbase.base`` for ``BaseObject``, ``BaseEstimator`` and other base classes
  - ``skbase.testing`` for functionality to test ``BaseObject``-s
  - ``skbase.lookup`` for retrieving metadata and all ``BaseObject``-s from a package
  - ``skbase.validate`` for comparing and validating ``BaseObject``-s

- Expanded test coverage of ``skbase.base`` and ``skbase.lookup`` modules and
  ``skbase`` exceptions (:pr:`62`, :pr:`80`, :pr:`91`) :user:`rnkuhns`
- Add equality dunded to ``BaseObject`` to allow ``BaseObejct``-s to be compared based
  on parameter equality (:pr:`86`) :user:`fkiraly`
- Add ``sktime``-like interface for retrieving fitted parameters to ``BaseEstimator``
  (:pr:`87`) :user:`fkiraly`

Enhancements
------------

- Reorganized package functionality into submodules focused on specific
  functionality (:pr:`78`) :user:`rnkuhns`
- Add equality dunded to ``BaseObject`` to allow ``BaseObejct``-s to be compared based
  on parameter equality (:pr:`86`) :user:`fkiraly`
- Add ``sktime``-like interface for retrieving fitted parameters to ``BaseEstimator``
  (:pr:`87`) :user:`fkiraly`
- Rename ``QuickTester.run_tests`` parameter ``return_exceptions`` to
  ``raise_exceptions`` (:pr:`95`) :user:`fkiraly`

Fixes
-----

- Fix all_objects retrieval functionality (:pr:`69`) :user:`fkiraly`
- Fix issues identified by CodeQL scanning (:pr:`79`) :user:`rnkuhns`

Documentation
-------------

- Switch from use of ``sphinx-panels`` to ``sphinx-design`` (:pr:`93`) :user:`rnkuhns`
- Updated installation instructions, added release instructions and made
  other minor documentation improvements  (:pr:`100`) :user:`rnkuhns`

Maintenance
-----------

- Updated Github Action versions (:pr:`60`) :user:`rnkuhns`
- Migrate from use of lgtm.com to CodeQL scanning built-in to Github (:pr:`68`)
- Update config files and remove use of setup.py (:pr:`75`) :user:`rnkuhns`
- Add support for Python 3.11 (:pr:`77`) :user:`rnkuhns`
- Update ``sklearn``s version upper bounds to ``<1.3`` (:pr:`89`) :user:`fkiraly`


Contributors
------------
:user:`fkiraly`,
:user:`rnkuhns`


[0.2.0] - 2022-09-09
====================

This release is a maintenance release to change the name of the package
from ``baseobject`` to ``skbase``.

Highlights
----------

- The package name was changed to ``skbase`` (:pr:`46`, :pr:`47`) :user:`fkiraly`

[0.1.0] - 2022-09-08
====================

Highlights
----------

- Refacted code for ``BaseObject`` and related interfaces from ``sktime`` into its
  own package :user:`fkiraly`, :user:`rnkuhns`
- Setup initial continuous integration routines :user:`rnkuhns`
- Setup initial documentation :user:`rnkuhns`
- Setup initial deployment workflow :user:`fkiraly`
