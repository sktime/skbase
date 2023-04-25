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

[0.4.0] - 2023-04-25
====================

## What's Changed
* [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci in https://github.com/sktime/skbase/pull/104
* Create Issue and PR Templates by @RNKuhns in https://github.com/sktime/skbase/pull/105
* Update pydocstyle in pre-commit config by @RNKuhns in https://github.com/sktime/skbase/pull/108
* [MNT] Handle updates to pre-commit linters by @RNKuhns in https://github.com/sktime/skbase/pull/120
* [ENH] `skbase` native `get_params` by @fkiraly in https://github.com/sktime/skbase/pull/118
* [ENH] ensure that `all_objects` always returns (class name/class) pairs by @fkiraly in https://github.com/sktime/skbase/pull/115
* [MNT] numpy as a soft dependency by @fkiraly in https://github.com/sktime/skbase/pull/121
* [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci in https://github.com/sktime/skbase/pull/119
* [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci in https://github.com/sktime/skbase/pull/123
* [BUG] fix faulty `BaseObject.__eq__` and `deep_equals` if an attribute or nested structure contains `np.nan` by @fkiraly in https://github.com/sktime/skbase/pull/111
* [ENH] Initial type and named object validator code by @RNKuhns in https://github.com/sktime/skbase/pull/122
* [ENH] `deep` argument for `get_fitted_params` by @fkiraly in https://github.com/sktime/skbase/pull/117
* [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci in https://github.com/sktime/skbase/pull/127
* [DOC] Update installation guide to build skbase in a virtual env by @achieveordie in https://github.com/sktime/skbase/pull/134
* [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci in https://github.com/sktime/skbase/pull/133
* [BUG] Fix type error bug by @RNKuhns in https://github.com/sktime/skbase/pull/130
* Add stacklevel to warnings.warn calls by @RNKuhns in https://github.com/sktime/skbase/pull/137
* [ENH] Improve `skbase.utils` by @RNKuhns in https://github.com/sktime/skbase/pull/126
* Add object_type param to named object check by @RNKuhns in https://github.com/sktime/skbase/pull/136
* [BUG] fix unreported return type bug of `BaseFixtureGenerator.is_excluded` by @fkiraly in https://github.com/sktime/skbase/pull/142
* [ENH] Add vs code settings and auto generated api area to .gitignore by @RNKuhns in https://github.com/sktime/skbase/pull/143
* [ENH] tag manager mixin by @fkiraly in https://github.com/sktime/skbase/pull/138
* [ENH] object config interface by @fkiraly in https://github.com/sktime/skbase/pull/140
* [ENH] sync `TestAllObjects` with `sktime` by @fkiraly in https://github.com/sktime/skbase/pull/139
* [MNT] Update slack to point to skbase workspace by @RNKuhns in https://github.com/sktime/skbase/pull/148
* [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci in https://github.com/sktime/skbase/pull/152
* [ENH] Update meta classes and add unit tests by @RNKuhns in https://github.com/sktime/skbase/pull/107
* [pre-commit.ci] pre-commit autoupdate by @pre-commit-ci in https://github.com/sktime/skbase/pull/153
* [ENH] tag logic mixin for meta-estimators by @fkiraly in https://github.com/sktime/skbase/pull/155
* [ENH] `sklearn` style pretty printing by @fkiraly in https://github.com/sktime/skbase/pull/156
* [DOC] fix odd author formatting on pypi by @fkiraly in https://github.com/sktime/skbase/pull/157


[0.3.0] - 2023-01-08
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
- Add equality dunder to ``BaseObject`` to allow ``BaseObejct``-s to be compared based
  on parameter equality (:pr:`86`) :user:`fkiraly`
- Add ``sktime``-like interface for retrieving fitted parameters to ``BaseEstimator``
  (:pr:`87`) :user:`fkiraly`

Enhancements
------------

- Reorganized package functionality into submodules focused on specific
  functionality (:pr:`78`) :user:`rnkuhns`
- Add equality dunder to ``BaseObject`` to allow ``BaseObejct``-s to be compared based
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

- Refactored code for ``BaseObject`` and related interfaces from ``sktime`` into its
  own package :user:`fkiraly`, :user:`rnkuhns`
- Setup initial continuous integration routines :user:`rnkuhns`
- Setup initial documentation :user:`rnkuhns`
- Setup initial deployment workflow :user:`fkiraly`
