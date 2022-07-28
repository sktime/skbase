# -*- coding: utf-8 -*-
# copyright: BaseObject developers, BSD-3-Clause License (see LICENSE file)
"""Tools to lookup information on code artifacts in a Python package or module.

This module exports the following methods for registry lookup:

package_metadata()
    Walk package and return metadata on included classes and functions by module.
all_objects(object_types, filter_tags)
    Look (and optionally filter) BaseObject descendents in a package or module.

"""
# all_objects is based on the sktime all_estimator retrieval utility, which
# is based on the sklearn estimator retrieval utility of the same name
# See https://github.com/scikit-learn/scikit-learn/blob/main/COPYING and
# https://github.com/alan-turing-institute/sktime/blob/main/LICENSE
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
from types import FunctionType, ModuleType
from typing import (
    Any,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from baseobject import BaseObject

# Conditionally import TypedDict based on Python version
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__: List[str] = ["all_objects", "package_metadata"]
__author__: List[str] = [
    "fkiraly",
    "mloning",
    "katiebuc",
    "miraep8",
    "xloem",
    "rnkuhns",
]


class ClassInfo(TypedDict):
    """Type definitions for information on a module's classes."""

    klass: Type
    name: str
    description: str
    tags: MutableMapping[str, Any]
    is_concrete_implementation: bool
    is_base_class: bool
    is_base_object: bool
    authors: Optional[Union[List[str], str]]
    module_name: str


class FunctionInfo(TypedDict):
    """Type definitions for information on a module's functions."""

    func: FunctionType
    name: str
    description: str
    module_name: str


class ModuleInfo(TypedDict):
    """Module information type definitions."""

    path: str
    name: str
    classes: MutableMapping[str, ClassInfo]
    functions: MutableMapping[str, FunctionInfo]
    __all__: List[str]
    authors: str
    is_package: bool
    contains_concrete_class_implementations: bool
    contains_base_classes: bool
    contains_base_objects: bool


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
    is_non_public: bool = "._" in module_name
    return is_non_public


def _is_ignored_module(
    module_name: str, modules_to_ignore: Union[List[str], Tuple[str]] = None
) -> bool:
    """Determine if module is one of the ignored modules.

    Paramters
    ---------
    module_name : str
        Name of the module.
    modules_to_ignore : list[str] or tuple[str]
        The modules that should be ignored when walking the package.

    Returns
    -------
    is_ignored : bool
        Whether the module is an ignrored module or not.
    """
    is_ignored: bool
    if modules_to_ignore is not None:
        is_ignored = any(part in modules_to_ignore for part in module_name.split("."))
    else:
        is_ignored = False
    return is_ignored


def _is_abstract(klass: type) -> bool:
    """Determine if a class is an abstract class.

    Parameters
    ----------
    klass : object
        Class to check.

    Returns
    -------
    is_abstract : bool
        Whether the input class is an abstract class or not.
    """
    # Simplify check by starting as an abstract class
    is_abstract = True
    if not (hasattr(klass, "__abstractmethods__")):
        is_abstract = False
    elif not len(klass.__abstractmethods__):
        is_abstract = False
    return is_abstract


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
    """
    if class_filter is None:
        is_subclass = True
    else:
        if isinstance(class_filter, Iterable) and not isinstance(class_filter, tuple):
            class_filter = tuple(class_filter)
        if issubclass(klass, class_filter):
            is_subclass = True
        else:
            is_subclass = False
    return is_subclass


def _filter_by_tags(
    klass: type,
    tag_filter: Optional[Union[str, Sequence[str], Mapping[str, Any]]] = None,
) -> bool:
    """Determine if a class has a tag or has certain values for a tag.

    Parameters
    ----------
    klass : object
        Class to check.
    tag_filter : str, iterable of str or dict
        Filter used to determine if `klass` has tag or expected tag values.

    Returns
    -------
    has_tag : bool
        Whether the input class has tags defined by the `tag_filter`.
    """
    if tag_filter is None:
        return True
    if hasattr(klass, "get_class_tags"):
        klass_tags = klass.get_class_tags()
    # If a string is supplied verify it is in the returned tag dict
    if isinstance(tag_filter, str):
        has_tag = tag_filter in klass_tags
    # If a iterable of strings is provided, check that all are in the returned tag_dict
    elif isinstance(tag_filter, Iterable) and all(
        [isinstance(t, str) for t in tag_filter]
    ):
        has_tag = all([tag in klass_tags for tag in tag_filter])
    # If a dict is suppied verify that tag and value are acceptable
    elif isinstance(tag_filter, dict):
        for tag, value in tag_filter.items():
            if not isinstance(value, Iterable):
                value = [value]
                if tag in klass_tags:
                    has_tag = klass_tags[tag] in set(value)
                else:
                    has_tag = False
                # We can break the loop and return has_tag as False if it is ever False
                if not has_tag:
                    break
    else:
        raise ValueError(
            "`tag_filter` should be a string tag name, iterable of string tag names, "
            "or a dictionary mapping tag names to allowable values. "
            f"But `tag_filter` has type {type(tag_filter)}."
        )

    return has_tag


def _import_module(
    module_name: str,
    suppress_import_stdout: bool = True,
    loader: importlib.machinery.SourceFileLoader = None,
) -> ModuleType:
    """Import a module, while optionally suppressing import standard out.

    Parameters
    ----------
    module_name : str
        Name of the module to be imported.
    suppress_import_stdout : bool, default=True
        Whether to suppress stdout printout upon import.
    loader : importlib.machinery.SourceFileLoader, default=None
        If provided, this should be the loader to load the module.

    Returns
    -------
    module : ModuleType
        The module that was imported.
    """
    if loader is None:
        if suppress_import_stdout:
            # setup text trap, import, then restore
            sys.stdout = io.StringIO()
            module = importlib.import_module(module_name)
            sys.stdout = sys.__stdout__
        else:
            module = importlib.import_module(module_name)
    else:
        if suppress_import_stdout:
            sys.stdout = io.StringIO()
            module = loader.load_module()
            sys.stdout = sys.__stdout__
        else:
            module = loader.load_module()
    return module


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
            # path = Path(module.__file__).parent
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
                module = _import_module(
                    package_name, suppress_import_stdout=False, loader=loader
                )
            except ImportError:
                raise ValueError(
                    f"Unable to import a package named {package_name} based "
                    f"on provided `path`: {path_}."
                )
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
) -> ModuleInfo:
    # Make package_base_classes a tuple if it was supplied as a class
    base_classes_none = False
    if isinstance(package_base_classes, Iterable):
        package_base_classes = tuple(package_base_classes)
    elif not isinstance(package_base_classes, tuple):
        if package_base_classes is None:
            base_classes_none = True
        package_base_classes = (package_base_classes,)
    designed_imports: List[str] = getattr(module, "__all__", [])
    authors: Union[str, List[str]] = getattr(module, "__author__", [])
    if isinstance(authors, (list, tuple)):
        authors = ", ".join(authors)
    # Compile information on classes in the module
    module_classes: MutableMapping[str, ClassInfo] = {}
    for name, klass in inspect.getmembers(module, inspect.isclass):
        # Skip a class if non-public items should be excluded and it starts with "_"
        if exclude_non_public_items and klass.__name__.startswith("_"):
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

    module_functions: MutableMapping[str, FunctionInfo] = {}
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if func.__module__ == module.__name__ or name in designed_imports:
            # Skip a class if non-public items should be excluded and it starts with "_"
            if exclude_non_public_items and klass.__name__.startswith("_"):
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
    module_info: ModuleInfo = {
        "path": path,
        "name": module.__name__,
        "classes": module_classes,
        "functions": module_functions,
        "__all__": designed_imports,
        "authors": authors,
        "is_package": is_pkg,
        "contains_concrete_class_implementations": False,
        "contains_base_classes": any(
            v["is_base_class"] for v in module_classes.values()
        ),
        "contains_base_objects": any(
            v["is_base_object"] for v in module_classes.values()
        ),
    }
    return module_info


def package_metadata(
    package_name: str,
    path: Optional[str] = None,
    recursive: bool = True,
    exclude_non_public_items: bool = True,
    exclude_nonpublic_modules: bool = True,
    modules_to_ignore: Union[List[str], Tuple[str]] = ("tests",),
    package_base_classes: Union[type, Tuple[type, ...]] = (BaseObject,),
    suppress_import_stdout: bool = True,
) -> Mapping[str, ModuleInfo]:
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
    modules_to_ignore : list[str] or tuple[str], default=()
        The modules that should be ignored when walking the package.
    package_base_classes: type or Sequence[type], default = (BaseObject,)
        The base classes used to determine if any classes found in metadata descend
        from a base class.

    Other Parameters
    ----------------
    suppress_import_stdout : bool, default=True
        Whether to suppress stdout printout upon import.

    Returns
    -------
    module_info: dict
        Dictionary mapping string submodule name (key) to a dictionary of the
        submodules metadata.
    """
    module, path, loader = _determine_module_path(package_name, path)
    module_info: MutableMapping[str, ModuleInfo] = {}
    # Get any metadata at the top-level of the provided package
    # This is because the pkgutil.walk_packages doesn't include __init__
    # file when walking a package
    module_info[package_name] = _get_module_info(
        module,
        loader.is_package(package_name),
        path,
        package_base_classes,
        exclude_non_public_items=exclude_non_public_items,
    )

    # Now walk through any submodules
    prefix = f"{package_name}."
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        warnings.simplefilter("module", category=ImportWarning)
        warnings.filterwarnings(
            "ignore", category=UserWarning, message=".*has been moved to.*"
        )
        for _, name, is_pkg in pkgutil.walk_packages(path=[path], prefix=prefix):
            # Used to skip-over ignored modules and non-public modules
            if _is_ignored_module(name, modules_to_ignore=modules_to_ignore) or (
                exclude_nonpublic_modules and _is_non_public_module(name)
            ):
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
                )
            except ImportError:
                continue

            if recursive and is_pkg:
                name_ending: str = name.split(".")[1] if "." in name else name
                updated_path: str = "\\".join([path, name_ending])
                module_info.update(
                    package_metadata(
                        package_name=name,
                        path=updated_path,
                        recursive=recursive,
                        exclude_non_public_items=exclude_non_public_items,
                        exclude_nonpublic_modules=exclude_nonpublic_modules,
                        modules_to_ignore=modules_to_ignore,
                        package_base_classes=package_base_classes,
                    )
                )

    return module_info


