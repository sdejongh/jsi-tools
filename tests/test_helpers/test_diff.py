"""Tests for the diff helper."""

from __future__ import annotations

import pytest

from jsi_tools.helpers.diff import DictDiff, ListDiff, SetDiff, diff

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    def test_mismatched_types_list_set(self):
        with pytest.raises(TypeError, match="Cannot diff list with set"):
            diff([1], {1})

    def test_mismatched_types_set_frozenset(self):
        with pytest.raises(TypeError, match="Cannot diff set with frozenset"):
            diff({1}, frozenset({1}))

    def test_mismatched_types_list_dict(self):
        with pytest.raises(TypeError, match="Cannot diff list with dict"):
            diff([1], {"a": 1})

    def test_unsupported_type_tuple(self):
        with pytest.raises(TypeError, match="Convert to list"):
            diff((1, 2), (3, 4))

    def test_unsupported_type_string(self):
        with pytest.raises(TypeError, match="Unsupported type str"):
            diff("abc", "def")

    def test_unsupported_type_range(self):
        with pytest.raises(TypeError, match="Unsupported type range"):
            diff(range(3), range(5))

    def test_dict_vs_ordered_dict_rejected(self) -> None:
        from collections import OrderedDict
        with pytest.raises(TypeError, match="Cannot diff"):
            diff({"a": 1}, OrderedDict({"a": 1}))


# ---------------------------------------------------------------------------
# List diff
# ---------------------------------------------------------------------------


class TestListDiff:
    def test_identical_lists(self):
        result = diff([1, 2, 3], [1, 2, 3])
        assert sorted(result.added) == []
        assert sorted(result.removed) == []
        assert sorted(result.common) == [1, 2, 3]

    def test_completely_different(self):
        result = diff([1, 2], [3, 4])
        assert sorted(result.added) == [3, 4]
        assert sorted(result.removed) == [1, 2]
        assert sorted(result.common) == []

    def test_additions_only(self):
        result = diff([1, 2], [1, 2, 3])
        assert sorted(result.added) == [3]
        assert sorted(result.removed) == []
        assert sorted(result.common) == [1, 2]

    def test_removals_only(self):
        result = diff([1, 2, 3], [1, 2])
        assert sorted(result.added) == []
        assert sorted(result.removed) == [3]
        assert sorted(result.common) == [1, 2]

    def test_mixed_changes(self):
        result = diff([1, 2, 3], [2, 3, 4])
        assert sorted(result.added) == [4]
        assert sorted(result.removed) == [1]
        assert sorted(result.common) == [2, 3]

    def test_duplicates(self):
        result = diff([1, 1, 2], [1, 3])
        assert sorted(result.added) == [3]
        assert sorted(result.removed) == [1, 2]
        assert sorted(result.common) == [1]

    def test_both_empty(self):
        result = diff([], [])
        assert result.added == ()
        assert result.removed == ()
        assert result.common == ()

    def test_first_empty(self):
        result = diff([], [1, 2])
        assert sorted(result.added) == [1, 2]
        assert result.removed == ()
        assert result.common == ()

    def test_second_empty(self):
        result = diff([1, 2], [])
        assert result.added == ()
        assert sorted(result.removed) == [1, 2]
        assert result.common == ()

    def test_duplicates_symmetric(self) -> None:
        result = diff([1, 1, 1, 2, 2], [1, 1, 3, 3])
        assert sorted(result.added) == [3, 3]
        assert sorted(result.removed) == [1, 2, 2]
        assert sorted(result.common) == [1, 1]

    def test_all_same_element(self) -> None:
        result = diff([1, 1, 1], [1, 1, 1, 1, 1])
        assert sorted(result.added) == [1, 1]
        assert sorted(result.removed) == []
        assert sorted(result.common) == [1, 1, 1]

    def test_string_elements(self) -> None:
        result = diff(["a", "b", "c"], ["b", "c", "d"])
        assert sorted(result.added) == ["d"]
        assert sorted(result.removed) == ["a"]
        assert sorted(result.common) == ["b", "c"]

    def test_unhashable_items_raises(self):
        with pytest.raises(TypeError):
            diff([{"a": 1}], [{"a": 2}])


# ---------------------------------------------------------------------------
# Set diff
# ---------------------------------------------------------------------------


class TestSetDiff:
    def test_identical_sets(self):
        result = diff({1, 2, 3}, {1, 2, 3})
        assert result.added == frozenset()
        assert result.removed == frozenset()
        assert result.common == frozenset({1, 2, 3})

    def test_completely_different(self):
        result = diff({1, 2}, {3, 4})
        assert result.added == frozenset({3, 4})
        assert result.removed == frozenset({1, 2})
        assert result.common == frozenset()

    def test_additions_only(self):
        result = diff({1, 2}, {1, 2, 3})
        assert result.added == frozenset({3})
        assert result.removed == frozenset()
        assert result.common == frozenset({1, 2})

    def test_removals_only(self):
        result = diff({1, 2, 3}, {1})
        assert result.added == frozenset()
        assert result.removed == frozenset({2, 3})
        assert result.common == frozenset({1})

    def test_both_empty(self):
        result = diff(set(), set())
        assert result.added == frozenset()
        assert result.removed == frozenset()
        assert result.common == frozenset()

    def test_frozenset_identical(self):
        result = diff(frozenset({1, 2}), frozenset({1, 2}))
        assert result.added == frozenset()
        assert result.removed == frozenset()
        assert result.common == frozenset({1, 2})

    def test_frozenset_different(self):
        result = diff(frozenset({1, 2}), frozenset({2, 3}))
        assert result.added == frozenset({3})
        assert result.removed == frozenset({1})
        assert result.common == frozenset({2})

    def test_frozenset_both_empty(self) -> None:
        result = diff(frozenset(), frozenset())
        assert result.added == frozenset()
        assert result.removed == frozenset()
        assert result.common == frozenset()

    def test_result_fields_are_frozensets(self):
        result = diff({1, 2}, {2, 3})
        assert isinstance(result.added, frozenset)
        assert isinstance(result.removed, frozenset)
        assert isinstance(result.common, frozenset)


