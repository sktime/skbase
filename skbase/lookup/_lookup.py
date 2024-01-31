#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
"""Tools to lookup information on code artifacts in a Python package or module.

This module exports the following methods for registry lookup:

package_metadata()
    Walk package and return metadata on included classes and functions by module.
all_objects(object_types, filter_tags)
    Look (and optionally filter) BaseObject descendants in a package or module.
"""
# all_objects is based on the sktime all_estimator retrieval utility, which
# is based on the sklearn estimator retrieval utility of the same name
# See https://github.com/scikit-learn/scikit-learn/blob/main/COPYING and
# https://github.com/sktime/sktime/blob/main/LICENSE
import importlib
import inspect
import io
import os
import pathlib
import pkgutil
import sys
import warnings
from collections.abc import Iterable
from copy import deepcopy
from operator import itemgetter
from types import ModuleType
from typing import Any, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union

from skbase.base import BaseObject
from skbase.validate import check_sequence

__all__: List[str] = ["all_objects", "get_package_metadata"]
__author__: List[str] = [
    "fkiraly",
    "mloning",
    "katiebuc",
    "miraep8",
    "xloem",
    "rnkuhns",
]

# the below is commented out to avoid a dependency on typing_extensions
# but still left in place as it is informative regarding expected return type

# class ClassInfo(TypedDict):
#     """Type definitions for information on a module's classes."""

#     klass: Type
#     name: str
#     description: str
#     tags: MutableMapping[str, Any]
#     is_concrete_implementation: bool
#     is_base_class: bool
#     is_base_object: bool
#     authors: Optional[Union[List[str], str]]
#     module_name: str


# class FunctionInfo(TypedDict):
#     """Information on a module's functions."""

#     func: FunctionType
#     name: str
#     description: str
#     module_name: str


# class ModuleInfo(TypedDict):
#     """Module information type definitions."""

#     path: str
#     name: str
#     classes: MutableMapping[str, ClassInfo]
#     functions: MutableMapping[str, FunctionInfo]
#     __all__: List[str]
#     authors: str
#     is_package: bool
#     contains_concrete_class_implementations: bool
#     contains_base_classes: bool
#     contains_base_objects: bool


def _is_non_public_module(module_name: str) -> bool:
    """Determine if a module is non-public or not.

    Parameters
    ----------
    module_name : str
        Name of the module.

    Returns
    -------
    is_non_public : bool
        Whether the module is non-public or not.
    """
    if not isinstance(module_name, str):
        raise ValueError(
            f"Parameter `module_name` should be str, but found {type(module_name)}."
        )
    is_non_public: bool = "._" in module_name or module_name.startswith("_")
    return is_non_public


def _is_ignored_module(
    module_name: str, modules_to_ignore: Union[str, List[str], Tuple[str]] = None
) -> bool:
    """Determine if module is one of the ignored modules.

    Ignores a module if identical with, or submodule of a module whose name
    is in the list/tuple `modules_to_ignore`.

    E.g., if `modules_to_ignore` contains the string `"foo"`, then `True` will be
    returned for `module_name`-s `"bar.foo"`, `"foo"`, `"foo.bar"`,
    `"bar.foo.bar"`, etc.

    Parameters
    ----------
    module_name : str
        Name of the module.
    modules_to_ignore : str, list[str] or tuple[str]
        The modules that should be ignored when walking the package.

    Returns
    -------
    is_ignored : bool
        Whether the module is an ignrored module or not.
    """
    if isinstance(modules_to_ignore, str):
        modules_to_ignore = (modules_to_ignore,)
    is_ignored: bool
    if modules_to_ignore is None:
        is_ignored = False
    else:
        is_ignored = any(part in modules_to_ignore for part in module_name.split("."))

    return is_ignored


def _filter_by_class(
    klass: type, class_filter: Optional[Union[type, Sequence[type]]] = None
) -> bool:
    """Determine if a class is a subclass of the supplied classes.

    Parameters
    ----------
    klass : object
        Class to check.
    class_filter : objects or iterable of objects
        Classes that `klass` is checked against.

    Returns
    -------
    is_subclass : bool
        Whether the input class is a subclass of the `class_filter`.
        If `class_filter` was `None`, returns `True`.
    """
    if class_filter is None:
        return True

    if isinstance(class_filter, Iterable) and not isinstance(class_filter, tuple):
        class_filter = tuple(class_filter)
    return issubclass(klass, class_filter)