def all_objects(
    object_types=None,
    filter_tags=None,
    exclude_estimators=None,
    return_names=True,
    as_dataframe=False,
    return_tags=None,
    suppress_import_stdout=True,
    package_name="baseobject",
    path: Optional[str] = None,
    ignore_modules=None,
    class_lookup=None,
):
    """Get a list of all estimators in the package with name `package_name`.

    This function crawls the package/module and gets all classes that
    are descendents of BaseObject. These classes can be retrieved
    based on their inherittence from intermediate classes, and their tags.

    Parameters
    ----------
    object_types: class or list of classes, default=None
        - If class_lookup is provided, can also be str or list of str
          which kind of objects should be returned.
        - If None, no filter is applied and all estimators are returned.
        - If class or list of class, estimators are filtered to inherit from
          one of these.
        - If str or list of str, classes ca be aliased by strings, via class_lookup.
    return_names: bool, default=True
        - If True, estimator class name is included in the all_estimators()
          return in the order: name, estimator class, optional tags, either as
          a tuple or as pandas.DataFrame columns.
        if False, estimator class name is removed from the all_estimators()
            return.
    filter_tags: dict of (str or list of str), optional (default=None)
        For a list of valid tag strings, use the registry.all_tags utility.
        subsets the returned estimators as follows:
            each key/value pair is statement in "and"/conjunction
                key is tag name to sub-set on
                value str or list of string are tag values
                condition is "key must be equal to value, or in set(value)".
    exclude_estimators: str or list of str, odefault=None
        Names of estimators to exclude.
    as_dataframe: bool, default=False
        - If False, all_estimators will return a list (either a list of
            estimators or a list of tuples, see Returns).
        - If True, all_estimators will return a pandas.DataFrame with named
            columns for all of the attributes being returned.
            this requires soft dependency pandas to be installed.
    return_tags: str or list of str, default=None
        Names of tags to fetch and return each estimator's value of.
        For a list of valid tag strings, use the registry.all_tags utility.
        If str or list of str, the tag values named in return_tags will be
        fetched for each object and will be appended as either columns or
        tuple entries.
    package_name : str, default="baseobject".
        should be set to default to package or module name if used for search.
        objects will be searched inside the package/module called package_name,
        this can include sub-module dots, e.g., "package.module1.module2".
    path : str, default=None
        If provided, this should be the path that should be used as root
        to find `package_name` and start the search for any submodules/packages.
    ignore_modules : str or lits of str, optional. Default=empty list
        list of module names to ignore in search.
    class_lookup : dict[str, class], default=None
        Dictionary of aliases for classes used in object_types.

    Other Parameters
    ----------------
    suppress_import_stdout : bool, default=True
        whether to suppress stdout printout upon import.

    Returns
    -------
    all_estimators will return one of the following:
        1. list of estimators, if return_names=False, and return_tags is None
        2. list of tuples (optional estimator name, class, ~optional estimator
                tags), if return_names=True or return_tags is not None.
        3. pandas.DataFrame if as_dataframe = True

        - If list of estimators, entries are estimators matching the query,
          in alphabetical order of estimator name
        - If list of tuples list of (optional estimator name, estimator,
          optional estimator tags) matching the query,
          in alphabetical order of estimator name, where:

           - ``name`` is the estimator name as string, and is an
             optional return
            - ``estimator`` is the actual estimator
            - ``tags`` are the estimator's values for each tag in return_tags
              and is an optional return.

        - If dataframe, all_estimators will return a pandas.DataFrame.
          Column names represent the attributes contained in each column.
          "estimators" will be the name of the column of estimators, "names"
          will be the name of the column of estimator class names and the string(s)
          passed in return_tags will serve as column names for all columns of
          tags that were optionally requested.

    References
    ----------
    Modified version of scikit-learn's and sktime's `all_estimators()`.
    """
    module, root, _ = _determine_module_path(package_name, path)

    if ignore_modules is None:
        modules_to_ignore = []
    else:
        modules_to_ignore = ignore_modules

    all_estimators = []
    # root = str(pathlib.Path(__file__).parent.parent)  # sktime package root directory

    # def _is_abstract(klass):
    #     if not (hasattr(klass, "__abstractmethods__")):
    #         return False
    #     if not len(klass.__abstractmethods__):
    #         return False
    #     return True

    def _is_private_module(module):
        return "._" in module

    def _is_ignored_module(module):
        module_parts = module.split(".")
        return any(part in modules_to_ignore for part in module_parts)

    def _is_base_class(name):
        return name.startswith("_") or name.startswith("Base")

    def _is_estimator(name, klass):
        # Check if klass is subclass of base estimators, not an base class itself and
        # not an abstract class
        return issubclass(klass, BaseObject) and not _is_base_class(name)

    # Ignore deprecation warnings triggered at import time and from walking
    # packages
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        warnings.simplefilter("module", category=ImportWarning)
        warnings.filterwarnings(
            "ignore", category=UserWarning, message=".*has been moved to.*"
        )
        prefix = f"{package_name}."
        for _, module_name, _ in pkgutil.walk_packages(path=[root], prefix=prefix):
            # Filter modules
            if _is_ignored_module(module_name) or _is_private_module(module_name):
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
                    (name, klass)
                    for name, klass in classes
                    if _is_estimator(name, klass)
                ]
                all_estimators.extend(estimators)
            except ModuleNotFoundError as e:
                # Skip missing soft dependencies
                if "soft dependency" not in str(e):
                    raise e
                warnings.warn(str(e), ImportWarning)

    # Drop duplicates
    all_estimators = set(all_estimators)

    # Filter based on given estimator types
    def _is_in_object_types(estimator, object_types):
        return any(
            inspect.isclass(x) and isinstance(estimator, x) for x in object_types
        )

    if object_types:
        object_types = _check_object_types(object_types, class_lookup)
        all_estimators = [
            (name, estimator)
            for name, estimator in all_estimators
            if _is_in_object_types(estimator, object_types)
        ]

    # Filter based on given exclude list
    if exclude_estimators:
        exclude_estimators = _check_list_of_str_or_error(
            exclude_estimators, "exclude_estimators"
        )
        all_estimators = [
            (name, estimator)
            for name, estimator in all_estimators
            if name not in exclude_estimators
        ]

    # Drop duplicates, sort for reproducibility
    # itemgetter is used to ensure the sort does not extend to the 2nd item of
    # the tuple
    all_estimators = sorted(all_estimators, key=itemgetter(0))

    if filter_tags:
        all_estimators = [
            (n, est) for (n, est) in all_estimators if _check_tag_cond(est, filter_tags)
        ]

    # remove names if return_names=False
    if not return_names:
        all_estimators = [estimator for (name, estimator) in all_estimators]
        columns = ["estimator"]
    else:
        columns = ["name", "estimator"]

    # add new tuple entries to all_estimators for each tag in return_tags:
    if return_tags:
        return_tags = _check_list_of_str_or_error(return_tags, "return_tags")
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