# ---------------------------------------------------------------------------
# Dict diff
# ---------------------------------------------------------------------------


class TestDictDiff:
    def test_identical_dicts(self):
        result = diff({"a": 1}, {"a": 1})
        assert result.added == {}
        assert result.removed == {}
        assert result.changed == {}
        assert result.unchanged == {"a": 1}

    def test_added_keys(self):
        result = diff({"a": 1}, {"a": 1, "b": 2})
        assert result.added == {"b": 2}
        assert result.removed == {}
        assert result.changed == {}
        assert result.unchanged == {"a": 1}

    def test_removed_keys(self):
        result = diff({"a": 1, "b": 2}, {"a": 1})
        assert result.added == {}
        assert result.removed == {"b": 2}
        assert result.changed == {}
        assert result.unchanged == {"a": 1}

    def test_changed_values(self):
        result = diff({"a": 1}, {"a": 2})
        assert result.added == {}
        assert result.removed == {}
        assert result.changed == {"a": (1, 2)}
        assert result.unchanged == {}

    def test_mixed_operations(self):
        result = diff({"a": 1, "b": 2, "c": 3}, {"b": 20, "c": 3, "d": 4})
        assert result.added == {"d": 4}
        assert result.removed == {"a": 1}
        assert result.changed == {"b": (2, 20)}
        assert result.unchanged == {"c": 3}

    def test_both_empty(self):
        result = diff({}, {})
        assert result.added == {}
        assert result.removed == {}
        assert result.changed == {}
        assert result.unchanged == {}

    def test_first_empty(self):
        result = diff({}, {"a": 1})
        assert result.added == {"a": 1}
        assert result.removed == {}
        assert result.changed == {}
        assert result.unchanged == {}

    def test_second_empty(self):
        result = diff({"a": 1}, {})
        assert result.added == {}
        assert result.removed == {"a": 1}
        assert result.changed == {}
        assert result.unchanged == {}

    def test_nested_dict_values(self):
        result = diff({"a": {"x": 1}}, {"a": {"x": 2}})
        assert result.changed == {"a": ({"x": 1}, {"x": 2})}
        assert result.unchanged == {}

    def test_value_type_change(self):
        result = diff({"a": 1}, {"a": "1"})
        assert result.changed == {"a": (1, "1")}
        assert result.unchanged == {}

    def test_large_mixed_dict(self) -> None:
        a = {f"k{i}": i for i in range(100)}
        b = {f"k{i}": i + 1 for i in range(50, 150)}
        result = diff(a, b)
        assert len(result.removed) == 50
        assert len(result.added) == 50
        assert len(result.changed) == 50
        assert len(result.unchanged) == 0

    def test_none_values(self) -> None:
        result = diff({"a": None, "b": 1}, {"a": None, "b": None})
        assert result.changed == {"b": (1, None)}
        assert result.unchanged == {"a": None}


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_list_diff_frozen(self):
        result = diff([1, 2], [2, 3])
        with pytest.raises(AttributeError):
            result.added = [99]  # type: ignore[misc]

    def test_set_diff_frozen(self):
        result = diff({1, 2}, {2, 3})
        with pytest.raises(AttributeError):
            result.added = frozenset({99})  # type: ignore[misc]

    def test_dict_diff_frozen(self):
        result = diff({"a": 1}, {"b": 2})
        with pytest.raises(AttributeError):
            result.added = {"z": 0}  # type: ignore[misc]

    def test_dict_diff_values_immutable(self) -> None:
        result = diff({"a": 1}, {"b": 2})
        with pytest.raises(TypeError):
            result.added["c"] = 3  # type: ignore[index]


# ---------------------------------------------------------------------------
# Return types
# ---------------------------------------------------------------------------


class TestReturnTypes:
    def test_list_returns_list_diff(self):
        result = diff([1, 2], [2, 3])
        assert isinstance(result, ListDiff)

    def test_set_returns_set_diff(self):
        result = diff({1, 2}, {2, 3})
        assert isinstance(result, SetDiff)

    def test_frozenset_returns_set_diff(self):
        result = diff(frozenset({1}), frozenset({2}))
        assert isinstance(result, SetDiff)

    def test_dict_returns_dict_diff(self):
        result = diff({"a": 1}, {"b": 2})
        assert isinstance(result, DictDiff)

    def test_ordered_dict_accepted(self) -> None:
        from collections import OrderedDict
        result = diff(OrderedDict({"a": 1}), OrderedDict({"b": 2}))
        assert isinstance(result, DictDiff)

    def test_list_diff_fields_are_tuples(self) -> None:
        result = diff([1, 2], [2, 3])
        assert isinstance(result.added, tuple)
        assert isinstance(result.removed, tuple)
        assert isinstance(result.common, tuple)

    def test_top_level_import(self) -> None:
        from jsi_tools import DictDiff as _DictDiff
        from jsi_tools import ListDiff as _ListDiff
        from jsi_tools import SetDiff as _SetDiff
        from jsi_tools import diff as _diff

        assert callable(_diff)
        assert _DictDiff is not None
        assert _ListDiff is not None
        assert _SetDiff is not None
