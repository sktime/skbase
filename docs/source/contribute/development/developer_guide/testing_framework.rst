=================
Testing Framework
=================

.. note::

    This page explains ``baseobject's`` testing framework with an emphasis on how
    the package's developers  are expected to interact with the test suite. If
    you are developer and want to learn how you can use the ``baseobject``
    testing framework to develop your own package, see our
    :ref:`testing user guide <user_guide_testing>`.

``baseobject`` uses ``pytest`` to test the correctness of code.
This page gives an overview of the tests, an introduction on adding new tests,
and how to extend the testing framework.

Test module architecture
========================

``baseobject`` uses a tiered approach to test its functionality:

- *package level* tests in ``tests/test_base.py`` are designed to verify the
  ``BaseObject`` interface

- *module level* tests are focused on verifying the compliance of a concrete

- *low level* tests in the ``tests`` folders in each module are used to verify the
  functionality of individual code artifacts

Module conventions are as follows:

* Each module contains a ``tests`` folder that contains tests specific to that module.
    * Sub-modules may also contain ``tests`` folders.
    * *module* tests focused on testing a specific class interface should contain a file
      ``test_all_[name_of_class].py``
* ``tests`` folders may contain ``_config.py`` files to collect test
  configuration settings for that module
* Generic utilities for tests are located in the module ``utils._testing``.
* Tests for these utilities should be contained in the ``utils._testing.tests`` folder.
* *module* and *low* level tests should not repeat tests performed at a higher level