def _check_list_of_str_or_error(arg_to_check, arg_name):
    """Check that certain arguments are str or list of str.

    Parameters
    ----------
    arg_to_check: any
        Argument we are testing the type of.
    arg_name: str,
        name of the argument we are testing, will be added to the error if
        ``arg_to_check`` is not a str or a list of str.

    Returns
    -------
    arg_to_check: list of str,
        if arg_to_check was originally a str it converts it into a list of str
        so that it can be iterated over.

    Raises
    ------
    TypeError if arg_to_check is not a str or list of str.
    """
    # check that return_tags has the right type:
    if isinstance(arg_to_check, str):
        arg_to_check = [arg_to_check]
    elif not isinstance(arg_to_check, list) or not all(
        isinstance(value, str) for value in arg_to_check
    ):
        raise TypeError(
            f"Input error. Argument {arg_name} must be either\
             a str or list of str"
        )
    return arg_to_check


def _check_iterable_of_class_or_error(arg_to_check, arg_name, coerce_to_list=False):
    """Check that certain arguments are class or list of class.

    Parameters
    ----------
    arg_to_check: any
        Argument we are testing the type of.
    arg_name: str
        name of the argument we are testing, will be added to the error if
        ``arg_to_check`` is not a str or a list of str.
    coerce_to_list : bool, default=False
        Whether `arg_to_check` should be coerced to a list prior to return.

    Returns
    -------
    arg_to_check: list of class,
        If `arg_to_check` was originally a class it converts it into a list
        containing the class so it can be iterated over. Otherwise,
        `arg_to_check` is returned.

    Raises
    ------
    TypeError:
        If `arg_to_check` is not a class or iterable of class.
    """
    # check that return_tags has the right type:
    if inspect.isclass(arg_to_check):
        arg_to_check = [arg_to_check]
    elif not (
        isinstance(arg_to_check, Iterable)
        and all(inspect.isclass(value) for value in arg_to_check)
    ):
        raise TypeError(
            f"Input error. Argument {arg_name} must be either\
             a class or an iterable of classes"
        )
    elif coerce_to_list:
        arg_to_check = list(arg_to_check)
    return arg_to_check


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


