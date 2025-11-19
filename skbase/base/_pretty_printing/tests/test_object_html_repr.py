# -*- coding: utf-8 -*-
"""Tests for HTML representation of meta-objects (regression for #160/#163)."""

from skbase.base import BaseObject
from skbase.base._meta import BaseMetaObject
from skbase.base._pretty_printing._object_html_repr import _object_html_repr


class ComponentDummy(BaseObject):
    def __init__(self, a=1):
        self.a = a
        super().__init__()


class MetaObjectForHtml(BaseMetaObject):
    def __init__(self, steps=None):
        self.steps = steps
        super().__init__()


def test_meta_object_html_repr_does_not_raise():
    """Ensure HTML repr for a meta-object does not raise (regression test).

    This covers the failure case where displaying meta-objects as HTML used an
    incorrect VisualBlock import and would crash. The function should return
    an HTML string and not raise an exception.
    """
    steps = [("comp", ComponentDummy(42))]
    meta = MetaObjectForHtml(steps=steps)

    html_repr = _object_html_repr(meta)

    assert isinstance(html_repr, str)
    # should include the class name and at least one html tag
    assert meta.__class__.__name__ in html_repr
    assert "<div" in html_repr
