# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)
"""Tests the aliasing logic in the Tag Aliaser."""

import re

import pytest

from skbase.base import BaseObject as _BaseObject
from skbase.base._base import TagAliaserMixin as _TagAliaserMixin


class AliaserTestClass(_TagAliaserMixin, _BaseObject):
    """Class for testing tag aliasing logic."""

    _tags = {
        "new_tag_1": "new_tag_1_value",
        "old_tag_1": "old_tag_1_value",
        "new_tag_2": "new_tag_2_value",
        "old_tag_3": "old_tag_3_value",
    }

    alias_dict = {
        "old_tag_1": "new_tag_1",
        "old_tag_2": "new_tag_2",
        "old_tag_3": "new_tag_3",
    }
    deprecate_dict = {
        "old_tag_1": "42.0.0",
        "old_tag_2": "84.0.0",
        "old_tag_3": "126.0.0",
    }

    def __init__(self):
        super().__init__()


def _tag_deprecation_regex(old_tag, new_tag):
    """Generate a regex matching a deprecation warning for old_tag and new_tag."""
    return f"{re.escape(old_tag)}.*{re.escape(new_tag)}"


def test_tag_aliaser():
    """Tests the tag aliaser logic, as described in its docstring."""
    # case both new and old tags exist
    # old tag takes precedence
    with pytest.warns(
        FutureWarning, match=_tag_deprecation_regex("old_tag_1", "new_tag_1")
    ):
        new_tag_1_val = AliaserTestClass().get_tag("new_tag_1")
        assert new_tag_1_val == "old_tag_1_value"
        old_tag_1_val = AliaserTestClass().get_tag("old_tag_1")
        assert old_tag_1_val == "old_tag_1_value"

        new_tag_1_val = AliaserTestClass.get_class_tag("new_tag_1")
        assert new_tag_1_val == "old_tag_1_value"
        old_tag_1_val = AliaserTestClass.get_class_tag("old_tag_1")
        assert old_tag_1_val == "old_tag_1_value"

    # case only new tag exists
    with pytest.warns(
        FutureWarning, match=_tag_deprecation_regex("old_tag_2", "new_tag_2")
    ):
        new_tag_2_val = AliaserTestClass().get_tag("new_tag_2")
        assert new_tag_2_val == "new_tag_2_value"
        old_tag_2_val = AliaserTestClass().get_tag("old_tag_2")
        assert old_tag_2_val == "new_tag_2_value"

        new_tag_2_val = AliaserTestClass.get_class_tag("new_tag_2")
        assert new_tag_2_val == "new_tag_2_value"
        old_tag_2_val = AliaserTestClass.get_class_tag("old_tag_2")
        assert old_tag_2_val == "new_tag_2_value"

    # case only old tag exists
    with pytest.warns(
        FutureWarning, match=_tag_deprecation_regex("old_tag_3", "new_tag_3")
    ):
        new_tag_3_val = AliaserTestClass().get_tag("new_tag_3")
        assert new_tag_3_val == "old_tag_3_value"
        old_tag_3_val = AliaserTestClass().get_tag("old_tag_3")
        assert old_tag_3_val == "old_tag_3_value"

        new_tag_3_val = AliaserTestClass.get_class_tag("new_tag_3")
        assert new_tag_3_val == "old_tag_3_value"
        old_tag_3_val = AliaserTestClass.get_class_tag("old_tag_3")
        assert old_tag_3_val == "old_tag_3_value"

    # test all tags retrieval
    with pytest.warns(FutureWarning):
        all_tags = AliaserTestClass().get_tags()
        assert all_tags["new_tag_1"] == "old_tag_1_value"
        assert all_tags["old_tag_1"] == "old_tag_1_value"
        assert all_tags["new_tag_2"] == "new_tag_2_value"
        assert all_tags["old_tag_2"] == "new_tag_2_value"
        assert all_tags["new_tag_3"] == "old_tag_3_value"
        assert all_tags["old_tag_3"] == "old_tag_3_value"

        all_tags_cls = AliaserTestClass.get_class_tags()
        assert all_tags_cls["new_tag_1"] == "old_tag_1_value"
        assert all_tags_cls["old_tag_1"] == "old_tag_1_value"
        assert all_tags_cls["new_tag_2"] == "new_tag_2_value"
        assert all_tags_cls["old_tag_2"] == "new_tag_2_value"
        assert all_tags_cls["new_tag_3"] == "old_tag_3_value"
        assert all_tags_cls["old_tag_3"] == "old_tag_3_value"
