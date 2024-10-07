# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
# Many elements of this code were developed in scikit-learn. These elements
# are copyrighted by the scikit-learn developers, BSD-3-Clause License. For
# conditions see https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
"""Utility functionality for pretty-printing objects used in BaseObject.__repr__."""
import inspect
import pprint
from collections import OrderedDict

from skbase.base import BaseObject

# from skbase.config import get_config
from skbase.utils._check import _is_scalar_nan


class KeyValTuple(tuple):
    """Dummy class for correctly rendering key-value tuples from dicts."""

    def __repr__(self):
        """Represent as string."""
        # needed for _dispatch[tuple.__repr__] not to be overridden
        return super().__repr__()


class KeyValTupleParam(KeyValTuple):
    """Dummy class for correctly rendering key-value tuples from parameters."""

    pass


def _changed_params(base_object):
    """Return dict (param_name: value) of parameters with non-default values."""
    params = base_object.get_params(deep=False)
    init_func = getattr(
        base_object.__init__, "deprecated_original", base_object.__init__
    )
    init_params = inspect.signature(init_func).parameters
    init_params = {name: param.default for name, param in init_params.items()}

    def has_changed(k, v):
        if k not in init_params:  # happens if k is part of a **kwargs
            return True
        if init_params[k] == inspect._empty:  # k has no default value
            return True
        # try to avoid calling repr on nested BaseObjects
        if isinstance(v, BaseObject) and v.__class__ != init_params[k].__class__:
            return True
        # Use repr as a last resort. It may be expensive.
        if repr(v) != repr(init_params[k]) and not (
            _is_scalar_nan(init_params[k]) and _is_scalar_nan(v)
        ):
            return True
        return False

    return {k: v for k, v in params.items() if has_changed(k, v)}


