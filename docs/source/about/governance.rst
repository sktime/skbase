.. _governance:

==========
Governance
==========

Overview
========

``skbase`` is a consensus-based project that is part of the ``sktime`` community.
Anyone with an interest in the project can join the community, contribute to
the project, and participate in the governance process. The rest of this document
describes how that participation takes place, which roles we have in our community,
how we make decisions, and how we acknowledge contributions.

.. note::

    As a new project, ``skbase`` has adopted a governance structure similar
    to ``sktime``. In the future this could change as the project grows. But for
    the time being, any governance process not covered by this document, defaults
    to ``sktime's`` process.

.. _gov_coc:

Code of Conduct
===============

The ``skbase`` project believes that everyone should be able to participate
in our community without fear of harrassment or discrimination (see our
:ref:`Code of Conduct guide <coc>`).

Roles
=====

``skbase`` distinguishes between the following key community roles:

- :ref:`Contributors`
- :ref:`Core developers <core-devs>`
- :ref:`Community Council members <cc-members>`

.. _contribs:

Contributors
------------

Anyone can become a contributor by making a concrete contribution
to the project. Contributions can take many forms – not only code – as detailed
in the :ref:`contributing guide <contributing>`

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

The :ref:`core developmer team <team>`  helps ensure the smooth functioning of
the project by:

- ongoing engagement with community
- managing issues and Pull Requests
- closing resolved issues
- reviewing others contributions in accordance with the project
  :ref:`reviewers guide <rev_guide>`)
- approving and merging Pull Requests
- participating in the project's decision making process
- nominating new core developers and Community Council members

Any core developer nominee must receive affirmative votes from two-thirds of
existing core developers over the course of a 5 business day voting period.

Core developers who continue to participate in their role's duties, can serve
as long as they would like. Core developers will move to inactive status if
they do not engage in their role over a 12 month period; they can also
resign at any time.

.. _cc-members:

Community Council members
-------------------------

Community Council (CC) :ref:`team members <team>` are core developers with
additional rights and responsibilities for maintaining the project, including:

- providing technical direction
- strategic planning, roadmapping and project management
- managing community infrastructure (e.g., Github repository, etc)
- fostering collaborations with external organisations
- avoiding deadlocks and ensuring a smooth functioning of the project

CC nominees must be nominated by an existing core developer and receive
affirmative votes from two-thirds of core developers and a simple majority
(with tie breaking) of existing CC members.

CC members who continue to engage with the project can serve as long as they'd like.
However, CC members who do not actively engage in their CC responsibilities are
expected to resign. In the event, a CC member who no longer engages in their
responsibilities does not resign, the remaining CC members and core developers
can vote to remove them (same voting rules as appointment).

.. _decisions:

Decision making
===============

The ``skbase`` community tries to take feedback from all community members into account
when making decisions and strives to find consensus and avoid deadlocks.

To accomplish this, this section outlines the decision-making process used
by the project.

Where we make decisions
-----------------------

Most of the project's decisions and voting takes place on the project’s `issue
tracker <https://github.com/sktime/baseobject/issues>`__,
`pull requests <https://github.com/sktime/baseobject/pulls>`__ or an
:ref:`steps`. However, some sensitive discussions and all appointment votes
occur on private chats.

Core developers are expected to express their consensus (or veto) in the medium
where a given decision takes place. For changes included in the Project's issues
and Pull Requests, this is through comments or Github's built-in review process.

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

Changes are approved "lazily" when after *reasonable* amount of time
the change receives approval from at least one core developer
and no rejections (excercise of core developer veto right).

.. _gov_bep:

``skbase`` enhancement proposals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Project design decisions have a more detailed approval process,
commensurate with their broader impact on the project. Any changes
to the project's core API design, hard dependencies or supported versions
should first be presented in a ``skbase`` enhancement proposal (BEP).

See the developer guide for more information on creating a :ref:`BEP <bep>`.

Resolving conflicts
^^^^^^^^^^^^^^^^^^^

When consensus can't be found lazily, core developers can call for a vote
on a topic. A topic must receive two-thirds of core developer votes cast
(abstentions are allowed) via comments on the relevant issue or
Pull Request over a 5 day voting period.

In the event a proposed change does not gather the necesssary votes, then:

- The core developer who triggered the vote can choose to drop the issue
- The proposed changes can be escalated to the CC, who will seek to learn more
  about the team member viewpoints, before bringing the topic up for a simple
  majority vote of CC members.

.. _acknowledging:

Acknowledging contributions
===========================

The ``skbase`` project values all kinds of contributions and the
development team is committed to recognising each of them fairly.

The project follows the `all-contributors <https://allcontributors.org>`_
specification to recognise all contributors, including those that don’t
contribute code. Please see our list of `all contributors <contributors.md>`_.

Please let us know or open a PR with the appropriate changes to
`baseobject/.all-contributorsrc
<https://github.com/sktime/baseobject/blob/main/.all-contributorsrc>`_
if we have missed anything.

.. note::

  ``skbase`` is an open-source project. All code is contributed
  under `our open-source
  license <https://github.com/sktime/baseobject/blob/main/LICENSE>`_.
  Contributors acknowledge that they have rights to make their contribution
  (code or otherwise) available under this license.

Outlook
=======

As with other parts of the project, the governance may change as the project
matures. Suggestions on potential governance changes are also welcome.

References
==========

Our governance model is inspired by various existing governance
structures. In particular, we’d like to acknowledge:

* `sktime’s governance model <https://www.sktime.org/en/latest/governance.html>`_
* `scikit-learn’s governance model <https://scikit-learn.org/stable/governance.html>`_
