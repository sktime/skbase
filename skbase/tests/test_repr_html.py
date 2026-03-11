# -*- coding: utf-8 -*-
"""Tests for BaseObject HTML representation."""

from skbase.base import BaseObject

class DummyObject(BaseObject):
    """Dummy object for testing."""
    def __init__(self, a=1, b="test"):
        self.a = a
        self.b = b
        super().__init__()

class CompositeObject(BaseObject):
    """Composite object for testing."""
    def __init__(self, obj=None, c=42):
        self.obj = obj
        self.c = c
        super().__init__()

def test_repr_html_default_text():
    """Test that default display="text" config returns None for _repr_html_."""
    obj = DummyObject()
    # default config is "text"
    assert obj._repr_html_() is None
    
    # explicit config
    obj.set_config(display="text")
    assert obj._repr_html_() is None

def test_repr_html_diagram():
    """Test that display="diagram" config returns valid HTML."""
    obj = DummyObject(a=100, b="hello")
    obj.set_config(display="diagram")
    html_repr = obj._repr_html_()
    
    assert html_repr is not None
    assert isinstance(html_repr, str)
    assert "DummyObject" in html_repr
    assert "<strong>a</strong>" in html_repr
    assert "<code>100</code>" in html_repr
    assert "<strong>b</strong>" in html_repr
    assert "<code>&#x27;hello&#x27;</code>" in html_repr or "<code>'hello'</code>" in html_repr

def test_repr_html_composite():
    """Test that composite object renders collapsible details."""
    inner = DummyObject(a=5, b="inner_str")
    obj = CompositeObject(obj=inner, c=99)
    obj.set_config(display="diagram")
    
    html_repr = obj._repr_html_()
    
    assert html_repr is not None
    assert "CompositeObject" in html_repr
    assert "DummyObject" in html_repr
    
    # Check for details and summary tags used for nested BaseObjects
    assert "<details" in html_repr
    assert "<summary" in html_repr
    
    # Check that inner object's parameters are rendered
    assert "<strong>a</strong>" in html_repr
    assert "<code>5</code>" in html_repr
    assert "<strong>obj</strong>" in html_repr
