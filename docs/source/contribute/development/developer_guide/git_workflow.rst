.. _git_workflow:

Git and GitHub workflow
=======================

.. note::

   If your not familiar with ``git`` you may want to start by reviewing
   `Git's documentation <https://git-scm.com/doc>`_ and then trying
   out the workflow. If you get stuck, chat with us on
   `Slack <https://join.slack.com/t/sktime-group/shared_invite/zt-1cghagwee-sqLJ~eHWGYgzWbqUX937ig>`_.

The preferred workflow for contributing to ``baseobject's`` repository is to
fork the `main repository <https://github.com//sktime/baseobject>`_ on GitHub,
clone your fork locally and create a development installation, and then create
a new feature branch for your development.

1.  Fork the `project
    repository <https://github.com/sktime/baseobject>`_ by
    clicking on the 'Fork' button near the top right of the page. This
    creates a copy of the code under your GitHub user account. For more
    details on how to fork a repository see `this
    guide <https://help.github.com/articles/fork-a-repo/>`_.

2.  Follow ``baseobject's`` :ref:`development installation <dev_install>` instructions.

3.  Configure and link the remote for your fork to the upstream
    repository:

    .. code:: bash

       git remote -v
       git remote add upstream https://github.com/sktime/baseobject.git

4.  Verify the new upstream repository you've specified for your fork:

    .. code:: bash

       git remote -v
       > origin    https://github.com/<username>/baseobject.git (fetch)
       > origin    https://github.com/<username>/baseobject.git (push)
       > upstream  https://github.com/sktime/baseobject.git (fetch)
       > upstream  https://github.com/sktime/baseobject.git (push)

5.  `Sync
    <https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork>`_
    the ``main`` branch of your fork with the upstream repository:

    .. code:: bash

       git fetch upstream
       git checkout main
       git merge upstream/main

    .. hint::

        You can use these same instructions to sync another branch by replacing
        the "main" branch with the name of the other branch you want to sync.

6.  Create a new ``feature`` branch from the ``main`` branch to hold
    your changes:

    .. code:: bash

       git checkout main
       git checkout -b <name-of-feature-branch>

    .. note::

        Always use a ``feature`` branch. It's good practice to never work on
        the ``main`` branch. Name the ``feature`` branch after your contribution.

7.  Develop your contribution on your feature branch. Add changed files
    using ``git add`` and then ``git commit`` files to record your
    changes in Git:

    .. code:: bash

       git add <modified_files>
       git commit

8.  When finished, push the changes to your GitHub account with:

    .. code:: bash

       git push --set-upstream origin my-feature-branch

9.  Follow
    `these instructions
    <https://help.github.com/articles/creating-a-pull-request-from-a-fork>`_
    to create a pull request from your fork. If your work is still work in progress,
    make sure to open a draft pull request.

    .. note::

        We recommend opening a pull request early, so that other contributors
        become aware of your work and can give you feedback early on.

10. To add more changes related to this feature, simply repeat steps 7 - 8.


    .. note::

        Pull requests are updated automatically if you push new changes to the
        same branch. This will trigger ``baseobject's``
        :ref:`continuous integration <ci>` routine to re-run automatically.
