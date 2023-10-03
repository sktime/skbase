.. _getting_started:

===========
Get Started
===========

The following information is designed to get users up and running with
``skbase`` quickly. For more detailed information, see the links in each
of the subsections.

Installation
============

``skbase`` currently supports:

* environments with python version 3.8, 3.9, 3.10 or 3.11
* operating systems Mac OS X, Unix-like OS, Windows 8.1 and higher
* installation via ``PyPi``

Users can choose whether to install the ``skbase`` with its standard dependencies or
alternatively to install ``skbase`` with all its dependencies using the
code snippets below.

.. tab-set::

    .. tab-item:: PyPi

        .. code-block:: bash

           pip install scikit-base

    .. tab-item:: PyPi (all dependencies)

        .. code-block:: bash

           pip install scikit-base[all_extras]

    .. tab-item:: Conda

        .. note::

            We are still working on creating releases of ``skbase`` on ``conda``.
            If you would like to help, please open a pull request.

    .. tab-item:: Conda (all dependencies)

        .. note::

            We are still working on creating releases of ``skbase`` on ``conda``.
            If you would like to help, please open a pull request.

For additional details see our :ref:`full installation guide <full_install>`.


Key Concepts
============

``skbase`` seeks to provide a general :term:`framework`  for creating and
working with classes that follow `scikit-learn`_, and `sktime`_ style design patterns.

Primary functionality is provided through base classes that provide interfaces for:

 - `scikit-learn`_ style parameter getting and setting
 - using :term:`tags <tag>` to record characteristics of the class that can
   be used to alter the classes code or how it interacts with other functionality
 - generating test instances

To make it easy to build :term:`toolboxes <toolbox>` and
:term:`applications <application>` that use ``skbase``'s, interfaces
are also provided for:

- retrieving information on ``BaseObject``-s
- automating the testing of ``BaseObject``-s
- validating ``BaseObject``-s or collections of ``BaseObjects``-s

.. warning::

    The ``skbase`` package is new and its interfaces are still experimental. The
    package's API may change as each functional area reaches maturity.

Quickstart
==========
The code snippets below are designed to introduce ``skbase``'s
functionality. For more detailed information see the :ref:`tutorials`,
:ref:`user_guide` and :ref:`api_ref` in ``skbase``'s
:ref:`user_documentation`.

.. _scikit-learn: https://scikit-learn.org/stable/index.html
.. _sktime: https://www.sktime.net/en/stable/index.html
