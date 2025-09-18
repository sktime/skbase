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

[0.12.6] - 2025-09-18
=====================

Minor release with feature, bugfix, and maintenance updates.

Contents
--------

* [ENH] update ``_safe_import`` to state in ``sktime`` and ``pytorch_forecasting``
  (:pr:`441`) :user:`fkiraly`
* [ENH] improved `QuickTester`: verbosity levels, plugin structure for fixture
  generation handling (:pr:`446`) :user:`fkiraly`
* [BUG] fix ``TagAliaserMixin`` ``get_tag``
  and ``get_class_tag`` (:pr:`445`) :user:`fkiraly`
* [MNT] Check versions in wheels workflow (:pr:`440`) :user:`szepeviktor`
* [MNT] [Dependabot](deps): Bump ``actions/setup-node`` from ``4`` to ``5``
  (:pr:`443`) :user:`dependabot[bot]`
* [MNT] [Dependabot](deps): Bump ``actions/setup-python`` from ``5`` to ``6``
  (:pr:`444`) :user:`dependabot[bot]`
* [pre-commit.ci] pre-commit autoupdate (:pr:`447`) :user:`pre-commit-ci[bot]`

Contributors
------------

:user:`fkiraly`,
:user:`szepeviktor`


[0.12.5] - 2025-08-17
=====================

Minor release with maintenance updates.

Contents
--------

* [ENH] ensure ``_get_installed_packages`` does not break in case of
  incomplete or corrupted package metadata (:pr:`433`) :user:`fkiraly`
* [MNT] remove deprecated ``fix-encoding-pragma`` hook from ``pre-commit``
  (:pr:`438`) :user:`fkiraly`