def _filter_by_tags(obj, tag_filter=None, as_dataframe=True):
    """Check whether estimator satisfies tag_filter condition.

    Parameters
    ----------
    obj : BaseObject, an sktime estimator
    tag_filter : dict of (str or list of str), default=None
        subsets the returned estimators as follows:
        each key/value pair is statement in "and"/conjunction

        * key is tag name to sub-set on
        * value str or list of string are tag values
        * condition is "tag value at key must be equal to search value",
          if search value, tag value are not iterable.
          if one of search value, tag value, or both, are lists: condition is
          "at least one element of search value must be contained in tag value"

    Returns
    -------
    cond_sat: bool, whether estimator satisfies condition in `tag_filter`
        if `tag_filter` was None, returns `True`
    """
    if tag_filter is None:
        return True

    if not isinstance(tag_filter, (str, Iterable, dict)):
        raise TypeError(
            "tag_filter argument of _filter_by_tags must be "
            "a dict with str keys, str, or iterable of str, "
            f"but found tag_filter of type {type(tag_filter)}"
        )

    if not hasattr(obj, "get_class_tag"):
        return False

    klass_tags = obj.get_class_tags().keys()

    # case: tag_filter is string
    if isinstance(tag_filter, str):
        return tag_filter in klass_tags

    # case: tag_filter is iterable of str but not dict
    # If a iterable of strings is provided, check that all are in the returned tag_dict
    if isinstance(tag_filter, Iterable) and not isinstance(tag_filter, dict):
        if not all(isinstance(t, str) for t in tag_filter):
            raise ValueError(
                "tag_filter argument of _filter_by_tags must be "
                f"a dict with str keys, str, or iterable of str, but found {tag_filter}"
            )
        return all(tag in klass_tags for tag in tag_filter)

    # case: tag_filter is dict
    if not all(isinstance(t, str) for t in tag_filter.keys()):
        raise ValueError(
            "tag_filter argument of _filter_by_tags must be "
            f"a dict with str keys, str, or iterable of str, but found {tag_filter}"
        )

    cond_sat = True

    for key, search_value in tag_filter.items():
        if not isinstance(search_value, list):
            search_value = [search_value]
        tag_value = obj.get_class_tag(key)
        if not isinstance(tag_value, list):
            tag_value = [tag_value]
        cond_sat = cond_sat and len(set(search_value).intersection(tag_value)) > 0

    return cond_sat


def _walk(root, exclude=None, prefix=""):
    """Recursively return all modules and sub-modules as list of strings.

    Unlike pkgutil.walk_packages, does not import modules on exclusion list.

    Parameters
    ----------
    root : str or path-like
        Root path in which to look for submodules. Can be a string path,
        pathlib.Path or other path-like object.
    exclude : tuple of str or None, optional, default = None
        List of sub-modules to ignore in the return, including sub-modules
    prefix: str, optional, default = ""
        This str is pre-appended to all strings in the return

    Yields
    ------
    str : sub-module strings
        Iterates over all sub-modules of root that do not contain any of the
        strings on the `exclude` list string is prefixed by the string `prefix`
    """
    if not isinstance(root, str):
        root = str(root)
    for loader, module_name, is_pkg in pkgutil.iter_modules(path=[root]):
        if not _is_ignored_module(module_name, modules_to_ignore=exclude):
            yield f"{prefix}{module_name}", is_pkg, loader
            if is_pkg:
                yield from (
                    (f"{prefix}{module_name}.{x[0]}", x[1], x[2])
                    for x in _walk(f"{root}/{module_name}", exclude=exclude)
                )


