"""Structured diff for lists, sets, frozensets, and dicts."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Generic, TypeVar, overload

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = ["DictDiff", "ListDiff", "SetDiff", "diff"]

T = TypeVar("T")
KT = TypeVar("KT")
VT = TypeVar("VT")

_SUPPORTED_TYPES = (list, set, frozenset, dict)


@dataclass(frozen=True)
class ListDiff(Generic[T]):
    """Result of diffing two lists using multiset semantics.

    Attributes:
        added: Elements present in the second list but not the first.
        removed: Elements present in the first list but not the second.
        common: Elements present in both lists.
    """

    added: tuple[T, ...]
    removed: tuple[T, ...]
    common: tuple[T, ...]


@dataclass(frozen=True)
class SetDiff(Generic[T]):
    """Result of diffing two sets or frozensets.

    Attributes:
        added: Elements present in the second set but not the first.
        removed: Elements present in the first set but not the second.
        common: Elements present in both sets.
    """

    added: frozenset[T]
    removed: frozenset[T]
    common: frozenset[T]


@dataclass(frozen=True)
class DictDiff(Generic[KT, VT]):
    """Result of diffing two dicts by key.

    Attributes:
        added: Read-only mapping of key-value pairs present only in the second dict.
        removed: Read-only mapping of key-value pairs present only in the first dict.
        changed: Read-only mapping of keys present in both dicts whose values differ.
            Maps each key to a ``(old, new)`` tuple.
        unchanged: Read-only mapping of key-value pairs identical in both dicts.
    """

    added: Mapping[KT, VT]
    removed: Mapping[KT, VT]
    changed: Mapping[KT, tuple[VT, VT]]
    unchanged: Mapping[KT, VT]


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _diff_lists(a: list[T], b: list[T]) -> ListDiff[T]:
    """Diff two lists using multiset (Counter) semantics."""
    counter_a = Counter(a)
    counter_b = Counter(b)

    common_counter = counter_a & counter_b
    added_counter = counter_b - counter_a
    removed_counter = counter_a - counter_b

    return ListDiff(
        added=tuple(added_counter.elements()),
        removed=tuple(removed_counter.elements()),
        common=tuple(common_counter.elements()),
    )


def _diff_sets(a: set[T] | frozenset[T], b: set[T] | frozenset[T]) -> SetDiff[T]:
    """Diff two sets or frozensets using set operations."""
    return SetDiff(
        added=frozenset(b - a),
        removed=frozenset(a - b),
        common=frozenset(a & b),
    )


def _diff_dicts(a: dict[KT, VT], b: dict[KT, VT]) -> DictDiff[KT, VT]:
    """Diff two dicts by comparing keys and values."""
    keys_a = set(a.keys())
    keys_b = set(b.keys())

    added_keys = keys_b - keys_a
    removed_keys = keys_a - keys_b

    changed: dict[KT, tuple[VT, VT]] = {}
    unchanged: dict[KT, VT] = {}
    for k in keys_a & keys_b:
        if a[k] == b[k]:
            unchanged[k] = a[k]
        else:
            changed[k] = (a[k], b[k])

    return DictDiff(
        added=MappingProxyType({k: b[k] for k in added_keys}),
        removed=MappingProxyType({k: a[k] for k in removed_keys}),
        changed=MappingProxyType(changed),
        unchanged=MappingProxyType(unchanged),
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


@overload
def diff(a: list[T], b: list[T]) -> ListDiff[T]: ...


@overload
def diff(a: set[T], b: set[T]) -> SetDiff[T]: ...


@overload
def diff(a: frozenset[T], b: frozenset[T]) -> SetDiff[T]: ...


@overload
def diff(a: dict[KT, VT], b: dict[KT, VT]) -> DictDiff[KT, VT]: ...


def diff(
    a: list[T] | set[T] | frozenset[T] | dict[KT, VT],
    b: list[T] | set[T] | frozenset[T] | dict[KT, VT],
) -> ListDiff[T] | SetDiff[T] | DictDiff[KT, VT]:
    """Compute a structured diff between two collections of the same type.

    Args:
        a: The first collection (list, set, frozenset, or dict).
        b: The second collection. Must be the same type as *a*.

    Returns:
        A ``ListDiff``, ``SetDiff``, or ``DictDiff`` describing the
        differences between *a* and *b*.

    Raises:
        TypeError: If *a* and *b* are different types, if tuples are
            passed, or if the type is not supported.
    """
    if type(a) is not type(b):
        msg = f"Cannot diff {type(a).__name__} with {type(b).__name__}: both arguments must be the same type"
        raise TypeError(msg)

    if isinstance(a, tuple):
        msg = "Tuples are not supported by diff. Convert to list first: diff(list(a), list(b))"
        raise TypeError(msg)

    if not isinstance(a, _SUPPORTED_TYPES):
        msg = f"Unsupported type {type(a).__name__}: diff supports list, set, frozenset, and dict"
        raise TypeError(msg)

    if isinstance(a, list):
        return _diff_lists(a, b)  # type: ignore[arg-type]
    if isinstance(a, (set, frozenset)):
        return _diff_sets(a, b)  # type: ignore[arg-type]
    return _diff_dicts(a, b)  # type: ignore[arg-type]
