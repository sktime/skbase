.. _testing_framework:

=================
Testing Framework
=================

.. note::

    This page explains ``skbase``'s testing framework with an emphasis on how
    the package's developers are expected to interact with the test suite. If
    you are a developer and want to learn how you can use the ``skbase``
    testing framework to develop your own package, see our
    :ref:`testing user guide <user_guide_testing>`.

``skbase`` uses ``pytest`` to verify code is working as expected.
This page gives an overview of the tests, an introduction on adding new tests,
and how to extend the testing framework.

Running tests locally
=====================

Before submitting changes, you should run the test suite locally to make sure
nothing is broken.

Running the full test suite
---------------------------

From the project root, run:

.. code-block:: bash

   pytest skbase

This executes all tests across all modules.

Running a single test file
--------------------------

To run only the tests in a specific file:

.. code-block:: bash

   pytest skbase/tests/test_base.py -v

The ``-v`` flag enables verbose output so you can see which tests passed or
failed.

Running a single test function
------------------------------

To run a single test by name:

.. code-block:: bash

   pytest skbase/tests/test_base.py::test_function_name -v


Test module architecture
========================

``skbase`` uses a tiered approach to test its functionality:

- *Package level* tests in ``skbase/tests/test_base.py`` verify the
  ``BaseObject`` interface and core behaviour shared by all objects.

- *Module level* tests are focused on verifying the compliance of a concrete
  class with the ``BaseObject`` contract. These live alongside the module
  they test in ``test_all_[name_of_class].py`` files.

- *Low level* tests in the ``tests`` folders in each module verify the
  functionality of individual code artifacts (functions and helpers).

Module conventions
------------------

* Each module contains a ``tests`` folder with tests specific to that module.

  * Sub-modules may also contain ``tests`` folders.
  * *Module* tests focused on testing a specific class interface should
    contain a file ``test_all_[name_of_class].py``.

* ``tests`` folders may contain ``_config.py`` files to collect test
  configuration settings for that module.
* *Module* and *low level* tests should not repeat tests performed at a
  higher level.


The ``skbase.testing`` module
=============================

The ``skbase.testing`` module provides three key classes that form the
backbone of the testing framework:

* ``BaseFixtureGenerator`` — generates parameterized test fixtures from
  discovered ``BaseObject`` subclasses.
* ``QuickTester`` — a mixin that adds a ``run_tests`` method for running
  tests on a single object, outside of ``pytest``.
* ``TestAllObjects`` — the concrete test class that combines
  ``BaseFixtureGenerator`` and ``QuickTester`` and contains the standard
  package-level tests.


``BaseFixtureGenerator``
------------------------

``BaseFixtureGenerator`` automatically discovers all ``BaseObject``
subclasses in a given package and generates ``pytest`` fixtures for them.
It plugs into ``pytest``'s ``pytest_generate_tests`` hook to parameterize
tests with ``object_class`` and ``object_instance`` fixtures.

Class variables that can be overridden by descendants:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Description
   * - ``package_name``
     - Package to search for objects (default: ``"skbase.tests.mock_package"``).
   * - ``object_type_filter``
     - Filter objects by type tag; ``None`` means all types.
   * - ``exclude_objects``
     - List of class name strings to skip.
   * - ``excluded_tests``
     - Dict mapping class names to lists of test names to skip.
   * - ``valid_tags``
     - List of valid tag names; ``None`` means all tags are valid.
   * - ``fixture_sequence``
     - Order in which conditional fixtures are generated.


``QuickTester``
---------------

``QuickTester`` is a mixin class that adds the ``run_tests`` method. When
mixed into a test class that also inherits from ``BaseFixtureGenerator``,
it allows you to run the full test suite on a *single* object — useful for
interactive debugging or CI scripts.

Key parameters of ``run_tests``:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Description
   * - ``obj``
     - A ``BaseObject`` subclass or instance to test.
   * - ``raise_exceptions``
     - If ``True``, exceptions are raised immediately.
       If ``False`` (default), they are collected in the results dict.
   * - ``tests_to_run``
     - Subset of test names to run (default: all).
   * - ``tests_to_exclude``
     - Tests to skip.
   * - ``verbose``
     - ``0`` = silent, ``1`` = summary, ``2`` = full output.


``TestAllObjects``
------------------

``TestAllObjects`` inherits from both ``BaseFixtureGenerator`` and
``QuickTester``. It contains the standard package-level tests that every
``BaseObject`` subclass should pass, including:

* ``test_create_test_instance`` — verifies ``create_test_instance`` returns
  a valid instance and that ``__init__`` calls ``super().__init__``.