def _import_module(
    module: Union[str, importlib.machinery.SourceFileLoader],
    suppress_import_stdout: bool = True,
) -> ModuleType:
    """Import a module, while optionally suppressing import standard out.

    Parameters
    ----------
    module : str or importlib.machinery.SourceFileLoader
        Name of the module to be imported or a SourceFileLoader to load a module.
    suppress_import_stdout : bool, default=True
        Whether to suppress stdout printout upon import.

    Returns
    -------
    imported_mod : ModuleType
        The module that was imported.
    """
    # input check
    if not isinstance(module, (str, importlib.machinery.SourceFileLoader)):
        raise ValueError(
            "`module` should be string module name or instance of "
            "importlib.machinery.SourceFileLoader."
        )

    # if suppress_import_stdout:
    # setup text trap, import
    if suppress_import_stdout:
        temp_stdout = sys.stdout
        sys.stdout = io.StringIO()

    try:
        if isinstance(module, str):
            imported_mod = importlib.import_module(module)
        elif isinstance(module, importlib.machinery.SourceFileLoader):
            spec = importlib.util.spec_from_file_location(module.name, module.path)
            imported_mod = importlib.util.module_from_spec(spec)

            loader = spec.loader
            loader.exec_module(imported_mod)
        exc = None
    except Exception as e:
        # we store the exception so we can restore the stdout first
        exc = e

    # if we set up a text trap, restore it to the initial value
    if suppress_import_stdout:
        sys.stdout = temp_stdout

    # if we encountered an exception, now raise it
    if exc is not None:
        raise exc

    return imported_mod


def _determine_module_path(
    package_name: str, path: Optional[Union[str, pathlib.Path]] = None
) -> Tuple[ModuleType, str, importlib.machinery.SourceFileLoader]:
    """Determine a package's path information.

    Parameters
    ----------
    package_name : str
        The name of the package/module to return metadata for.

        - If `path` is not None, this should be the name of the package/module
          associated with the path. `package_name` (with "." appended at end)
          will be used as prefix for any submodules/packages when walking
          the provided `path`.
        - If `path` is None, then package_name is assumed to be an importable
          package or module and the `path` to `package_name` will be determined
          from its import.

    path : str or absolute pathlib.Path, default=None
        If provided, this should be the path that should be used as root
        to find any modules or submodules.

    Returns
    -------
    module, path_, loader : ModuleType, str, importlib.machinery.SourceFileLoader
        Returns the module, a string of its path and its SourceFileLoader.
    """
    if not isinstance(package_name, str):
        raise ValueError(
            "`package_name` must be the string name of a package or module."
            "For example, 'some_package' or 'some_package.some_module'."
        )

    def _instantiate_loader(package_name: str, path: str):
        if path.endswith(".py"):
            loader = importlib.machinery.SourceFileLoader(package_name, path)
        elif os.path.exists(path + "/__init__.py"):
            loader = importlib.machinery.SourceFileLoader(
                package_name, path + "/__init__.py"
            )
        else:
            loader = importlib.machinery.SourceFileLoader(package_name, path)
        return loader

    if path is None:
        module = _import_module(package_name, suppress_import_stdout=False)
        if hasattr(module, "__path__") and (
            module.__path__ is not None and len(module.__path__) > 0
        ):
            path_ = module.__path__[0]
        elif hasattr(module, "__file__") and module.__file__ is not None:
            path_ = module.__file__.split(".")[0]
        else:
            raise ValueError(
                f"Unable to determine path for provided `package_name`: {package_name} "
                "from the imported module. Try explicitly providing the `path`."
            )
        loader = _instantiate_loader(package_name, path_)
    else:
        # Make sure path is str and not a pathlib.Path
        if isinstance(path, (pathlib.Path, str)):
            path_ = str(path.absolute()) if isinstance(path, pathlib.Path) else path
            # Use the provided path and package name to load the module
            # if both available.
            try:
                loader = _instantiate_loader(package_name, path_)
                module = _import_module(loader, suppress_import_stdout=False)
            except ImportError as exc:
                raise ValueError(
                    f"Unable to import a package named {package_name} based "
                    f"on provided `path`: {path_}."
                ) from exc
        else:
            raise ValueError(
                f"`path` must be a str path or pathlib.Path, but is type {type(path)}."
            )

    return module, path_, loader


