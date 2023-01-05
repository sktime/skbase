.. _release:

Release Management
=====================================

This section provides detailed instructions used to release a new version of ``skbase``.

This task is carried out by core developers with write access to the ``skbase``
repository and designated as release managers by the
:ref:`Community Council <cc-members>`.

Summary of release process
--------------------------

The release process includes, in sequence:

* :ref:`prepare for an upcoming release <cycle_process>`
* :ref:`get the release ready <release_version_prep>`
* :ref:`release on PyPi <pypi_release>`
* :ref:`release on conda <conda_release>`
* troubeleshooting and accident remediation, if applicable (see troubeleshooting
  tips in each of the prior sections)

Details follow below.

.. _cycle_process:

Release preparation cycle
^^^^^^^^^^^^^^^^^^^^^^^^^

``skbase`` aims for a release every month, typically coinciding with the start of
the month. To ensure releases go smoothly, the following steps are taken leading
up to each release:

1. 1 week before release date, update the release project board and alert
   project contributors of upcoming release on slack.
2. For major releases or substantial features, optionally extend the release cycle,
   if needed, so that the changes can be completed and incorporated in the release.
   If a release will be delayed, notify project contributors on slack.
3. All changes to the main branch of the repository are frozen 1 day prior to the
   release. At this point only the release managers (for this release) should
   merge any Pull Requests. Remind core developers of the timing of the feature
   freeze on slack when announcing the upcoming release date. Remind core developers
   of the feature freeze again 1 day prior to its start. Make sure to keep
   core developers in the loop if any delays or extensions to the feature freeze arise.
4. If "must have" Pull Requests are not merged by the planned release date, the
   release manager should coordinate with the Community Council to either delay
   the release date and extend freeze period, or move the Pull Requests target
   completion to a later release.

.. _release_version_prep:

Preparing the release version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The release process is as follows, on high-level:

1. Ensure deprecation actions are carried out. Deprecation actions for a version
   should be marked by "version number" annotated comments in the code. E.g.,
   for the release 0.2.0, search for the string 0.2.0 in the code and carry out
   the described deprecation actions. Collect list of deprecation actions in an issue,
   as they will have to go in the release notes. Deprecation actions should be merged
   only by release managers.

2. Create a "release" Pull Request from a branch following the naming pattern
   ``release/v0.x.y``. This Pull Request should:

   - Update the package version numbers
     (see :ref:`version number locations <version_number_locs>`)
   - Add copmlete release notes
     (see :ref:`generating release notes <generate_release_notes>`)
   - Update the ``switcher.json`` file located at ``./docs/source/_static/``
     relative to the proejct's root. This involves creating a new entry for the
     prior release (which was the "stable" doc release previously) and rename
     the stable release to reference the updated version number.

3. The PR and release notes should be reviewed by the other core developers,
   then merged once tests pass.

4. Create a GitHub draft release with a new tag following the syntax
   v[MAJOR].[MINOR].[PATCH]. E.g., the string ``v0.12.0`` for version 0.12.0.
   The GitHub release notes should contain only "new contributors" and
   "all contributors" section, and otherwise link to the release notes in the
   changelog, following the pattern of current GitHub release notes.

.. _pypi_release:

``pypi`` release and release validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

5. Publish the GitHub draft release. Creation of the new tag will trigger the
   ``pypi`` release CI/CD.

6. Wait for the ``pypi`` release CI/CD to finish. If tests fail due to sporadic
   failures unrelated to the content being released, restart the CI/CD routine.
   If tests fail genuinely, something went wrong in the above steps, investigate,
   fix, and repeat. Common possibilities are core devs not respecting the feature
   freeze period, new releases of dependencies that happen in the period between
   release PR and release.

7. Once release CI/CD has passed, check the ``skbase`` version on ``pypi``,
   this should be the new version. It should be checked that all wheels have been
   uploaded, `here <https://pypi.org/simple/skbase/>`__. As a test, one install
   of ``skbase`` in a new ``python`` environment should be carried out
   according to the install instructions (choose an arbitrary version/OS).
   If the install does not succeed or wheels have not been uploaded, urgent
   action to diagnose and remedy must be taken. All core developers should be
   informed of the situation through mail-all in the core developer channel on slack.
   In the most common case, the install instructions need to be updated.
   If wheel upload has failed, the tag in 5. needs to be deleted and recreated.
   The tag can be deleted using the ``git`` command
   ``git push --delete origin tagname`` from a local repo.

.. _conda_release:

``conda`` release and release validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

8. If the release on ``pypi`` has succeeded, there should be an automated
   release PR created against the ``skbase`` conda-forge repo:
   https://github.com/conda-forge/skbase-feedstock.

  .. note:: Manual creation of release pull request
     In cases where the release PR is not created automatically it can be created
     and submitted manually. For general guidelines related to maintaining conda
     feedstcok packages see
     `conda-forge package <https://conda-forge.org/docs/maintainer/updating_pkgs.html>`_.

     After forking and cloning the repo, edit the ``meta.yml`` file by:

     - incrementing the version in the line that contains ``{% set version = "0.X.Y" %}``
     - pasting the sha256 sum of the source archive from github in the
       ``source/sha256`` section

    Once finished, submit the PR and ask for review.

9. The conda release PR needs to be reviewed and in dependencies should be
   checked against any changes in the main ``skbase`` repo. In case the dependencies
   (or python version support) have changes, the ``meta.yml`` file in the conda
   recipe needs to be updated to reflect those changes.

10. Once reviewed, the conda release PR should merged, and it will automatically
    trigger a release of the conda package.

11. After 1h, it should be checked whether the package has been released on conda.
    Once the package is available on ``conda``, a test install should be carried out
    to validate the release. Should either of these fail, alert the core developers
    and follow an urgent action plan in line with the description in step 7.

.. _version_number_locs:

Version number locations
------------------------

Version numbers need to be updated in:

* root ``__init__.py``
* ``README.md``
* ``pyproject.toml``

.. _generate_release_notes:

Generating release notes
------------------------

Release notes can be generated using the ``build_tools.changelog.py`` script,
and should be placed at the top of the ``changelog.rst``. Generally, release notes
should follow the general pattern of previous release notes, with sections:

* highlights
* dependency changes, if any
* deprecations and removals, if any. In PATCH versions, there are no deprecation
  actions, but there can be new deprecations.
  Deprecation action usually happen with the MINOR release cycle.
* core interface changes, if any. This means, changes to the base class interfaces.
  Only MINOR or MAJOR releases should have core interface changes that are not
  downwards compatible.
* enhancements, by module/area
* documentation
* maintenance
* bugfixes
* all contributor credits