* ``test_create_test_instances_and_names`` — checks the return signature.
* ``test_object_tags`` — checks tag conventions.
* ``test_inheritance`` — checks the class inherits from ``BaseObject``.
* ``test_get_params`` / ``test_set_params`` — parameter interface checks.
* ``test_clone`` — verifies that ``clone`` produces a correct copy.
* ``test_repr`` / ``test_repr_html`` — checks string representations.


Using the testing framework
============================

Providing test parameters with ``get_test_params``
--------------------------------------------------

Every ``BaseObject`` subclass should override ``get_test_params`` to return
parameter dictionaries used to create test instances. The method should
return a single ``dict`` or a ``list`` of ``dict``.

.. code-block:: python

    from skbase.base import BaseObject

    class MyEstimator(BaseObject):
        def __init__(self, alpha=1.0, method="fast"):
            self.alpha = alpha
            self.method = method
            super().__init__()

        @classmethod
        def get_test_params(cls, parameter_set="default"):
            """Return testing parameter settings for MyEstimator."""
            params1 = {"alpha": 0.5, "method": "fast"}
            params2 = {"alpha": 2.0, "method": "slow"}
            return [params1, params2]

Using ``create_test_instance`` and ``create_test_instances_and_names``
----------------------------------------------------------------------

These class methods build test instances from ``get_test_params``:

.. code-block:: python

    # Create a single test instance (uses the first parameter dict)
    obj = MyEstimator.create_test_instance()
    print(type(obj))  # <class 'MyEstimator'>
    print(obj.get_params())  # {'alpha': 0.5, 'method': 'fast'}

    # Create all test instances with names
    instances, names = MyEstimator.create_test_instances_and_names()
    for inst, name in zip(instances, names):
        print(f"{name}: {inst.get_params()}")
    # MyEstimator-0: {'alpha': 0.5, 'method': 'fast'}
    # MyEstimator-1: {'alpha': 2.0, 'method': 'slow'}


Running tests on a single object with ``QuickTester``
-----------------------------------------------------

You can run the standard test suite on any ``BaseObject`` subclass
interactively:

.. code-block:: python

    from skbase.testing import TestAllObjects

    # Run all standard tests on MyEstimator
    results = TestAllObjects().run_tests(MyEstimator, verbose=True)

    # Run only specific tests
    results = TestAllObjects().run_tests(
        MyEstimator,
        tests_to_run="test_create_test_instance",
    )

    # Raise exceptions immediately for debugging
    results = TestAllObjects().run_tests(
        MyEstimator,
        raise_exceptions=True,
    )

The ``results`` dictionary maps test-fixture identifiers to ``"PASSED"``
or the exception that was raised.


Writing and registering new tests
=================================

Adding a new ``BaseObject`` subclass to the test suite
------------------------------------------------------

To have your new subclass automatically picked up by the testing framework:

1. **Implement ``get_test_params``** on your class (see above).

2. **Ensure the class is importable** from the package specified in
   ``BaseFixtureGenerator.package_name``. The framework uses
   ``skbase.lookup.all_objects`` to discover classes.

3. The existing ``TestAllObjects`` tests will automatically run on your
   new class when you execute ``pytest``.

Adding new test methods
-----------------------

To add a new test that runs on every ``BaseObject``:

1. Create a new method on a class inheriting from
   ``BaseFixtureGenerator`` and ``QuickTester`` (or add it to
   ``TestAllObjects``).

2. Name the method ``test_*`` so ``pytest`` discovers it.

3. Use ``object_class`` and/or ``object_instance`` as parameters — they are
   automatically parameterized by the fixture generator.

.. code-block:: python

    class TestAllObjects(BaseFixtureGenerator, QuickTester):

        def test_my_custom_check(self, object_instance):
            """Check a custom invariant on all BaseObject instances."""
            params = object_instance.get_params()
            assert isinstance(params, dict)

Excluding tests for specific classes
-------------------------------------

If a test should be skipped for a particular class, add an entry to the
``excluded_tests`` dictionary:

.. code-block:: python

    class MyTestSuite(BaseFixtureGenerator, QuickTester):
        excluded_tests = {
            "MySpecialClass": ["test_clone", "test_set_params"],
        }


Testing utilities
=================

``skbase.testing.utils`` contains helper utilities:

* ``_conditional_fixtures.py`` — logic for conditional fixture generation
  used internally by ``BaseFixtureGenerator``.
* ``inspect.py`` — helper to introspect function arguments for fixture
  generation.

These are internal utilities and typically do not need to be used directly.
