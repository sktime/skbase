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


[0.4.2] - 2023-05-02
====================

Maintenance update that cleans up dependencies.

Notably, ``scikit-base`` no longer has any core dependencies.

This is as per usage intention as a base module,
therefore this removal is not accompanied by deprecation.

Dependency changes
~~~~~~~~~~~~~~~~~~

* ``scikit-learn``, ``typing-extensions``, and ``pytest`` are no longer core dependencies.
  ``pytest`` remains a dependency in ``dev`` and ``test`` dependency sets.
* ``scikit-learn`` is now part of the ``dev`` and ``test`` depency sets,
  as it is required to test compatibility with ``scikit-learn``
* a dependency conflict has been resolved in the ``docs`` dependency set for the docs build,
  by pinning versions

Maintenance
-----------

* [MNT] remove dependency on ``typing-extensions`` (:pr:`167`) :user:`fkiraly`
* [MNT] remove dependency on ``pytest`` (:pr:`168`) :user:`fkiraly`
* [MNT] remove dependency on ``scikit-learn`` (:pr:`171`) :user:`fkiraly`
* [MNT] add ``scikit-learn`` to ``test`` dependency set (:pr:`172`) :user:`fkiraly`
* [MNT] remove ``fail-fast`` flag in CI (:pr:`169`) :user:`fkiraly`
* [MNT] resolve dependency conflict in ``docs`` dependency set (:pr:`173`) :user:`fkiraly`


[0.4.1] - 2023-04-26
====================

Small bugfix patch for pydata 2023 Seattle notebooks.

Fixes
-----

* [BUG] fix html display for meta-objects (:pr:`160`) :user:`fkiraly`
* [BUG] Fix ``all_objects`` lookup, broken tag filter (:pr:`161`) :user:`fkiraly`


[0.4.0] - 2023-04-25
====================

Highlights
----------

- classes for heterogeneous collections aka meta-objects: ``BaseMetaObject`` and
  ``BaseMetaEstimator``, based on ``sklearn`` and ``sktime`` (:pr:`107`, :pr:`155`)
- ``skbase`` native ``get_params`` and ``get_fitted_params`` interface, both with
  ``deep`` argument (:pr:`115`, :pr:`117`) :user:`fkiraly`
- tag and config manager for objects, with ``get_tag``, ``set_tag``, ``get_config``,
  ``set_config``, etc (:pr:`138`, :pr:`140`, :pr:`155`) :user:`fkiraly`
- ``sklearn`` style pretty printing, configurable via
  tags (:pr:`156`) :user:`fkiraly`, :user:`RNKuhns`

Enhancements
------------

* [ENH] Update meta classes and add unit tests (:pr:`107`) :user:`RNKuhns`
* [ENH] ``skbase`` native ``get_params`` (:pr:`115`) :user:`fkiraly`
* [ENH] ensure that ``all_objects`` always
  returns (class name/class) pairs (:pr:`115`) :user:`fkiraly`
* [ENH] Initial type and named object validator code (:pr:`122`) :user:`RNKuhns`
* [ENH] ``deep`` argument for ``get_fitted_params`` (:pr:`117`) :user:`fkiraly`
* [ENH] Improve ``skbase.utils`` module structure (:pr:`126`) :user:`RNKuhns`
* [ENH] Add ``object_type`` param to named object check (:pr:`136`) :user:`RNKuhns`
* [ENH] tag manager mixin (:pr:`138`) :user:`fkiraly`
* [ENH] sync ``TestAllObjects`` with ``sktime`` (:pr:`139`) :user:`fkiraly`
* [ENH] object config interface (:pr:`140`) :user:`fkiraly`
* [ENH] tag logic mixin for meta-estimators (:pr:`155`) :user:`fkiraly`
* [ENH] ``sklearn`` style pretty printing (:pr:`156`) :user:`fkiraly`, :user:`RNKuhns`

Fixes
-----

* [BUG] fix faulty ``BaseObject.__eq__`` and ``deep_equals`` if an attribute
  or nested structure contains ``np.nan`` (:pr:`111`) :user:`fkiraly`
* [BUG] Fix type error bug (:pr:`130`) :user:`RNKuhns`
* [BUG] fix unreported return type bug
  of ``BaseFixtureGenerator.is_excluded`` (:pr:`142`) :user:`fkiraly`

Documentation
-------------

* [DOC] Update installation guide to build ``skbase`` in
  a virtual env (:pr:`157`) :user:`achieveordie`
* [DOC] fix odd author formatting on pypi (:pr:`157`) :user:`fkiraly`

Maintenance
-----------

* [MNT] Create Issue and PR Templates (:pr:`157`) :user:`RNKuhns`
* [MNT] Update pydocstyle in pre-commit config (:pr:`108`) :user:`RNKuhns`
* [MNT] Handle updates to pre-commit linters (:pr:`120`) :user:`RNKuhns`
* [MNT] numpy as a soft dependency (:pr:`121`) :user:`RNKuhns`
* [MNT] Add stacklevel to ``warnings.warn`` calls (:pr:`137`) :user:`RNKuhns`
* [MNT] Add vs code settings and auto generated api area
  to ``.gitignore`` (:pr:`143`) :user:`RNKuhns`
* [MNT] Update slack to point to ``skbase`` workspace (:pr:`148`) :user:`RNKuhns`

Contributors
------------
:user:`achieveordie`,
:user:`fkiraly`,
:user:`rnkuhns`


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
- Add equality dunder to ``BaseObject`` to allow ``BaseObject``-s to be compared based
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
