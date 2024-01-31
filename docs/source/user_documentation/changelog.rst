=========
Changelog
=========

All notable changes to this project beginning with version 0.1.0 will be
documented in this file. The format is based on
`Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_ and we adhere
to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_. The source
code for all `releases <https://github.com/sktime/skbase/releases>`_
is available on GitHub.

You can also subscribe to ``skbase``'s
`PyPi release <https://libraries.io/pypi/scikit-base>`_.

For planned changes and upcoming releases, see our :ref:`roadmap`.


[0.7.2] - 2023-01-31
====================


[0.7.1] - 2023-01-12
====================

Minor bugfix and maintenance release.

Contents
--------

* [BUG] fix ``deep_equals`` for ``np.array`` with ``dtype="object"``
  (:pr:`263`) :user:`fkiraly`
* [pre-commit.ci] pre-commit autoupdate (:pr:`264`) :user:`precommit-ci`


[0.7.0] - 2023-01-03
====================

Bugfix release with potentially breaking changes related to
``set_config``, ``get_config`` (:pr:`257`, :pr:`259`, :user:`fkiraly`)
due to masking of third party bugs,
please consult the changelog for details in case of breakage.

Core interface changes
----------------------

* configuration values - set via ``set_config`` and inspectable via ``get_config`` -
  are now retained through ``clone`` and ``reset``.
  Previous behaviour was to reset configuration values to default,
  which is considered a bug. However, this change may break existing code
  if two errors cancel out, e.g.,
  if a breaking (without bug) configuration was set, the reset through the bug.
  In this case, the bug masked the breaking configuration, which should be addressed.
  Most breakages over 0.6.2 should be addressable by removing ``set_config`` calls,
  i.e., removing the genuinely breaking configuration.
* A configuration field ``clone_config`` was added that allows to configure
  whether ``clone`` should clone the configuration.
  This is useful for meta-estimators that
  should not clone the configuration of their components.
  This change is not breaking - considered in difference to the above - as
  the default behaviour is to clone the configuration.

Fixes
-----

* [BUG] fix ``deep_equals`` plugin for ``pd.Index`` (:pr:`260`) :user:`fkiraly`
* [BUG] retain config at ``reset``, add tests for ``set_config``, ``get_config``
  (:pr:`259`) :user:`fkiraly`
* [BUG] retain config after ``clone``, add config to configure whether to clone config
  (:pr:`257`) :user:`fkiraly`


[0.6.2] - 2023-12-30
====================

Release with minor improvements and bugfixes.

Enhancements
------------

* [ENH] ``deep_equals`` - clearer return on diffs from ``dtypes`` and ``index``,
  relaxation of ``MultiIndex`` equality check (:pr:`246`) :user:`fkiraly`

Fixes
-----

* [BUG] ensure ``deep_equals`` plugins are passed on to all recursions
  (:pr:`243`) :user:`fkiraly`

Documentation
-------------

* [DOC] Fixed spelling mistakes as identified by ``codespell`` and ``typos``
  (:pr:`245`) :user:`yarnabrina`

Maintenance
-----------