def _get_module_info(
    module: ModuleType,
    is_pkg: bool,
    path: str,
    package_base_classes: Union[type, Tuple[type, ...]],
    exclude_non_public_items: bool = True,
    class_filter: Optional[Union[type, Sequence[type]]] = None,
    tag_filter: Optional[Union[str, Sequence[str], Mapping[str, Any]]] = None,
    classes_to_exclude: Optional[Union[type, Sequence[type]]] = None,
) -> dict:  # of ModuleInfo type
    # Make package_base_classes a tuple if it was supplied as a class
    base_classes_none = False
    if isinstance(package_base_classes, Iterable):
        package_base_classes = tuple(package_base_classes)
    elif not isinstance(package_base_classes, tuple):
        if package_base_classes is None:
            base_classes_none = True
        package_base_classes = (package_base_classes,)

    exclude_classes: Optional[Sequence[type]]
    if classes_to_exclude is None:
        exclude_classes = classes_to_exclude
    elif isinstance(classes_to_exclude, Sequence):
        exclude_classes = classes_to_exclude
    elif inspect.isclass(classes_to_exclude):
        exclude_classes = (classes_to_exclude,)

    designed_imports: List[str] = getattr(module, "__all__", [])
    authors: Union[str, List[str]] = getattr(module, "__author__", [])
    if isinstance(authors, (list, tuple)):
        authors = ", ".join(authors)
    # Compile information on classes in the module
    module_classes: MutableMapping = {}  # of ClassInfo type
    for name, klass in inspect.getmembers(module, inspect.isclass):
        # Skip a class if non-public items should be excluded and it starts with "_"
        if (
            (exclude_non_public_items and klass.__name__.startswith("_"))
            or (exclude_classes is not None and klass in exclude_classes)
            or not _filter_by_tags(klass, tag_filter=tag_filter)
            or not _filter_by_class(klass, class_filter=class_filter)
        ):
            continue
        # Otherwise, store info about the class
        if klass.__module__ == module.__name__ or name in designed_imports:
            klass_authors = getattr(klass, "__author__", authors)
            if isinstance(klass_authors, (list, tuple)):
                klass_authors = ", ".join(klass_authors)
            if base_classes_none:
                concrete_implementation = False
            else:
                concrete_implementation = (
                    issubclass(klass, package_base_classes)
                    and klass not in package_base_classes
                )
            module_classes[name] = {
                "klass": klass,
                "name": klass.__name__,
                "description": (
                    "" if klass.__doc__ is None else klass.__doc__.split("\n")[0]
                ),
                "tags": (
                    klass.get_class_tags() if hasattr(klass, "get_class_tags") else None
                ),
                "is_concrete_implementation": concrete_implementation,
                "is_base_class": klass in package_base_classes,
                "is_base_object": issubclass(klass, BaseObject),
                "authors": klass_authors,
                "module_name": module.__name__,
            }

    module_functions: MutableMapping = {}  # of FunctionInfo type
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if func.__module__ == module.__name__ or name in designed_imports:
            # Skip a class if non-public items should be excluded and it starts with "_"
            if exclude_non_public_items and func.__name__.startswith("_"):
                continue
            # Otherwise, store info about the class
            module_functions[name] = {
                "func": func,
                "name": func.__name__,
                "description": (
                    "" if func.__doc__ is None else func.__doc__.split("\n")[0]
                ),
                "module_name": module.__name__,
            }

    # Combine all the information on the module together
    module_info = {  # of ModuleInfo type
        "path": path,
        "name": module.__name__,
        "classes": module_classes,
        "functions": module_functions,
        "__all__": designed_imports,
        "authors": authors,
        "is_package": is_pkg,
        "contains_concrete_class_implementations": any(
            v["is_concrete_implementation"] for v in module_classes.values()
        ),
        "contains_base_classes": any(
            v["is_base_class"] for v in module_classes.values()
        ),
        "contains_base_objects": any(
            v["is_base_object"] for v in module_classes.values()
        ),
    }
    return module_info


