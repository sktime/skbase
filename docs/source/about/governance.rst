.. _governance:

==========
Governance
==========

Overview
========

``baseobject`` is a consensus-based project that is part of the ``sktime`` community.
Anyone with an interest in the project can join the community, contribute to
the project, and participate in the governance process. This document describes
how that participation takes place, which roles we have in our community,
how we make decisions, and how we acknowledge contributions.

.. list-table::
   :header-rows: 1

   * - Section
     - Purpose
   * - :ref:`Code of conduct <gov_coc>`
     - How members of the community should interact
   * - :ref:`roles`
     - The roles used in ``baseobjects's`` community and what rights and
       responsibilities they have
   * - :ref:`decision-making <decisions>`
     - How and by whom decisions are made
   * - :ref:`acknowledging-contributions <acknowledging>`
     - How we acknowledge contributions
   * - :ref:`outlook`
     - What we may change in the future

.. _gov_coc:

Code of Conduct
===============

The ``baseobject`` project believes that everyone should be able to participate
in our community without fear of harrassment or discrimination (see our
:ref:`Code of Conduct guide <coc>`). Check out our
:ref:`contributing guide <contrib_guide>` for more details on how you can get
involved in the community.


Roles
=====

``baseobject`` distinguishes between the following key community roles. We
describe each role's rights and responsibilities, and appointment
process in more detail below.

.. list-table::
   :header-rows: 1

   * - Role
     - Rights/responsibilities
     - Appointment
   * - :ref:`contribs`
     - \-
     - Concrete contribution
   * - :ref:`core-devs`
     - Direct write access, issue/PR management, veto right, voting, nomination
     - Nomination by core developers, vote by core developers, 2/3 majority
   * - :ref:`coc-committee-members`
     - CoC maintenance, investigation and enforcement
     - Nomination by core developers, vote by core developers, 2/3 majority and
       simple CoC majority
   * - :ref:`cc-members`
     - Conflict resolution, technical leadership, project management
     - Nomination by core developers, vote by core developers, 2/3 majority and
       simple CC majority

.. _contribs:

Contributors
------------

Contributors are community members who have contributed in concrete ways
to the project. Anyone can become a contributor, and contributions can
take many forms – not only code – as detailed in the
:ref:`contributing guide <contributing>`

For more details on how we acknowledge contributions,
see the :ref:`acknowledging-contributions` section below.

All of our contributors are listed under the `contributors <contributors.md>`_
section of our documentation.

.. _core-devs:

Core developers
---------------

Core developers are contributors who have shown dedication to the continued
development of the project through ongoing engagement with the community (
see the :ref:`core development team <team>`).

Core developers help ensure the smooth functioning of the project by:

- managing issues and Pull Requests
- closing resolved issues
- reviewing others contributions in accordance with the project
  :ref:`reviewers guide <rev_guide>`)
- approving and merging Pull Requests
- participating in the project's decision making process
- nominating new core developers and Community Council members

Community members can become core developers if they are nominated by an existing
core developer and they receive affirmative votes from two-thirds of
existing core developers over the course of a business day voting period.

Core developers who continue to participate in their role's duties, can serve
as long as they would like. Core developers will move to inactive status if
they do not engage in their role over a 12 month period; they can also
resign at any time.

.. _cc-members:

Community Council members
-------------------------

Community Council (CC) members are core developers with additional rights and
responsibilities for maintaining the project
(see the :ref:`community council members <team>`).

This includes:

- providing technical direction
- strategic planning, roadmapping and project management
- managing community infrastructure (e.g., Github repositories, continuous integration
  accounts, etc)
- fostering collaborations with external organisations
- avoiding deadlocks and ensuring a smooth functioning of the project

Community members can become CC members if they are nominated by an existing
core developers and receive affirmative votes from two-thirds of core developers
and a simple majority (with tie breaking) of existing CC members. Like other
appointment votes, the voting will take place in private communication
channels and will be anonymous.

CC members who continue to engage with the project can serve as long as they'd like.
However, CC members who do not actively engage in their CC responsibilities are
expected to resign. In the event, a CC member who no longer engages in their
responsibilities does not resign, the remaining CC members and core developers
can vote to remove them (same rules as appointment).

.. _decisions:

Decision making
===============

``baseobject's`` decision-making process is designed to take into account
feedback from all community members and strives to find consensus. In cases,
where consensus cannot be found, it seeks to avoid deadlocks.

To accomplish this, this section outlines the decision-making process used
by the project.