* [MNT] [Dependabot](deps-dev): Update sphinx-gallery requirement
  from ``<0.15.0`` to ``<0.16.0`` (:pr:`247`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump actions/setup-python from 4 to 5
  (:pr:`250`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump conda-incubator/setup-miniconda from 2 to 3
  (:pr:`249`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump github/codeql-action from 2 to 3
  (:pr:`252`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump actions/download-artifact from 3 to 4
  (:pr:`253`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump actions/upload-artifact from 3 to 4
  (:pr:`254`) :user:`dependabot`


[0.6.1] - 2023-10-26
====================

Highlights
----------

* ``set_params`` now recognizes unique suffixes as aliases
  for full parameter strings, e.g., ``foo`` instead of
  ``estimator__component__foo`` (:pr:`229`) :user:`fkiraly`
* the ``deep_equals`` utility now admits custom plugins with dependency
  isolation, e.g., for data types such as ``dask`` or ``polars``
  (:pr:`238`) :user:`fkiraly`
* ``dependabot`` is now enabled for the ``skbase`` repository
  (:pr:`228`) :user:`fkiraly`


Core interface changes
----------------------

* ``set_params`` now recognizes unique suffixes as aliases
  for full parameter strings. This change is not breaking as behaviour
  changes only in cases where previously exceptions were raised.

Enhancements
------------

* [ENH] ``set_params`` to recognize unique suffixes as aliases
  for full parameter string (:pr:`229`) :user:`fkiraly`
* [ENH] refactor string coercions and return logic in ``deep_equals`` utility
  (:pr:`237`) :user:`fkiraly`
* [ENH] improved ``deep_equals`` utility - plugins for custom types
  (:pr:`238`) :user:`fkiraly`
* [ENH] informative failure message in
  ``test_get_package_metadata_returns_expected_results`` (:pr:`239`) :user:`fkiraly`

Maintenance
-----------

* [MNT] activate ``dependabot`` for version updates and maintenance
  (:pr:`228`) :user:`fkiraly`
* [MNT] [Dependabot](deps): Bump actions/upload-artifact from 2 to 3
  (:pr:`230`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump actions/dependency-review-action from 1 to 3
  (:pr:`231`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump actions/checkout from 3 to 4
  (:pr:`232`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump actions/download-artifact from 2 to 3
  (:pr:`233`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump styfle/cancel-workflow-action from 0.9.1 to 0.12.0
  (:pr:`234`) :user:`dependabot`

Fixes
-----

* [BUG] correct parameter name in ``TestAllObjects`` ``all_objects`` call
  (:pr:`236`) :user:`fkiraly`


[0.6.0] - 2023-10-05
====================

Maintenance release at python 3.12 release.

Adds support for python 3.12.

Dependency changes
------------------

* ``skbase`` now supports python 3.12.

Deprecations and removals
-------------------------

* the ``deep_equals`` utility has moved to ``skbase.utils.deep_equals``.
  The old location in ``skbase.testing.utils.deep_equals`` has now been removed.

Contents
--------

* [MNT] address deprecation of ``load_module`` in ``python 3.12``
  (:pr:`190`) :user:`fkiraly`
* [MNT] simplify test CI and remove ``conda`` (:pr:`224`) :user:`fkiraly`
* [MNT] update dependency versions in ``doc`` dependency set and set upper bounds
  (:pr:`226`, :pr:`227`) :user:`fkiraly`
* [MNT] update ``python`` version to 3.12 (:pr:`221`) :user:`fkiraly`
* [MNT] 0.6.0 deprecation actions (:pr:`225`) :user:`fkiraly`


[0.5.2] - 2023-10-03
====================

Release with minor improvements.

* [ENH] move tests for dependency checks and ``deep_equals``
  to ``utils`` module (:pr:`217`) :user:`fkiraly`
* [ENH] meta-object mixins (:pr:`216`) :user:`fkiraly`
* [DOC] update ``sktime`` links (:pr:`219`) :user:`fkiraly`


[0.5.1] - 2023-08-14
====================

Release with minor improvements and bugfixes.

Enhancements
------------

* [ENH] remove ``sklearn`` dependency in ``test_get_params`` (:pr:`212`) :user:`fkiraly`

Documentation
-------------

* [DOC] landing page updates (:pr:`188`) :user:`fkiraly`

Maintenance
-----------

* [MNT] separate windows CI element from unix based CI (:pr:`209`) :user:`fkiraly`
* [MNT] convert ``black`` ``extend-exclude`` parameter to single string
  (:pr:`207`) :user:`fkiraly`
* [MNT] update ``__init__`` version (:pr:`210`) :user:`fkiraly`
* [MNT] fix linting issue from newest pre-commit versions (:pr:`211`) :user:`fkiraly`

Fixes
-----

* [BUG] fix for ``get_fitted_params`` in ``_HeterogenousMetaEstimator``
  (:pr:`191`) :user:`fkiraly`


[0.5.0] - 2023-06-21
====================

Maintenance release at python 3.7 end-of-life.

Removes support for python 3.7.


[0.4.6] - 2023-06-16
====================

Bugfix release:

* [BUG] fix clone for nested sklearn estimators (:pr:`195`)
  :user:`fkiraly`, :user:`hazrulakmal`
* [BUG] fix faulty ``suppress_import_stdout`` in ``all_objects`` (:pr:`193`)
  :user:`fkiraly`


[0.4.5] - 2023-05-14
====================

Dummy release for ``aarch64`` support on ``conda`` (added in recipe there).


[0.4.4] - 2023-05-13
====================

Regular maintenance release.

Deprecations and removals
-------------------------

The ``deep_equals`` utility has moved to ``skbase.utils.deep_equals``.
The old location in ``skbase.testing.utils.deep_equals`` will be removed in
``skbase`` 0.6.0, until then it can still be imported from there, with a warning.

Maintenance
-----------

* [MNT] move ``deep_equals`` and dependency checkers from testing to utilities
  to remove accidental coupling to ``pytest`` (:pr:`178`)
  :user:`fkiraly`, :user:`yarnabrina`
* [MNT] test for isolation of developer dependencies,
  and basic ``pytest``-less test for ``BaseObject`` (:pr:`179`, :pr:`183`)
  :user:`fkiraly`

Contributors
------------
:user:`fkiraly`,
:user:`yarnabrina`


[0.4.3] - 2023-05-04
====================

Hotfix for accidental import of ``pytest`` through ``BaseObject.clone``,
including test for ``pytest`` dependency isolation.

Contents
--------

* [BUG] turn off check in ``BaseObject.clone`` (:pr:`176`) :user:`fkiraly`
* [MNT] test for isolation of developer dependencies,
  and basic ``pytest``-less test for ``BaseObject`` (:pr:`179`) :user:`fkiraly`
* [DOC] fix some broken doc links, linting (:pr:`175`) :user:`fkiraly`


[0.4.2] - 2023-05-02
====================

Maintenance update that cleans up dependencies.

Notably, ``scikit-base`` no longer has any core dependencies.

This is as per usage intention as a base module,
therefore this removal is not accompanied by deprecation.

Dependency changes
------------------

* ``scikit-learn``, ``typing-extensions``, and ``pytest`` are no longer
  core dependencies.
  ``pytest`` remains a dependency in ``dev`` and ``test`` dependency sets.
* ``scikit-learn`` is now part of the ``dev`` and ``test`` dependency sets,
  as it is required to test compatibility with ``scikit-learn``
* a dependency conflict has been resolved in the ``docs`` dependency set for
  the docs build,
  by pinning versions

Maintenance
-----------

* [MNT] remove dependency on ``typing-extensions`` (:pr:`167`) :user:`fkiraly`
* [MNT] remove dependency on ``pytest`` (:pr:`168`) :user:`fkiraly`
* [MNT] remove dependency on ``scikit-learn`` (:pr:`171`) :user:`fkiraly`
* [MNT] add ``scikit-learn`` to ``test`` dependency set (:pr:`172`) :user:`fkiraly`
* [MNT] remove ``fail-fast`` flag in CI (:pr:`169`) :user:`fkiraly`
* [MNT] resolve dependency conflict in ``docs`` dependency
  set (:pr:`173`) :user:`fkiraly`


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
- Add equality dunder to ``BaseObject`` to allow ``BaseObject``-s to be compared based
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