class _BaseObjectPrettyPrinter(pprint.PrettyPrinter):
    """Pretty Printer class for BaseObjects.

    This extends the pprint.PrettyPrinter class similar to scikit-learn's
    implementation, so that:

    - BaseObjects are printed with their parameters, e.g.
      BaseObject(param1=value1, ...) which is not supported by default.
    - the 'compact' parameter of PrettyPrinter is ignored for dicts, which
      may lead to very long representations that we want to avoid.

    Quick overview of pprint.PrettyPrinter (see also
    https://stackoverflow.com/questions/49565047/pprint-with-hex-numbers):

    - the entry point is the _format() method which calls format() (overridden
      here)
    - format() directly calls _safe_repr() for a first try at rendering the
      object
    - _safe_repr formats the whole object recursively, only calling itself,
      not caring about line length or anything
    - back to _format(), if the output string is too long, _format() then calls
      the appropriate _pprint_TYPE() method (e.g. _pprint_list()) depending on
      the type of the object. This where the line length and the compact
      parameters are taken into account.
    - those _pprint_TYPE() methods will internally use the format() method for
      rendering the nested objects of an object (e.g. the elements of a list)

    In the end, everything has to be implemented twice: in _safe_repr and in
    the custom _pprint_TYPE methods. Unfortunately PrettyPrinter is really not
    straightforward to extend (especially when we want a compact output), so
    the code is a bit convoluted.

    This class overrides:
    - format() to support the changed_only parameter
    - _safe_repr to support printing of BaseObjects that fit on a single line
    - _format_dict_items so that dict are correctly 'compacted'
    - _format_items so that ellipsis is used on long lists and tuples

    When BaseObjects cannot be printed on a single line, the builtin _format()
    will call _pprint_object() because it was registered to do so (see
    _dispatch[BaseObject.__repr__] = _pprint_object).

    both _format_dict_items() and _pprint_Object() use the
    _format_params_or_dict_items() method that will format parameters and
    key-value pairs respecting the compact parameter. This method needs another
    subroutine _pprint_key_val_tuple() used when a parameter or a key-value
    pair is too long to fit on a single line. This subroutine is called in
    _format() and is registered as well in the _dispatch dict (just like
    _pprint_object). We had to create the two classes KeyValTuple and
    KeyValTupleParam for this.
    """

    def __init__(
        self,
        indent=1,
        width=80,
        depth=None,
        stream=None,
        *,
        compact=False,
        indent_at_name=True,
        n_max_elements_to_show=None,
        changed_only=True,
    ):
        super().__init__(indent, width, depth, stream, compact=compact)
        self._indent_at_name = indent_at_name
        if self._indent_at_name:
            self._indent_per_level = 1  # ignore indent param
        self.changed_only = changed_only
        # Max number of elements in a list, dict, tuple until we start using
        # ellipsis. This also affects the number of arguments of a BaseObject
        # (they are treated as dicts)
        self.n_max_elements_to_show = n_max_elements_to_show

    def format(self, obj, context, maxlevels, level):  # noqa
        return _safe_repr(
            obj, context, maxlevels, level, changed_only=self.changed_only
        )

    def _pprint_object(self, obj, stream, indent, allowance, context, level):
        stream.write(obj.__class__.__name__ + "(")
        if self._indent_at_name:
            indent += len(obj.__class__.__name__)

        if self.changed_only:
            params = _changed_params(obj)
        else:
            params = obj.get_params(deep=False)

        params = OrderedDict((name, val) for (name, val) in sorted(params.items()))

        self._format_params(
            params.items(), stream, indent, allowance + 1, context, level
        )
        stream.write(")")

    def _format_dict_items(self, items, stream, indent, allowance, context, level):
        return self._format_params_or_dict_items(
            items, stream, indent, allowance, context, level, is_dict=True
        )

    def _format_params(self, items, stream, indent, allowance, context, level):
        return self._format_params_or_dict_items(
            items, stream, indent, allowance, context, level, is_dict=False
        )

    def _format_params_or_dict_items(
        self, obj, stream, indent, allowance, context, level, is_dict
    ):
        """Format dict items or parameters respecting the compact=True parameter.

        For some reason, the builtin rendering of dict items doesn't
        respect compact=True and will use one line per key-value if all cannot
        fit in a single line.
        Dict items will be rendered as <'key': value> while params will be
        rendered as <key=value>. The implementation is mostly copy/pasting from
        the builtin _format_items().
        This also adds ellipsis if the number of items is greater than
        self.n_max_elements_to_show.
        """
        write = stream.write
        indent += self._indent_per_level
        delimnl = ",\n" + " " * indent
        delim = ""
        width = max_width = self._width - indent + 1
        it = iter(obj)
        try:
            next_ent = next(it)
        except StopIteration:
            return
        last = False
        n_items = 0
        while not last:
            if n_items == self.n_max_elements_to_show:
                write(", ...")
                break
            n_items += 1
            ent = next_ent
            try:
                next_ent = next(it)
            except StopIteration:
                last = True
                max_width -= allowance
                width -= allowance
            if self._compact:
                k, v = ent
                krepr = self._repr(k, context, level)
                vrepr = self._repr(v, context, level)
                if not is_dict:
                    krepr = krepr.strip("'")
                middle = ": " if is_dict else "="
                rep = krepr + middle + vrepr
                w = len(rep) + 2
                if width < w:
                    width = max_width
                    if delim:
                        delim = delimnl
                if width >= w:
                    width -= w
                    write(delim)
                    delim = ", "
                    write(rep)
                    continue
            write(delim)
            delim = delimnl
            class_ = KeyValTuple if is_dict else KeyValTupleParam
            self._format(
                class_(ent), stream, indent, allowance if last else 1, context, level
            )

    def _format_items(self, items, stream, indent, allowance, context, level):
        """Format the items of an iterable (list, tuple...).

        Same as the built-in _format_items, with support for ellipsis if the
        number of elements is greater than self.n_max_elements_to_show.
        """
        write = stream.write
        indent += self._indent_per_level
        if self._indent_per_level > 1:
            write((self._indent_per_level - 1) * " ")
        delimnl = ",\n" + " " * indent
        delim = ""
        width = max_width = self._width - indent + 1
        it = iter(items)
        try:
            next_ent = next(it)
        except StopIteration:
            return
        last = False
        n_items = 0
        while not last:
            if n_items == self.n_max_elements_to_show:
                write(", ...")
                break
            n_items += 1
            ent = next_ent
            try:
                next_ent = next(it)
            except StopIteration:
                last = True
                max_width -= allowance
                width -= allowance
            if self._compact:
                rep = self._repr(ent, context, level)
                w = len(rep) + 2
                if width < w:
                    width = max_width
                    if delim:
                        delim = delimnl
                if width >= w:
                    width -= w
                    write(delim)
                    delim = ", "
                    write(rep)
                    continue
            write(delim)
            delim = delimnl
            self._format(ent, stream, indent, allowance if last else 1, context, level)

    def _pprint_key_val_tuple(self, obj, stream, indent, allowance, context, level):
        """Pretty printing for key-value tuples from dict or parameters."""
        k, v = obj
        rep = self._repr(k, context, level)
        if isinstance(obj, KeyValTupleParam):
            rep = rep.strip("'")
            middle = "="
        else:
            middle = ": "
        stream.write(rep)
        stream.write(middle)
        self._format(
            v, stream, indent + len(rep) + len(middle), allowance, context, level
        )

    # Follow what scikit-learn did here and copy _dispatch to prevent instances
    # of the builtin PrettyPrinter class to call methods of
    # _BaseObjectPrettyPrinter (see scikit-learn Github issue 12906)
    # mypy error: "Type[PrettyPrinter]" has no attribute "_dispatch"
    _dispatch = pprint.PrettyPrinter._dispatch.copy()  # type: ignore
    _dispatch[BaseObject.__repr__] = _pprint_object
    _dispatch[KeyValTuple.__repr__] = _pprint_key_val_tuple