Where we make decisions
-----------------------

Most of the project's decisions and voting takes place on the project’s `issue
tracker <https://github.com/sktime/baseobject/issues>`__,
`pull requests <https://github.com/sktime/baseobject/pulls>`__ or an
:ref:`steps`. However, some sensitive discussions and all appointment votes
occur on private chats.

Types of decisions
------------------

The consensus based decision-making process for major types of project
decisions are summarized below.

.. list-table::
   :header-rows: 1

   * - Type of change
     - Decision making process
   * - Code additions or changes
     - :ref:`Lazy consensus <lazy>`
   * - Documentation changes
     - :ref:`Lazy consensus <lazy>`
   * - Changes to the API design, hard dependencies, or supported versions
     - :ref:`Lazy consensus <lazy>` based on an :ref:`BEP <gov_bep>`
   * - Changes to sktime's governance
     - :ref:`Lazy consensus <lazy>` based on an :ref:`BEP <gov_bep>`
   * - Appointment to core developer or Community Council status
     - Anonymous voting


How we make decisions
---------------------

.. _lazy:

Lazy consensus
^^^^^^^^^^^^^^

``baseobject`` uses "lazy" consensus for many decisions, by seeking a resolution
that has no objections among the core development team. For a change to be
approved "lazily", core developers must be given a *reasonable* amount of time
to consider it, and it must receive approval from at least one core developer
and no rejections (excercise of core developer veto right).

Since most decisions (excluding appointments and other sensitive issues) occur
in the project's repository, core developers are expected to express their
consensus (or veto) in the comments of the project's issues and Pull Requests.

.. _gov_bep:

``baseobject`` enhancement proposals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Decisions about the project's design have a more detailed approval process,
commensurate with their broader impact on the project. Any changes
to the project's core API design, hard dependencies or supported versions
should first be presented in a ``baseobject`` enhancement proposal (BEP).

This ensures a greater amount of information is available to decision-makers.
Accordingly, the timeline for accepting a proposed BEP is typically longer
than smaller project changes. However, reasonable effort will be made to
review the BEP promptly.

See the developer guide for more information on creating a :ref:`BEP <bep>`.

Resolving conflicts
^^^^^^^^^^^^^^^^^^^

When consensus can't be found lazily, any core developer can call for a vote
on a topic. This triggers a 5 day voting period, where core developers vote
for or against the proposed changes (abstentions are allowed) by commenting
on the relevant issue or Pull Request.

Proposed changes must receive two-thirds of the votes casts. In the event a
a proposed change does not gather the necesssary votes, then:

- The core developer who triggered the vote can choose to drop the issue
- The proposed changes can be escalated to the CC, who will try to resolve
  the conflict

The CC will seek to understand the core development team's varied viewpoints, and
and arrive at consensus, before bringing the topic up for a simple majority
vote of CC members within a month. Any CC decision must be supported by an
:ref:`gov_bep`, which has been made public and discussed before the vote.

.. _acknowledging:

Acknowledging contributions
===========================

The ``baseobject`` project values all kinds
of contributions and the development team is committed to recognising
each of them fairly.

The project follows the `all-contributors <https://allcontributors.org>`_
specification to recognise all contributors, including those that don’t
contribute code. Please see our list of `all contributors <contributors.md>`_.

Please let us know or open a PR with the appropriate changes to
`baseobject/.all-contributorsrc
<https://github.com/sktime/baseobject/blob/main/.all-contributorsrc>`_
if we have missed anything.

Note that contributors do not own their contributions. ``baseobject`` is an
open-source project, and all code is contributed under `our open-source
license <https://github.com/sktime/baseobject/blob/main/LICENSE>`_.
All contributors acknowledge that they have all the rights to the code
they contribute to make it available under this license.

Outlook
=======

As with other parts of the project, the governance may change as the project
matures. We anticipate that as the community grows, we may consider the
following changes:

-  Allow for more time to discuss changes, and more time to cast vote
   when no consensus can be found,
-  Require more positive votes (less lazy consensus) to accept changes
   during consensus seeking stage,
-  Reduce time for maintainers to reply to issues

Suggestions on potential governance changes are also welcome.

References
==========

Our governance model is inspired by various existing governance
structures. In particular, we’d like to acknowledge:

* `sktime’s governance model <https://www.sktime.org/en/latest/governance.html>`_
* `scikit-learn’s governance model <https://scikit-learn.org/stable/governance.html>`_