def get_package_metadata(
    package_name: str,
    path: Optional[str] = None,
    recursive: bool = True,
    exclude_non_public_items: bool = True,
    exclude_non_public_modules: bool = True,
    modules_to_ignore: Union[str, List[str], Tuple[str]] = ("tests",),
    package_base_classes: Union[type, Tuple[type, ...]] = (BaseObject,),
    class_filter: Optional[Union[type, Sequence[type]]] = None,
    tag_filter: Optional[Union[str, Sequence[str], Mapping[str, Any]]] = None,
    classes_to_exclude: Optional[Union[type, Sequence[type]]] = None,
    suppress_import_stdout: bool = True,
) -> Mapping:  # of ModuleInfo type
    """Return a dictionary mapping all package modules to their metadata.

    Parameters
    ----------
    package_name : str
        The name of the package/module to return metadata for.

        - If `path` is not None, this should be the name of the package/module
          associated with the path. `package_name` (with "." appended at end)
          will be used as prefix for any submodules/packages when walking
          the provided `path`.
        - If `path` is None, then package_name is assumed to be an importable
          package or module and the `path` to `package_name` will be determined
          from its import.

    path : str, default=None
        If provided, this should be the path that should be used as root
        to find any modules or submodules.
    recursive : bool, default=True
        Whether to recursively walk through submodules.

        - If True, then submodules of submodules and so on are found.
        - If False, then only first-level submodules of `package` are found.

    exclude_non_public_items : bool, default=True
        Whether to exclude nonpublic functions and classes (where name starts
        with a leading underscore).
    exclude_non_public_modules : bool, default=True
        Whether to exclude nonpublic modules (modules where names start with
        a leading underscore).
    modules_to_ignore : str, tuple[str] or list[str], default="tests"
        The modules that should be ignored when searching across the modules to
        gather objects. If passed, `all_objects` ignores modules or submodules
        of a module whose name is in the provided string(s). E.g., if
        `modules_to_ignore` contains the string `"foo"`, then `"bar.foo"`,
        `"foo"`, `"foo.bar"`, `"bar.foo.bar"` are ignored.
    package_base_classes: type or Sequence[type], default = (BaseObject,)
        The base classes used to determine if any classes found in metadata descend
        from a base class.
    class_filter : object or Sequence[object], default=None
        Classes that `klass` is checked against. Only classes that are subclasses
        of the supplied `class_filter` are returned in metadata.
    tag_filter : str, Sequence[str] or dict[str, Any], default=None
        Filter used to determine if `klass` has tag or expected tag values.

        - If a str or list of strings is provided, the return will be filtered
          to keep classes that have all the tag(s) specified by the strings.
        - If a dict is provided, the return will be filtered to keep classes
          that have all dict keys as tags. Tag values are also checked such that:

          - If a dict key maps to a single value only classes with tag values equal
            to the value are returned.
          - If a dict key maps to multiple values (e.g., list) only classes with
            tag values in these values are returned.

    classes_to_exclude: objects or iterable of object, default=None
        Classes to exclude from returned metadata.

    Other Parameters
    ----------------
    suppress_import_stdout : bool, default=True
        Whether to suppress stdout printout upon import.

    Returns
    -------
    module_info: dict
        Mapping of string module name (key) to a dictionary of the
        module's metadata. The metadata dictionary includes the
        following key:value pairs:

        - "path": str path to the submodule.
        - "name": str name of the submodule.
        - "classes": dictionary with submodule's class names (keys) mapped to
          dictionaries with metadata about the class.
        - "functions": dictionary with function names (keys) mapped to
          dictionary with metadata about each function.
        - "__all__": list of string code artifact names that appear in the
          submodules __all__ attribute
        - "authors": contents of the submodules __authors__ attribute
        - "is_package": whether the submodule is a Python package
        - "contains_concrete_class_implementations": whether any module classes
          inherit from ``BaseObject`` and are not `package_base_classes`.
        - "contains_base_classes": whether any module classes that are
          `package_base_classes`.
        - "contains_base_objects": whether any module classes that
          inherit from ``BaseObject``.
    """
    module, path, loader = _determine_module_path(package_name, path)
    module_info: MutableMapping = {}  # of ModuleInfo type
    # Get any metadata at the top-level of the provided package
    # This is because the pkgutil.walk_packages doesn't include __init__
    # file when walking a package
    if not _is_ignored_module(package_name, modules_to_ignore=modules_to_ignore):
        module_info[package_name] = _get_module_info(
            module,
            loader.is_package(package_name),
            path,
            package_base_classes,
            exclude_non_public_items=exclude_non_public_items,
            class_filter=class_filter,
            tag_filter=tag_filter,
            classes_to_exclude=classes_to_exclude,
        )

    # Now walk through any submodules
    prefix = f"{package_name}."
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        warnings.simplefilter("module", category=ImportWarning)
        warnings.filterwarnings(
            "ignore", category=UserWarning, message=".*has been moved to.*"
        )
        for name, is_pkg, _ in _walk(path, exclude=modules_to_ignore, prefix=prefix):
            # Used to skip-over ignored modules and non-public modules
            if exclude_non_public_modules and _is_non_public_module(name):
                continue

            try:
                sub_module: ModuleType = _import_module(
                    name, suppress_import_stdout=suppress_import_stdout
                )
                module_info[name] = _get_module_info(
                    sub_module,
                    is_pkg,
                    path,
                    package_base_classes,
                    exclude_non_public_items=exclude_non_public_items,
                    class_filter=class_filter,
                    tag_filter=tag_filter,
                    classes_to_exclude=classes_to_exclude,
                )
            except ImportError:
                continue

            if recursive and is_pkg:
                if "." in name:
                    name_ending = name[len(package_name) + 1 :]
                else:
                    name_ending = name

                updated_path: str
                if "." in name_ending:
                    updated_path = "/".join([path, name_ending.replace(".", "/")])
                else:
                    updated_path = "/".join([path, name_ending])
                module_info.update(
                    get_package_metadata(
                        package_name=name,
                        path=updated_path,
                        recursive=recursive,
                        exclude_non_public_items=exclude_non_public_items,
                        exclude_non_public_modules=exclude_non_public_modules,
                        modules_to_ignore=modules_to_ignore,
                        package_base_classes=package_base_classes,
                        class_filter=class_filter,
                        tag_filter=tag_filter,
                        classes_to_exclude=classes_to_exclude,
                        suppress_import_stdout=suppress_import_stdout,
                    )
                )

    return module_info


