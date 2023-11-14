.. _developer_guide_documentation:

=======================
Documentation standards
=======================

Providing instructive documentation is a key part of ``skbase``'s mission.
To meet this, developers are expected to follow the project's documentation standards.

These include:

* Documenting code using NumPy-style docstrings
* Following ``skbase``'s docstring convention for public code artifacts and modules
* Adding new public functionality to the :ref:`api_ref`
  and :ref:`user guide <user_guide>`

More detailed information on ``skbase``'s documentation format is provided below.

Docstring conventions
=====================

``skbase`` uses the numpydoc_ Sphinx extension and follows the
`NumPy docstring format <https://numpydoc.readthedocs.io/en/latest/format.html>`_.

To ensure docstrings meet expectations, ``skbase`` uses a combination of
validations built into numpydoc_, pydocstyle_ pre-commit checks
(set to the NumPy convention) and automated testing of docstring examples to
ensure the code runs without error.

However, the automated docstring validation in pydocstyle_ only covers basic
formatting. Passing these tests is necessary to meet the ``skbase``
docstring conventions, but is not sufficient for doing so.

To ensure docstrings meet ``skbase``'s conventions, developers are expected
to check their docstrings against numpydoc_ and ``skbase`` conventions and
ref:`reviewer's <reviewer_guide_doc>` are expected to also focus feedback on
docstring quality.

``skbase`` specific conventions
-------------------------------

Beyond basic NumPy docstring formatting conventions, developers should focus on:

- Ensuring all parameters (classes, functions, methods) and attributes (classes)
  are documented completely and consistently
- Including links to the relevant topics in the :ref:`glossary` or
  :ref:`user_guide` in the extended summary
- Including an `Examples` section that demonstrates at least basic functionality
  in all public code artifacts
- Adding a `See Also` section that references related ``skbase`` code
  artifacts as applicable
- Including citations to relevant sources in a `References` section

Accordingly, most public code artifacts in ``skbase``
should generally include the following NumPy docstring convention sections:

1. Summary
2. Extended Summary
3. Parameters
4. Attributes (classes only)
5. Returns or Yields (as applicable)
6. Raises (as applicable)
7. See Also (as applicable)
8. Notes (as applicable)
9. References (as applicable)
10. Examples

.. note::

    In many cases a parameter, attribute, return, or error may be described
    in the docstring of more than one class. To avoid confusion, developers
    should make sure their docstrings are as similar as possible to existing
    docstring descriptions of the the same parameter, attribute, return
    or error. As applicable, this may mean copying the same docstring
    section for the parameter, attribute, return or error.

Summary and extended summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The summary should be a single line, followed by a (properly formatted)
extended summary.

The extended summary should include a user friendly explanation
of the code artifacts functionality. The extended summary should also include
links to relevant content in the :ref:`glossary` and :ref:`user guide <user_guide>`.

If a "term" already exists in the glossary and the developer wants to link it
directly they can use:

.. code-block::

    :term:`the glossary term`

In other cases you'll want to use different phrasing but link to an existing
glossary term, and the developer can use:

.. code-block::

    :term:`the link text <the glossary term>`

In the event a term is not already in the glossary, developers should add the term
to the :ref:`glossary` and include a reference (as shown above) to the added term.

Likewise, a developer can link to a particular area of the user guide by including
an explicit cross-reference and following the steps for referencing in Sphinx
(see the helpful description on
`Sphinx cross-references
<https://docs.readthedocs.io/en/stable/guides/cross-referencing-with-sphinx.html>`_
posted by Read the Docs). Again developers are encouraged to add important content
to the user guide and link to it if it does not already exist.

See Also
~~~~~~~~

This section should reference other ``skbase`` code artifacts related to the code
artifact being documented by the docstring. Developers should use judgement in
determining related code artifacts.

Notes
~~~~~

The notes section can include several types of information, including:

- Mathematical details of a code object or other important implementation details
  (using ..math or :math:`` functionality)
