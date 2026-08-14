# -*- coding: utf-8 -*-
"""Tests for HTML representation of BaseObjects."""

from skbase.base import BaseObject
from skbase.base._meta import BaseMetaObject
from skbase.base._pretty_printing._object_html_repr import (
    _HTMLDocumentationLinkMixin,
    _object_html_repr,
)


class ComponentDummy(BaseObject):
    def __init__(self, a=1):
        self.a = a
        super().__init__()

    def __eq__(self, other):
        """Equality for test helper: objects equal if same type and `a` equals.

        This silences static analysis warnings about adding attributes
        without overriding `__eq__` and provides sensible equality for
        test comparisons. We intentionally do not implement `__hash__`
        because instances are mutable in tests.
        """
        if not isinstance(other, ComponentDummy):
            return NotImplemented
        return getattr(self, "a", None) == getattr(other, "a", None)

    __hash__ = None


class DocumentedDummy(BaseObject):
    """BaseObject with documented parameters.

    Parameters
    ----------
    alpha : int
        Documentation for alpha.
    beta : str
        Documentation for beta.
    """

    _html_repr_doc_link = "https://example.org/DocumentedDummy.html"

    def __init__(self, alpha=1, beta="default"):
        self.alpha = alpha
        self.beta = beta
        super().__init__()


class MetaObjectForHtml(BaseMetaObject):
    def __init__(self, steps=None):
        self.steps = steps
        super().__init__()


class ParentWithClassParam(BaseObject):
    """BaseObject whose parameter holds a BaseObject subclass, not an instance."""

    def __init__(self, nested_cls):
        self.nested_cls = nested_cls
        super().__init__()


class HtmlParamObject(BaseObject):
    """Object with parameters used to test HTML parameter rendering.

    Parameters
    ----------
    alpha : int
        Controls a numeric setting.
    beta : str
        Controls a text setting.
    payload : object
        Arbitrary payload.
    """

    _doc_link_template = "https://example.test/{object_module}.{object_name}.html"

    def __init__(self, alpha=1, beta="default", payload=None):
        self.alpha = alpha
        self.beta = beta
        self.payload = payload
        super().__init__()


class HtmlParentObject(BaseObject):
    """Object containing a nested BaseObject."""

    def __init__(self, child=None):
        self.child = child
        super().__init__()


class HtmlLinkedMixinObject(_HTMLDocumentationLinkMixin, BaseObject):
    """Object that receives docs links from the mixin defaults."""

    _doc_link_module = __name__.split(".")[0]
    _doc_link_template = "https://docs.example/{object_module}.{object_name}.html"

    def __init__(self, alpha=1):
        self.alpha = alpha
        super().__init__()


def test_html_repr_with_baseobject_class_param():
    """HTML diagram repr must not call get_params on a BaseObject class param.

    Regression test for https://github.com/sktime/skbase/issues/558
    """
    parent = ParentWithClassParam(nested_cls=ComponentDummy)
    html_repr = _object_html_repr(parent)
    assert isinstance(html_repr, str)
    assert parent.__class__.__name__ in html_repr


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
    assert meta.__class__.__name__ in html_repr
    assert "ComponentDummy" in html_repr


def test_html_repr_includes_shallow_parameter_table():
    """HTML repr includes escaped, truncated, changed/default shallow params."""
    payload = list(range(10))
    obj = HtmlParamObject(
        alpha=2,
        beta="<script>alert('xss')</script>",
        payload=payload,
    )

    html_repr = _object_html_repr(obj)

    assert "<summary>Parameters</summary>" in html_repr
    assert 'class="parameters-table sk-params-table"' in html_repr
    assert "sk-param-row--changed" in html_repr
    assert "sk-copy-btn" in html_repr
    assert "function skbaseCopyToClipboard" in html_repr
    assert "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;" in html_repr
    assert "<script>alert" not in html_repr
    assert "[0, 1, ...]" in html_repr


def test_html_repr_marks_default_parameters():
    """Parameters that match defaults receive default styling."""
    html_repr = _object_html_repr(HtmlParamObject())

    assert 'class="default sk-param-row--default"' in html_repr
    assert "sk-param-row--changed" not in html_repr


def test_html_repr_uses_nested_param_prefix_for_copy():
    """Nested parameter tables expose copy prefixes for deep set_params keys."""
    obj = HtmlParentObject(child=ComponentDummy(a=5))

    html_repr = _object_html_repr(obj)

    assert 'data-param-prefix="child__"' in html_repr


def test_html_repr_doc_links_from_class_attrs():
    """Class attributes opt objects into object and parameter doc links."""
    obj = HtmlParamObject(alpha=2)

    html_repr = _object_html_repr(obj)

    expected_doc = (
        "https://example.test/skbase.base._pretty_printing.tests."
        "test_object_html_repr.HtmlParamObject.html"
    )
    assert 'href="{}">'.format(expected_doc) in html_repr
    assert "Documentation for HtmlParamObject" in html_repr
    assert 'href="{}#:~:text=alpha,-int">'.format(expected_doc) in html_repr
    assert "Controls a numeric setting." in html_repr


def test_html_repr_doc_links_from_mixin():
    """The generic documentation mixin provides the same doc-link contract."""
    html_repr = _object_html_repr(HtmlLinkedMixinObject(alpha=2))

    expected_doc = (
        "https://docs.example/skbase.base._pretty_printing.tests."
        "test_object_html_repr.HtmlLinkedMixinObject.html"
    )
    assert 'href="{}">'.format(expected_doc) in html_repr


def test_html_repr_uses_direct_doc_link_attribute():
    """A direct HTML repr doc link is used for object and parameter docs."""
    html_repr = _object_html_repr(DocumentedDummy(alpha=2, beta="<tag>"))
    expected_doc = DocumentedDummy._html_repr_doc_link

    assert 'href="{}">'.format(expected_doc) in html_repr
    assert 'href="{}#:~:text=alpha,-int">'.format(expected_doc) in html_repr
    assert "Documentation for alpha." in html_repr
    assert "&lt;tag&gt;" in html_repr