def all_objects(
    object_types=None,
    filter_tags=None,
    exclude_objects=None,
    exclude_estimators=None,
    return_names=True,
    as_dataframe=False,
    return_tags=None,
    suppress_import_stdout=True,
    package_name="skbase",
    path: Optional[str] = None,
    modules_to_ignore=None,
    ignore_modules=None,
    class_lookup=None,
):
    """Get a list of all objects in a package with name `package_name`.

    This function crawls the package/module to retrieve all classes
    that are descendents of BaseObject. By default it does this for the `skbase`
    package, but users can specify `package_name` or `path` to another project
    and `all_objects` will crawl and retrieve BaseObjects found in that project.

    Parameters
    ----------
    object_types: class or list of classes, default=None

        - If class_lookup is provided, can also be str or list of str
          which kind of objects should be returned.
        - If None, no filter is applied and all estimators are returned.
        - If class or list of class, estimators are filtered to inherit from
          one of these.
        - If str or list of str, classes can be aliased by strings, as long
          as `class_lookup` parameter is passed a lookup dict.

    return_names: bool, default=True

        - If True, estimator class name is included in the all_estimators()
          return in the order: name, estimator class, optional tags, either as
          a tuple or as pandas.DataFrame columns.
        - If False, estimator class name is removed from the all_estimators()
          return.

    filter_tags: str, list[str] or dict[str, Any], default=None
        Filter used to determine if `klass` has tag or expected tag values.

        - If a str or list of strings is provided, the return will be filtered
          to keep classes that have all the tag(s) specified by the strings.
        - If a dict is provided, the return will be filtered to keep classes
          that have all dict keys as tags. Tag values are also checked such that:

          - If a dict key maps to a single value only classes with tag values equal
            to the value are returned.
          - If a dict key maps to multiple values (e.g., list) only classes with
            tag values in these values are returned.
          - If tag values are iterable,
            condition is "at least one search value is contained in tag values".

    exclude_objects: str or list[str], default=None
        Names of estimators to exclude.
    as_dataframe: bool, default=False

        - If False, `all_objects` will return a list (either a list of
          `skbase` objects or a list of tuples, see Returns).
        - If True, `all_objects` will return a `pandas.DataFrame` with named
            columns for all of the attributes being returned.
            this requires soft dependency `pandas` to be installed.

    return_tags: str or list of str, default=None
        Names of tags to fetch and return each object's value of. The tag values
        named in return_tags will be fetched for each object and will be appended
        as either columns or tuple entries.
    package_name : str, default="skbase".
        Should be set to default to package or module name that objects will
        be retrieved from. Objects will be searched inside `package_name`,
        including in sub-modules (e.g., in package_name, package_name.module1,
        package.module2, and package.module1.module3).
    path : str, default=None
        If provided, this should be the path that should be used as root
        to find `package_name` and start the search for any submodules/packages.
        This can be left at the default value (None) if searching in an installed
        package.
    modules_to_ignore : str or list[str], default=None
        The modules that should be ignored when searching across the modules to
        gather objects. If passed, `all_objects` ignores modules or submodules
        of a module whose name is in the provided string(s). E.g., if
        `modules_to_ignore` contains the string `"foo"`, then `"bar.foo"`,
        `"foo"`, `"foo.bar"`, `"bar.foo.bar"` are ignored.

    class_lookup : dict[str, class], default=None
        Dictionary of string aliases for classes used in object_types. If provided,
        `object_types` can accept str values or a list of string values.

    Other Parameters
    ----------------
    suppress_import_stdout : bool, default=True
        Whether to suppress stdout printout upon import.

    Returns
    -------
    all_estimators will return one of the following:

    - a pandas.DataFrame if `as_dataframe=True`, with columns:

      - "names" with the returned class names if `return_name=True`
      - "objects" with returned classes.
      - optional columns named based on tags passed in `return_tags`
        if `return_tags is not None`.

    - a list if `as_dataframe=False`, where list elements are:

      - classes (that inherit from BaseObject) in alphabetic order by class name
        if `return_names=False` and `return_tags=None.
      - (name, class) tuples in alphabetic order by name if `return_names=True`
        and `return_tags=None`.
      - (name, class, tag-value1, ..., tag-valueN) tuples in alphabetic order by name
        if `return_names=True` and `return_tags is not None`.
      - (class, tag-value1, ..., tag-valueN) tuples in alphabetic order by
        class name if `return_names=False` and `return_tags is not None`.

    References
    ----------
    Modified version of scikit-learn's and sktime's `all_estimators()` to allow
    users to find BaseObjects in `skbase` and other packages.
    """
    module, root, _ = _determine_module_path(package_name, path)
    if modules_to_ignore is None:
        modules_to_ignore = []
    if exclude_objects is None:
        exclude_objects = []

    all_estimators = []

    def _is_base_class(name):
        return name.startswith("_") or name.startswith("Base")

    def _is_estimator(name, klass):
        # Check if klass is subclass of base estimators, not an base class itself and
        # not an abstract class
        return issubclass(klass, BaseObject) and not _is_base_class(name)

    # Ignore deprecation warnings triggered at import time and from walking packages
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        warnings.simplefilter("module", category=ImportWarning)
        warnings.filterwarnings(
            "ignore", category=UserWarning, message=".*has been moved to.*"
        )
        prefix = f"{package_name}."
        for module_name, _, _ in _walk(
            root=root, exclude=modules_to_ignore, prefix=prefix
        ):
            # Filter modules
            if _is_non_public_module(module_name):
                continue

            try:
                if suppress_import_stdout:
                    # setup text trap, import, then restore
                    sys.stdout = io.StringIO()
                    module = importlib.import_module(module_name)
                    sys.stdout = sys.__stdout__
                else:
                    module = importlib.import_module(module_name)
                classes = inspect.getmembers(module, inspect.isclass)
                # Filter classes
                estimators = [
                    (klass.__name__, klass)
                    for _, klass in classes
                    if _is_estimator(klass.__name__, klass)
                ]
                all_estimators.extend(estimators)
            except ModuleNotFoundError as e:
                # Skip missing soft dependencies
                if "soft dependency" not in str(e):
                    raise e
                warnings.warn(str(e), ImportWarning, stacklevel=2)

    # Drop duplicates
    all_estimators = set(all_estimators)

    # Filter based on given estimator types
    if object_types:
        obj_types = _check_object_types(object_types, class_lookup)
        all_estimators = [
            (n, est) for (n, est) in all_estimators if _filter_by_class(est, obj_types)
        ]

    # Filter based on given exclude list
    if exclude_objects:
        exclude_objects = check_sequence(
            exclude_objects,
            sequence_type=list,
            element_type=str,
            coerce_scalar_input=True,
            sequence_name="exclude_object",
        )
        all_estimators = [
            (name, estimator)
            for name, estimator in all_estimators
            if name not in exclude_objects
        ]

    # Drop duplicates, sort for reproducibility
    # itemgetter is used to ensure the sort does not extend to the 2nd item of
    # the tuple
    all_estimators = sorted(all_estimators, key=itemgetter(0))

    if filter_tags:
        all_estimators = [
            (n, est) for (n, est) in all_estimators if _filter_by_tags(est, filter_tags)
        ]

    # remove names if return_names=False
    if not return_names:
        all_estimators = [estimator for (name, estimator) in all_estimators]
        columns = ["object"]
    else:
        columns = ["name", "object"]

    # add new tuple entries to all_estimators for each tag in return_tags:
    return_tags = [] if return_tags is None else return_tags
    if return_tags:
        return_tags = check_sequence(
            return_tags,
            sequence_type=list,
            element_type=str,
            coerce_scalar_input=True,
            sequence_name="return_tags",
        )
        # enrich all_estimators by adding the values for all return_tags tags:
        if all_estimators:
            if isinstance(all_estimators[0], tuple):
                all_estimators = [
                    (name, est) + _get_return_tags(est, return_tags)
                    for (name, est) in all_estimators
                ]
            else:
                all_estimators = [
                    (est,) + _get_return_tags(est, return_tags)
                    for est in all_estimators
                ]
        columns = columns + return_tags

    # convert to pandas.DataFrame if as_dataframe=True
    if as_dataframe:
        all_estimators = _make_dataframe(all_estimators, columns=columns)

    return all_estimators