- Links to alternative implementations of the code artifact that are external to
  ``skbase``
- A summary of the aspects of an object's state that are updated by state
  changing methods

References
~~~~~~~~~~

Objects that implement functionality covered in a research article, book or
other package, should include an applicable citation.

This should be done by adding references into the references section of the docstring,
and then typically linking to these in other parts of the docstring.

The references you intend to link to within the docstring should follow a very specific
format to ensure they render correctly. See the example below. Note the space between
the ".." and opening bracket, the space after the closing bracket, and how all the
lines after the first line are aligned immediately with the opening bracket.
Additional references should be added in exactly the same way, but the number
enclosed in the bracket should be incremented.

.. code-block:: rst

    .. [1] Some research article, link or other type of citation.
       Long references wrap onto multiple lines, but you need to
       indent them so they start aligned with opening bracket on first line.

To link to the reference labeled as "[1]", you use "[1]\_". This only works within
the same docstring. Sometimes this is not rendered correctly if the "[1]\_" link is
preceded or followed by certain characters. If you run into this issue, try
putting a space before and following the "[1]\_" link.

To list a reference but not link it elsewhere in the docstring, you can leave
out the ".. [1]" directive as shown below.

.. code-block:: rst

    Some research article, link or other type of citation.
    Long references wrap onto multiple lines. If you are
    not linking the reference you can leave off the ".. [1]".

Examples
~~~~~~~~

Most code artifacts in ``skbase`` should include an examples section. At
a minimum this should include a single example that illustrates basic functionality.


The examples should use simple data (e.g. randomly generated data, etc)
generated using a ``skbase`` dependency and wherever possible only depend
on ``skbase`` or its core dependencies. Examples should also be designed to
run quickly where possible. For quick running code artifacts, additional examples
can be included to illustrate the affect of different parameter settings.

Examples of Good ``skbase`` Docstrings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here are a few examples of ``skbase`` code artifacts with good documentation.

Classes
^^^^^^^
BaseObject_

Functions
^^^^^^^^^
all_objects_

get_package_metadata_

.. _numpydoc: https://numpydoc.readthedocs.io/en/latest/index.html
.. _pydocstyle: http://www.pydocstyle.org/en/stable/
.. _BaseObject: https://skbase.readthedocs.io/en/latest/api_reference/auto_generated/skbase.base.BaseObject.html#skbase.base.BaseObject
.. _all_objects: https://skbase.readthedocs.io/en/latest/api_reference/auto_generated/skbase.lookup.all_objects.html#skbase.lookup.all_objects
.. _get_package_metadata: https://skbase.readthedocs.io/en/latest/api_reference/auto_generated/skbase.lookup.get_package_metadata.html#skbase.lookup.get_package_metadata

.. _sphinx: https://www.sphinx-doc.org/
.. _readthedocs: https://readthedocs.org/projects/sktime/

Documentation Build
-------------------

We use `sphinx`_ to build our documentation and `readthedocs`_ to host it.
You can find our latest documentation `here <https://skbase.readthedocs.io/en/latest/index.html>`_.

The source files can be found
in `docs/source/ <https://github.com/sktime/skbase/tree/main/docs/source>`_.
The main configuration file for sphinx is
`conf.py <https://github.com/sktime/skbase/blob/main/docs/source/conf.py>`_
and the main page is
`index.rst <https://github.com/sktime/skbase/blob/main/docs/source/index.rst>`_.
To add new pages, you need to add a new ``.rst`` file and link to it from the
applicable file in the existing documentation.

To build the documentation locally, you need to install a few extra
dependencies listed in
`pyproject.toml <https://github.com/sktime/skbase/blob/main/pyproject.toml>`_.

1. To install extra dependencies from the root directory of your local copy
   of the forked repository, run:

   .. code:: bash

      pip install --editable .[docs]

2. To build the website locally, from the root directory of your local copy, run:

   .. code:: bash

      cd docs
      make html