* [MNT] [Dependabot](deps): Bump ``actions/download-artifact``
   from 4 to 5 (:pr:`434`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump ``actions/checkout``
  from 4 to 5 (:pr:`436`) :user:`dependabot`
* [pre-commit.ci] pre-commit autoupdate (:pr:`435`) :user:`pre-commit-ci[bot]`


[0.12.4] - 2025-07-23
=====================

Minor release with maintenance updates, features, and bugfixes.

Contents
--------

* [ENH] ``QuickTester`` verbose output on passed and failed tests
  if ``raise_exceptions=True`` (:pr:`428`) :user:`fkiraly`
* [MNT] remove ``stefanzweifel/git-auto-commit-action`` from all-contributors workflow
  (:pr:`426`) :user:`fkiraly`
* [pre-commit.ci] pre-commit autoupdate (:pr:`425`) :user:`pre-commit-ci[bot]`
* [pre-commit.ci] pre-commit autoupdate (:pr:`429`) :user:`pre-commit-ci[bot]`
* [DOC] correct macOS reference in README (:pr:`421`) :user:`fkiraly`
* [DOC] add missing docstring argument for ``QuickTester.run_tests``
  (:pr:`430`) :user:`fkiraly`
* [BUG] fix ``_check_soft_dependencies`` error message if version is wrong
  (:pr:`427`) :user:`fkiraly`


[0.12.3] - 2025-05-28
=====================

Minor release with maintenance updates, features, and bugfixes.

Contents
--------

* [ENH] doctest run utility (:pr:`415`) :user:`fkiraly`
* [ENH] improved ``_check_soft_dependencies`` utility: case sensitivity, disjunction
  (:pr:`417`) :user:`fkiraly`
* [MNT] use ``macos-latest`` and ``ubuntu-latest`` in release workflow
  (:pr:`411`, :pr:`420`) :user:`fkiraly`
* [MNT] update ``nodevdeps`` runner to latest ``ubuntu`` (:pr:`416`) :user:`fkiraly`
* [MNT] replace deprecated ``windows-2019`` runner with ``windows-latest`` in ``wheels``
  release workflow (:pr:`432`) :user:`fkiraly`
* [BUG] ensure ``all_objects`` handles decorators properly (:pr:`418`) :user:`fkiraly`
* [BUG] fix ``TagAliaserMixin`` missing warnings (:pr:`414`) :user:`fkiraly`


[0.12.2] - 2025-04-03
=====================

Minor release with maintenance updates, features, and bugfixes.

Contents
--------

* [ENH] refactor repetitive clone tests with pytest.mark.parametrize, fixes #170
  (:pr:`392`) :user:`JahnaviDhanaSri`
* [pre-commit.ci] pre-commit autoupdate
  (:pr:`393`, :pr:`397`, :pr:`398`, :pr:`401`, :pr:`403`, :pr:`408`)
  :user:`pre-commit-ci`
* [MNT] [Dependabot](deps): Update ``sphinx-gallery`` requirement
  from ``<0.19.0`` to ``<0.20.0`` (:pr:`400`) :user:`dependabot`
* [MNT] Add CI for updating contributors (:pr:`395`) :user:`Spinachboul`
* [MNT] remove ``tj-actions`` from CI (:pr:`404`) :user:`fkiraly`
* [DOC] Update Contributors List and Badge (:pr:`394`, :pr:`399`) :user:`Spinachboul`
* [DOC] minor typo fix in code comment (:pr:`402`) :user:`fkiraly`
* [DOC] minor documentation fixes (:pr:`405`) :user:`fkiraly`
* [BUG] fix ``deep_equals`` for ``pandas.Index`` (:pr:`407`) :user:`XinyuWuu`

Contributors
------------

:user:`fkiraly`,
:user:`JahnaviDhanaSri`,
:user:`Spinachboul`,
:user:`XinyuWuu`

[0.12.1] - 2025-01-05
=====================

Minor release with maintenance updates, features, and bugfixes.

Contents
--------

* [ENH] ``allow_empty`` option in ``_MetaObjectMixin._check_objects``
  (:pr:`386`) :user:`fkiraly`
* [ENH] sync dependency checker utilities with ``sktime`` (:pr:`388`) :user:`fkiraly`
* [BUG] Accepting prereleases as valid python version (:pr:`389`) :user:`Abelarm`
* [MNT] [Dependabot](deps): Bump ``codecov/codecov-action`` from ``4`` to ``5``
  (:pr:`385`) :user:`dependabot`
* [pre-commit.ci] pre-commit autoupdate (:pr:`387`) :user:`pre-commit-ci`

Contributors
------------

:user:`Abelarm`,
:user:`fkiraly`


[0.12.0] - 2024-11-13
=====================

Feature release, and python 3.8 End-of-Life update.

Core interface changes
----------------------

* the logic of ``clone`` has been refactored to a type-based plugin architecture,
  with plugins inheriting from ``BaseCloner``. The default behaviour of ``clone``
  remains unchanged, and a new plugin for ``scikit-learn`` estimators has been added,
  dispatching to ``sklearn`` ``clone``. This change is not breaking, and it fixes
  some reported bugs around ``sklearn`` config handling.
* ``clone`` plugins can be customized by extenders by overriding the
  ``_get_clone_plugins`` method, which can return a list of ``BaseCloner`` classes,
  functioning as plugins.

Enhancements
------------

* [ENH] refactor ``_clone`` to a plugin structure (:pr:`381`) :user:`fkiraly`
* [ENH] add ``_get_clone_plugins`` to allow packages to customize clone plugins
  (:pr:`383`) :user:`fkiraly`

Maintenance
-----------

* [MNT] manage ``python 3.8`` end-of-life (:pr:`378`) :user:`fkiraly`
* [MNT] fix failing ``code-quality`` CI step (:pr:`377`) :user:`fkiraly`
* [MNT] [Dependabot](deps): Update sphinx-gallery requirement
  from ``<0.18.0`` to ``<0.19.0`` (:pr:`375`) :user:`dependabot`
* [MNT] [Dependabot](deps): Update ``sphinx-issues`` requirement
  from ``<5.0.0`` to ``<6.0.0`` (:pr:`376`) :user:`dependabot`
* [pre-commit.ci] pre-commit autoupdate (:pr:`379`) :user:`pre-commit-ci`
* [pre-commit.ci] pre-commit autoupdate (:pr:`382`) :user:`pre-commit-ci`


[0.11.0] - 2024-10-07
=====================

Maintenance release with full support for ``python 3.13``,
and other minor improvements.

Contents
--------

* [MNT] full support for ``python 3.13`` (:pr:`372`) :user:`fkiraly`
* [DOC] improved docstrings for ``BaseObject`` (:pr:`369`) :user:`fkiraly`
* [DOC] merge docstring of ``NotFittedError`` with ``sktime``
  (:pr:`371`) :user:`fkiraly`
* [ENH] merge ``sktime`` ``BaseEstimator` into ``skbase`` ``BaseEstimator``
  (:pr:`370`) :user:`fkiraly`
* [pre-commit.ci] pre-commit autoupdate (:pr:`374`) :user:`pre-commit-ci`


[0.10.1] - 2024-09-29
=====================

Maintenance release with experimental ``python 3.13`` wheels.
Full 3.13 support will be added with ``scikit-base 0.11.0``.

Contents
--------

* [pre-commit.ci] pre-commit autoupdate (:pr:`364`) :user:`pre-commit-ci`
* [MNT] updates ``scikit-learn`` soft dependency checks to use PEP 440 name
  (:pr:`366`) :user:`fkiraly`
* [MNT] experimental ``python 3.13`` wheels and ``3.13-rc.2`` testing
  (:pr:`365`) :user:`fkiraly`


[0.10.0] - 2024-09-22
=====================

Maintenance release with scheduled changes and deprecations.

Contents
--------

* [pre-commit.ci] pre-commit autoupdate (:pr:`358`) :user:`pre-commit-ci`
* [ENH] add test that html repr of objects does not crash (:pr:`359`) :user:`fkiraly`
* [ENH] ``clone`` method to handle nested ``dict`` (:pr:`362`) :user:`fkiraly`
* [DOC] Replace use of "estimator" term in base object interfaces
  with more general references (:pr:`293`) :user:`tpvasconcelos`
* [MNT] 0.10.0 deprecations and change actions (:pr:`360`) :user:`fkiraly`

Contributors
------------

:user:`fkiraly`,
:user:`tpvasconcelos`


[0.9.0] - 2024-08-23
====================

Maintenance release with scheduled changes and deprecations.

Deprecations and removals
-------------------------

* In ``all_objects``, the meaning of ``filter_tags`` arguments ot type ``str``,
  and iterable of ``str``, has changed as scheduled.
  Prior to 0.9.0, ``str`` or iterable of ``str`` arguments
  selected objects that possess the
  tag(s) with the specified name, of any value.
  From 0.9.0 onwards, ``str`` or iterable of ``str``
  will select objects that possess the tag with the specified name,
  with the value ``True`` (boolean). See ``scikit-base`` issue #326 for the rationale
  behind this change.
  To retain previous behaviour, that is,
  to select objects that possess the tag with the specified name, of any value,
  use a ``dict`` with the tag name as key, and ``re.Pattern('*?')`` as value.
  That is, ``from re import Pattern``, and pass ``{tag_name: Pattern('*?')}``
  as ``filter_tags``, and similarly with multiple tag names.

Contents
--------

* [MNT] 0.9.0 deprecations and change actions (:pr:`355`) :user:`fkiraly`


[0.8.3] - 2024-08-23
====================

Regular maintenance release.

Contents
--------

* [MNT] release workflow: Upgrade deprecated pypa action parameter
  (:pr:`349`) :user:`szepeviktor`
* [MNT] pre-commit autoupdate by (:pr:`353`) :user:`pre-commit-ci`
* [ENH] StderrMute context manager (:pr:`350`) :user:`XinyuWuu`
* [BUG] fix dependency checkers in case of multiple distributions available in
  environment, e.g., on databricks (:pr:`352`) :user:`fkiraly`, :user:`toandaominh1997`
* [ENH] safer ``get_fitted_params`` default functionality to avoid exception
  on ``getattr`` (:pr:`353`) :user:`fkiraly`

Contributors
------------

:user:`fkiraly`,
:user:`szepeviktor`,
:user:`toandaominh1997`,
:user:`yarnabrina`


[0.8.2] - 2024-08-02
====================

Regular maintenance release.

Contents
--------

* [ENH] prevent imports in ``_check_soft_dependencies``
  (:pr:`340`) :user:`fkiraly`, :user:`yarnabrina`
* [ENH] sync dependency checkers with ``sktime`` (:pr:`345`) :user:`fkiraly`
* [pre-commit.ci] pre-commit autoupdate (:pr:`342`) :user:`pre-commit-ci`
* [MNT] [Dependabot](deps): Update ``sphinx-gallery`` requirement
  from ``<0.17.0`` to ``<0.18.0`` (:pr:`343`) :user:`dependabot`
* [MNT] [Dependabot](deps): Update ``sphinx`` requirement
  from ``!=7.2.0,<8.0.0`` to ``!=7.2.0,<9.0.0`` (:pr:`344`) :user:`dependabot`
* [MNT] Move release CI to macos-12 image (:pr:`347`) :user:`szepeviktor`

Contributors
------------

:user:`fkiraly`,
:user:`szepeviktor`,
:user:`yarnabrina`


[0.8.1] - 2024-06-20
====================

Regular bugfix and maintenance release.

Core interface changes
----------------------

* ``get_param_names`` now allows users to return the parameter names in the same order
  as in the`` ``__init__`` method, by passing the argument ``sort=False``.

Contents
--------

* [ENH] option to return ``BaseObject.get_param_names`` in the same order as in the
  ``__init__`` (:pr:`335`) :user:`fkiraly`
* [ENH] refactor - move ``StdoutMute`` context manager to ``utils``
  (:pr:`338`) :user:`fkiraly`
* [MNT] ``numpy 2`` compatibility of some tests (:pr:`337`) :user:`fkiraly`
* [pre-commit.ci] pre-commit autoupdate  (:pr:`336`) :user:`pre-commit-ci`


[0.8.0] - 2024-05-25
====================

Feature update for ``all_objects``, bugfix and maintenance release.

Core interface changes
----------------------

* ``all_objects`` now allows filtering tag values by ``re.Pattern`` regular expressions
  passed as query values via ``filter_tags``.

Deprecations and removals
-------------------------

* In ``all_objects``, the meaning of ``filter_tags`` arguments ot type ``str``,
  and iterable of ``str``, will change from ``scikit-base 0.9.0``.
  Currently, ``str`` or iterable of ``str`` arguments select objects that possess the
  tag(s) with the specified name, of any value.
  From 0.9.0 onwards, ``str`` or iterable of ``str``
  will select objects that possess the tag with the specified name,
  with the value ``True`` (boolean). See ``scikit-base`` issue #326 for the rationale
  behind this change.
  To retain previous behaviour, that is,
  to select objects that possess the tag with the specified name, of any value,
  use a ``dict`` with the tag name as key, and ``re.Pattern('*?')`` as value.
  That is, ``from re import Pattern``, and pass ``{tag_name: Pattern('*?')}``
  as ``filter_tags``, and similarly with multiple tag names.

Contents
--------

* [BUG] fix permanently muted ``stdout`` after ``all_objects`` call
  (:pr:`328`) :user:`fkiraly`
* [ENH] refactor - simplify ``all_objects`` logic and add cache for efficient lookup
  (:pr:`331`) :user:`fkiraly`
* [ENH] ``all_objects`` retrieval filtered by regex applied to tag values, deprecation
  of "has tag" condition in favour of "tag is True" (:pr:`329`) :user:`fkiraly`
* [MNT] [Dependabot](deps): Update ``sphinx-design`` requirement
  from ``<0.6.0`` to ``<0.7.0`` (:pr:`332`) :user:`dependabot`


[0.7.8] - 2024-05-10
====================

Regular bugfix and maintenance release.

Contents
--------

* [BUG] safer comparison in ``deep_equals`` if ``np.any(x != y)`` does not result in
  boolean (:pr:`323`) :user:`fkiraly`
* [pre-commit.ci] pre-commit autoupdate (:pr:`322`) :user:`dependabot`
* [MNT] [Dependabot](deps): Update ``sphinx-gallery`` requirement
  from ``<0.16.0`` to ``<0.17.0`` (:pr:`321`) :user:`dependabot`


[0.7.7] - 2024-04-17
====================

Small hotfix release.

Contents
--------

* Revert "[MNT] rename ``testing.utils.inspect`` to avoid shadowing of ``inspect``"
  (:pr:`319`) :user:`fkiraly`


[0.7.6] - 2024-03-02
====================

Minor feature and bugfix release.

Contents
--------

* [ENH] ``deep_equals`` support for nested ``np.ndarray`` (:pr:`314`) :user:`fkiraly`
* [BUG] fix ``sklearn`` compatibility of ``_VisualBlock`` (:pr:`310`) :user:`fkiraly`
* [pre-commit.ci] pre-commit autoupdates
  (:pr:`306`, :pr:`307`, :pr:`308`, :pr:`312`, :pr:`315`) :user:`pre-commit-ci`
* [MNT] rename ``testing.utils.inspect`` to avoid shadowing of ``inspect``
  (:pr:`316`) :user:`fkiraly`


[0.7.5] - 2024-03-02
====================

Small hotfix release.

Contents
--------

* [BUG] fix ``deep_equals`` on objects which have ``__len__`` but ``len(obj)``
  causes exception (:pr:`303`) :user:`fkiraly`


[0.7.4] - 2024-03-01
====================

Small hotfix release.

Contents
--------

* [BUG] preserve exception type raised by ``get_test_params``
  (:pr:`300`) :user:`fkiraly`


[0.7.3] - 2024-02-29
====================

Feature and bugfix release.

Core interface changes
----------------------

* ``all_objects`` now allows filtering for arbitrary parent classes, not just classes
  inheriting from ``BaseObject``. This is useful for looking up objects in a third
  party package that are not part of the ``skbase`` hierarchy.


Enhancements
------------

* [ENH] allow arbitrary base class in ``all_objects`` (:pr:`284`) :user:`fkiraly`
* [ENH] improved exception feedback for test instance generation methods
  of ``BaseObject`` (:pr:`286`) :user:`fkiraly`
* [ENH] estimator soft dependency check utilities (:pr:`285`) :user:`fkiraly`
* [ENH] Refactor ``BaseObject.clone`` (:pr:`281`) :user:`tpvasconcelos`

Fixes
-----

* [BUG] Fix ``deep_equals`` for ``pandas.Index`` of different length
  (:pr:`290`) :user:`MBristle`

Documentation
-------------

* [DOC] remove accidental duplicated section in ``get_test_params``
  docstring (:pr:`292`) :user:`fkiraly`
* [DOC] add yarnabrina to ``all-contributorsrc`` (:pr:`294`) :user:`fkiraly`

Maintenance
-----------

* [MNT] add ``codecov` config ``yml``, remove CI failure condition
  (:pr:`296`) :user:`fkiraly`
* [MNT] remove unnecessary CI triggers for release branches (:pr:`298`) :user:`fkiraly`
* [pre-commit.ci] pre-commit autoupdate by (:pr:`289`) :user:`@pre-commit-ci`
* [MNT] [Dependabot](deps): Bump codecov/codecov-action from ``3`` to ``4``
  (:pr:`283`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump pre-commit/action from ``3.0.0`` to ``3.0.1``
  (:pr:`287`) :user:`dependabot`

Contributors
------------

:user:`fkiraly`,
:user:`MBristle`,
:user:`tpvasconcelos`


[0.7.2] - 2024-01-31
====================

Feature and bugfix release.

Core interface changes
----------------------

* all ``BaseObject`` descendants now possess a method ``set_random_state``.
  This can be used for nested setting of ``random_state`` variables,
  and is useful for ensuring reproducibility in nested estimators.
  (:pr:`268`) :user:`fkiraly`
* ``all_objects`` now supports filtering for list-valued tags in ``filter_tags``
  as a convenience feature.
  When the query value is a single value or a list, the filter condition is
  that the tag value and the query value have at least one element in common.
  (:pr:`273`) :user:`fkiraly`

Enhancements
------------

* [ENH] ``all_objects`` ``filter_tags`` to function with list-of tags
  (:pr:`273`) :user:`fkiraly`
* [ENH] Random state handling, ``set_random_state`` method (:pr:`268`) :user:`fkiraly`

Fixes
-----

* [BUG] Fix cloning of config for nested objects (:pr:`276`) :user:`tpvasconcelos`

Documentation
-------------

* [DOC] lint changelog (:pr:`267`) :user:`fkiraly`

Maintenance
-----------

* [pre-commit.ci] pre-commit autoupdate (:pr:`274`) :user:`precommit-ci`
* [MNT] [Dependabot](deps): Bump ``actions/dependency-review-action`` from 3 to 4
  (:pr:`269`) :user:`dependabot`
* [MNT] [Dependabot](deps-dev): Update ``sphinx-issues`` requirement
  from ``<4.0.0`` to ``<5.0.0`` (:pr:`271`) :user:`dependabot`
* [MNT] [Dependabot](deps): Bump styfle/cancel-workflow-action
  from ``0.12.0`` to ``0.12.1`` (:pr:`272`) :user:`dependabot`
* [MNT] Add common IDE files to ``.gitignore`` (:pr:`277`) :user:`tpvasconcelos`

Contributors
------------
:user:`fkiraly`,
:user:`tpvasconcelos`


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
