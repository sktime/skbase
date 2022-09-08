.. _api_ref:

=============
API Reference
=============

Welcome to the API reference for ``skbase``.

The API reference provides a technical manual, describing the class and
function interface provided by the package. See the :ref:`user_guide` for
additional details.

.. automodule:: baseobject
    :no-members:
    :no-inherited-members:

.. _base_ref:

Base Classes
============

.. currentmodule:: baseobject

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: class.rst

    BaseObject
    BaseEstimator

.. _obj_retrieval:

Object Retrieval
================

.. currentmodule:: baseobject

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: function.rst

    all_objects
    get_package_metadata

.. _obj_testing:

Testing
=======

.. automodule:: baseobject.testing
    :no-members:
    :no-inherited-members:

.. currentmodule:: baseobject.testing

.. autosummary::
    :toctree: api_reference/auto_generated/
    :template: class.rst

    BaseFixtureGenerator
    QuickTester
    TestAllObjects