def _check_tag_cond(estimator, filter_tags=None, as_dataframe=True):
    """Check whether estimator satisfies filter_tags condition.

    Parameters
    ----------
    estimator: BaseObject
        Class inheritting from BaseOBject.
    filter_tags: dict of (str or list of str), default=None
        subsets the returned estimators as follows:
            each key/value pair is statement in "and"/conjunction
                key is tag name to sub-set on
                value str or list of string are tag values
                condition is "key must be equal to value, or in set(value)".
    as_dataframe: bool, default=False

        - If False, return is as described below.
        - If True, return is converted into a pandas.DataFrame for pretty
          display.

    Returns
    -------
    cond_sat: bool
        Whether estimator satisfies condition in filter_tags.
    """
    if not isinstance(filter_tags, dict):
        raise TypeError("filter_tags must be a dict")

    cond_sat = True

    for (key, value) in filter_tags.items():
        if not isinstance(value, list):
            value = [value]
        cond_sat = cond_sat and estimator.get_class_tag(key) in set(value)

    return cond_sat


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
        if class_lookup is None:
            return (
                f"Parameter `estimator_type` must be None, a sclass, or a list of "
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
        if not isinstance(estimator_type, (type, str)):
            raise ValueError(_get_err_msg(estimator_type))
        if isinstance(estimator_type, str):
            if estimator_type not in class_lookup.keys():
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
