# skbase Enhancement Proposal 1

Contributors: @RNKuhns, @fkiraly, @miraep8

## Overview

`skbase` seeks to provide a general framework for creating and working with classes
that follow scikit-learn and sktime style design patterns. To accomplish this
`skbase` will provide tools to make it easier for developers of other packages,
toolboxes or applications to reuse the `skbase` interfaces and design patterns.

Specifically,`skbase` will provide:

- [Base classes](#Base-Class-Interfaces) with `scikit-learn` and `sktime`
  style interfaces
- [Tools for working with base classes](#Tools-For-Working-With-Base-Classes)
    - Object collection (retrieval)
    - Object testing
    - Object comparison and validation
- An [example repository](#Example-Repository) that serves the dual purpose of
  illustrating how developers can use `skbase` in their own projects and
  providing test cases
- A [template repository](#Template-Repository) that developers can clone to
  easiliy set up a a new project using `skbase`'s principles

Although the package will initially inherit some of this functinality from
`scikit-learn` the goal is to make it easy to use the design patterns in a
variety of contexts, not just those that depend on `scikit-learn`. Accordingly,
`skbase` has a goal of providing the proposed functionality with minimal
third-party dependencies. This will eventually include the removal of any
dependency on `scikit-learn`.

The rest of this design document provides an outline of the proposed interfaces.

## Design

`skbase`'s core functionality will be available through submodule's tailored to
a given use case.

- `skbase.base` will include the `BaseObject` class and related base classes.
- `skbase.lookup` will include the tools for retrieving (i.e., collecting,
  looking up) any `BaseObject`'s from a project.
- `skbase.validate` will include tools for validating and comparing `BaseObject`'s
  and/or collections of `BaseObject`'s.
- `skbase.testing` will include tools for testing `BaseObject`s for interface
  compliance.

The proposed [example repository](#Example-Repository) and
[repository template](#Template-Repository) will live in separate repositories.

### skbase.base: Base Class Interfaces

`skbase`'s primary API is provided through classes that allow for
`scikit-learn`'s and `sktime`'s design patterns to be re-used in additional
contexts. This includes:

- [BaseObject](#BaseObject): a base class providing the package's primary
  class level interface. Other classes are subclasses of `BaseObject`.
- [BaseEstimator](#BaseEstimator): A subclass of `BaseObject` that adds a
  high-level interface for *fittable* estimators
- [BaseMetaObject](#BaseMetaObjectMixin): A mixin that provides a high-level interface
  for working with classes composed of collections of `BaseObject`s.
- [Base pipeline classes](#Base-Pipeline-Classes): `BaseObject`s that also
  inherit from `BaseMetaObject` mixin and provide additional generic functionalty
  for common pipeline use cases.

#### BaseObject

BaseObjects are base classes with:

- `scikit-learn` style interface to get and set parameters
- `sktime` style interface for working with *tags*
- `sktime` style interface for cloning and re-instantiation (resetting)
- `sktime` style interface for generating test instances
- `sktime` style interface for retrieving fitted parameters
- `scikit-learn` style interface for representing objects (e.g., pretty printing
  and drawing a simple block representation in HTML)
- Support simple composition where parameter arguments are other `BaseObject`s,
  including the ability to get and set the parameters of component `BaseObject`s
- Interface for instance-level override of configuration context
- Interface for parameter validation.

`BaseObject`s should also follow certain design patterns and coding practices,
including:

- Specify all parameters in the classes ``__init__`` as explicit keyword arguments.
  No ``args`` or ``kwargs`` should be used to set class parameters.
- Keyword arguments should be stored in the class as attributes with the same name.
  These should be documented in the parameters section of the docstring, and not
  documented in the attributes section of the docstring.
- All instance attributes should be created in ``__init__``. If the attribute
  is not assigned a value until later, initialize it as None.
- Attributes that depend on the state of the instance's parameters should end
  in an underscore to easily communicate that they are "state" dependent.
- Start non-public attributes and methods with an underscore
  (per standard Python conventions).
- Document all public attributes that are not parameters in the class docstring's
  attributes section.

#### BaseEstimator

Scikit-learn style [estimators](https://scikit-learn.org/stable/tutorial/statistical_inference/settings.html?highlight=estimator#estimators-objects) are *"objects that learn from data"*.

In `scikit-learn` and `sktime` these can be *regressors*, *classifiers*,
*clusterers*, *annotators*, *forecasters*, *transformers* and other type of
classes implementing learning algorithms.

`BaseEstimator` ties together the different algorithm categories through a
common high-level interface for learning (fitting) parameters from data by inheriting
from `BaseObject` and providing an additional interface for *fittable* learning
algorithms, including:

- An instance `is_fitted` property denoting whether the the estimator has been
  fit (`is_fitted` does this by inspecting a non-public `_is_fitted` attribute
  set in each algorithm's call to its `fit` method).
- An instance `check_is_fitted` method for raising an error when an estimator
  has not been fitted yet.

Although the `BaseEstimator` interface may seem like it should include a `fit`
method for learning the parameters from data, it is not included. Instead
`BaseEstimator` assumes sub-classes implement a `fit` method (and that this
method appropriately sets the `_is_fitted` attribute), since the signature of
`fit` is learning task specific. Therefore, the specific `fit` implementation
is left to child classes implemented outside of `skbase`.

#### BaseMetaObject

The `BaseObject` interface is designed to make it easy for developers to provide
uniform functionality for interacting with parametric objects in their
projects. This makes is particularly helpful in use cases where working with
collections of objects is important. For example, iterativately applying computations
to a dataset is common-place in statistical and data processing applications.

For example, `scikit-learn` and `sktime` include pipeline classes that let
users easily iteratively apply a series of estimators to their data. Meanwhile,
in data engineering pipelines, data may undergo a series of transformations prior
to being used or stored.

`skbase` supports these use cases by providing `BaseMetaObject`to provide a
high-level interface of working with classes composed of collections of
`BaseObject`s or `BaseEstimator`s. `BaseMetaObject` expands on the `BaseObject`
interface by expanding support for composite objects where parameter values include
collections of `BaseObject`s. This includes built-in parameter getting/setting on
nested `BaseObject`s when parameter values are collections of `BaseObjects`, and
functionality for working with the tags of nested objects.

##### Base Pipeline Classes
`skbase` intends to provide additional meta classes that expand on the `BaseMetaObject`
API to include specific functionality for the type of common pipeline use cases
found in `scikit-learn`, `sktime` and data processing workflows. This functionality
will eventually be made available through two base pipeline classes:

- `BasePipeline` expands on the `BaseMetaObject` framework by providing
  common functionality for (linear) step based pipelines like those found
  in `scikit-learn` and `sktime`
- `BaseDAGPipeline` expands on the `BaseMetaObject` framework by providing
  functionality for  pipelines composed of directed-acyclic graphs (DAGs)

Each base pipeline class will focus on providing generic functionality for
implementing the specific pipeline use case, while stopping short of implementing
methods for fitting, transforming or otherwise updating the state of the pipeline.

### Tools For Working With Base Classes

`skbase` should make it easy for developers to work with `BaseObject`s and create
their own packages that follow `skbase`'s principles. To accomplish this
`skbase` includes tools that make it easier to accomplish common workflows
that arise.

#### `skbase.lookup`: Collecting (Retrieving) Information on BaseObjects and Package Metadata

The need to lookup classes arises in several contexts when working working with
parametric objects, including the need to collect *similar* objects for
testing or reporting. For example, the developer of a machine learning package
may want to gather all the objects that subclass the base class for a given
type of learning problem so they can be tested for interface compliance (e.g.,
collect all *regressors* or *forecasters* and then test their interface).

`skbase` provides support for this through two function interfaces:

- `all_objects` provides the ability to recursively walk packages (or sub-packages)
  and return the objects that meet the filters specified in the function call.
- `get_package_metadata` provides the ability to recursively walk a package's modules
  and collect information on the items contained in the modules (including
  objects and functions).

#### `skbase.testing`: Testing BaseObjects

When building packages like `sktime` and `scikit-learn` that are made up of
related objects, there is a need to make all the objects comply with expected
interfaces and required functionality works as expected. `skbase` seeks to
make this easy by providing extensible functionality for automatically
collecting and testing classes that descend from BaseObject.

This benefits users by:

- Making it easy to incorporate these tests in their own projects, reducing the need
  to spend time testing that their classes comply with the interface inheritted
  from `BaseObject`.
- Providing an extensible framework they can use to collect and test their own
  object interfaces and functionality.

#### `skbase.validate`: Validating and Comparing BaseObjects

When developing packages that include parametric objects, verifying and comparing
objects is a common worfklow.

To aid this `skbase` will provide functions to:
- Check if a `BaseObject` complies with the expected interface
- Test if two BaseObjects have same parameters and parameter values
- Check if a sequence is all BaseObjects
- Check if a collection contains named objects in allowable interface formats

### Example Repository
`skbase`will also maintain a simple example package that illustrates how `skbase`'s
functionality can be used to create another package. This will help illustrate
how developers can use the package and also provide `skbase` another
method of testing the functionality provided by `skbase.testing`.

### Template Repository
To make it easy for others to use `skbase` in new projects, it is useful to provide
a template repository that provides a starting point. `skbase` tends to make this
available, potentially by creating and maintaining a
[cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html#features)
template. Users, can then use the `cookiecutter` package's functionality to
setup their own project.
