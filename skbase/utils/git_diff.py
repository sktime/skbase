"""Git related utilities to identify changed modules."""

__author__ = ["fkiraly"]
__all__ = []

import importlib.util
import inspect
from functools import lru_cache
from typing import List


@lru_cache
def get_module_from_class(cls):
    """Get full parent module string from class.

    Parameters
    ----------
    cls : class
        class to get module string from, e.g., NaiveForecaster

    Returns
    -------
    str : module string, e.g., sktime.forecasting.naive
    """
    module = inspect.getmodule(cls)
    return module.__name__ if module else None


@lru_cache
def get_path_from_module(module_str):
    r"""Get local path string from module string.

    Parameters
    ----------
    module_str : str
        module string, e.g., sktime.forecasting.naive

    Returns
    -------
    str : local path string, e.g., sktime\forecasting\naive.py
    """
    try:
        module_spec = importlib.util.find_spec(module_str)
        if module_spec is None:
            raise ImportError(
                f"Error in get_path_from_module, module {module_str!r} not found."
            )
        module_path = module_spec.origin
        if module_path.endswith("__init__.py"):
            return module_path[:-11]
        return module_path
    except Exception as e:
        raise ImportError(f"Error finding module {module_str!r}") from e


def _run_git_diff(cmd: List[str]) -> str:
    # Safety note: cmd is always a hard-coded list constructed in this module only.
    # No user input is ever injected → safe from shell injection.
    result = __import__("subprocess").run(  # nosec B404, B603
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout


@lru_cache
def is_module_changed(module_str):
    """Check if a module has changed compared to the main branch.

    If a child module has changed, the parent module is considered changed as well.

    Parameters
    ----------
    module_str : str
        module string, e.g., sktime.forecasting.naive
    """
    module_file_path = get_path_from_module(module_str)
    cmd = ["git", "diff", "remotes/origin/main", "--", module_file_path]
    output = _run_git_diff(cmd)
    return bool(output)


@lru_cache
def is_class_changed(cls):
    """Check if a class' parent module has changed compared to the main branch.

    Parameters
    ----------
    cls : class
        class to get module string from, e.g., NaiveForecaster

    Returns
    -------
    bool : True if changed, False otherwise
    """
    module_str = get_module_from_class(cls)
    return is_module_changed(module_str)


def get_changed_lines(file_path, only_indented=True):
    """Get changed or added lines from a file.

    Compares the current branch to the origin-main branch.

    Parameters
    ----------
    file_path : str
        path to file to get changed lines from
    only_indented : bool, default=True
        if True, only indented lines are returned, otherwise all lines are returned;
        more precisely, only changed/added lines starting with a space are returned

    Returns
    -------
    list of str : changed or added lines on current branch
    """
    cmd = ["git", "diff", "remotes/origin/main", "--", file_path]
    result_str = _run_git_diff(cmd)

    start_chars = "+ " if only_indented else "+"

    changed_lines = [
        line[1:].rstrip()
        for line in result_str.splitlines()
        if line.startswith(start_chars)
    ]

    if only_indented:
        changed_lines = [line for line in changed_lines if line and line[0] == " "]

    return changed_lines


def get_packages_with_changed_specs():
    """Get packages with changed or added specs.

    Returns
    -------
    list of str : names of packages with changed or added specs
    """
    return list(_get_packages_with_changed_specs())


@lru_cache
def _get_packages_with_changed_specs():
    """Get packages with changed or added specs.

    Private version of get_packages_with_changed_specs,
    to avoid side effects on the list return.

    Returns
    -------
    tuple of str : names of packages with changed or added specs
    """
    from packaging.requirements import InvalidRequirement, Requirement

    changed_lines = get_changed_lines("pyproject.toml")

    packages = []
    for line in changed_lines:
        if line.find("'") > line.find('"') and line.find('"') != -1:
            sep = '"'
        elif line.find("'") == -1:
            sep = '"'
        else:
            sep = "'"

        splits = line.split(sep)
        if len(splits) < 2:
            continue

        req = splits[1]

        if ";" in req:
            req = req.split(";")[0].strip()

        try:
            pkg = Requirement(req).name
        except InvalidRequirement:
            continue
        else:
            packages.append(pkg)

    packages = tuple(set(packages))

    return packages