def _get_return_tags(obj, return_tags):
    """Fetch a list of all tags for every_entry of all_estimators.

    Parameters
    ----------
    obj:  BaseObject
        A BaseObject.
    return_tags: list of str
        Names of tags to get values for the estimator.

    Returns
    -------
    tags: a tuple with all the object values for all tags in return tags.
        a value is None if it is not a valid tag for the object provided.
    """
    tags = tuple(obj.get_class_tag(tag) for tag in return_tags)
    return tags


def _check_object_types(object_types, class_lookup=None):
    """Return list of classes corresponding to type strings.

    Parameters
    ----------
    object_types : str, class, or list of string or class
    class_lookup : dict[string, class], default=None

    Returns
    -------
    list of class, i-th element is:
        class_lookup[object_types[i]] if object_types[i] was a string
        object_types[i] otherwise
    if class_lookup is none, only checks whether object_types is class or list of.

    Raises
    ------
    ValueError if object_types is not of the expected type.
    """
    object_types = deepcopy(object_types)

    if not isinstance(object_types, list):
        object_types = [object_types]  # make iterable

    def _get_err_msg(estimator_type):
        if class_lookup is None or not isinstance(class_lookup, dict):
            return (
                f"Parameter `estimator_type` must be None, a class, or a list of "
                f"class, but found: {repr(estimator_type)}"
            )
        else:
            return (
                f"Parameter `estimator_type` must be None, a string, a class, or a list"
                f" of [string or class]. Valid string values are: "
                f"{tuple(class_lookup.keys())}, but found: "
                f"{repr(estimator_type)}"
            )

    for i, estimator_type in enumerate(object_types):
        if isinstance(estimator_type, str):
            if not isinstance(class_lookup, dict) or (
                estimator_type not in class_lookup.keys()
            ):
                raise ValueError(_get_err_msg(estimator_type))
            estimator_type = class_lookup[estimator_type]
            object_types[i] = estimator_type
        elif isinstance(estimator_type, type):
            pass
        else:
            raise ValueError(_get_err_msg(estimator_type))
    return object_types


def _make_dataframe(all_objects, columns):
    """Create pandas.DataFrame from all_objects.

    Kept as a separate function with import to isolate the pandas dependency.
    """
    import pandas as pd

    return pd.DataFrame(all_objects, columns=columns)