def _safe_repr(obj, context, maxlevels, level, changed_only=False):
    """Safe string representation logic.

    Same as the builtin _safe_repr, with added support for BaseObjects.
    """
    typ = type(obj)

    if typ in pprint._builtin_scalars:
        return repr(obj), True, False

    r = getattr(typ, "__repr__", None)
    if issubclass(typ, dict) and r is dict.__repr__:
        if not obj:
            return "{}", True, False
        objid = id(obj)
        if maxlevels and level >= maxlevels:
            return "{...}", False, objid in context
        if objid in context:
            return pprint._recursion(obj), False, True
        context[objid] = 1
        readable = True
        recursive = False
        components = []
        append = components.append
        level += 1
        saferepr = _safe_repr
        items = sorted(obj.items(), key=pprint._safe_tuple)
        for k, v in items:
            krepr, kreadable, krecur = saferepr(
                k, context, maxlevels, level, changed_only=changed_only
            )
            vrepr, vreadable, vrecur = saferepr(
                v, context, maxlevels, level, changed_only=changed_only
            )
            append("%s: %s" % (krepr, vrepr))
            readable = readable and kreadable and vreadable
            if krecur or vrecur:
                recursive = True
        del context[objid]
        return "{%s}" % ", ".join(components), readable, recursive

    if (issubclass(typ, list) and r is list.__repr__) or (
        issubclass(typ, tuple) and r is tuple.__repr__
    ):
        if issubclass(typ, list):
            if not obj:
                return "[]", True, False
            format_ = "[%s]"
        elif len(obj) == 1:
            format_ = "(%s,)"
        else:
            if not obj:
                return "()", True, False
            format_ = "(%s)"
        objid = id(obj)
        if maxlevels and level >= maxlevels:
            return format_ % "...", False, objid in context
        if objid in context:
            return pprint._recursion(obj), False, True
        context[objid] = 1
        readable = True
        recursive = False
        components = []
        append = components.append
        level += 1
        for o in obj:
            orepr, oreadable, orecur = _safe_repr(
                o, context, maxlevels, level, changed_only=changed_only
            )
            append(orepr)
            if not oreadable:
                readable = False
            if orecur:
                recursive = True
        del context[objid]
        return format_ % ", ".join(components), readable, recursive

    if issubclass(typ, BaseObject):
        objid = id(obj)
        if maxlevels and level >= maxlevels:
            return "{...}", False, objid in context
        if objid in context:
            return pprint._recursion(obj), False, True
        context[objid] = 1
        readable = True
        recursive = False
        if changed_only:
            params = _changed_params(obj)
        else:
            params = obj.get_params(deep=False)
        components = []
        append = components.append
        level += 1
        saferepr = _safe_repr
        items = sorted(params.items(), key=pprint._safe_tuple)
        for k, v in items:
            krepr, kreadable, krecur = saferepr(
                k, context, maxlevels, level, changed_only=changed_only
            )
            vrepr, vreadable, vrecur = saferepr(
                v, context, maxlevels, level, changed_only=changed_only
            )
            append("%s=%s" % (krepr.strip("'"), vrepr))
            readable = readable and kreadable and vreadable
            if krecur or vrecur:
                recursive = True
        del context[objid]
        return ("%s(%s)" % (typ.__name__, ", ".join(components)), readable, recursive)

    rep = repr(obj)
    return rep, (rep and not rep.startswith("<")), False
