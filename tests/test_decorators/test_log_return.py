"""Tests for the @log_return decorator."""

from __future__ import annotations

import inspect
import logging
from dataclasses import dataclass
from typing import NamedTuple

import pytest

from jsi_tools.decorators.log_return import log_return

# ---------------------------------------------------------------------------
# Primitive types
# ---------------------------------------------------------------------------


class TestPrimitiveTypes:
    def test_int(self, caplog):
        @log_return
        def f():
            return 42

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == 42
        assert "f returned int: 42" in caplog.text

    def test_float(self, caplog):
        @log_return
        def f():
            return 3.14

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == 3.14
        assert "f returned float: 3.14" in caplog.text

    def test_str(self, caplog):
        @log_return
        def f():
            return "hello"

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == "hello"
        assert "f returned str[len=5]: 'hello'" in caplog.text

    def test_bool(self, caplog):
        @log_return
        def f():
            return True

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result is True
        assert "f returned bool: True" in caplog.text

    def test_none(self, caplog):
        @log_return
        def f():
            return None

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result is None
        assert "f returned None: None" in caplog.text


# ---------------------------------------------------------------------------
# Collections
# ---------------------------------------------------------------------------


class TestCollections:
    def test_list(self, caplog):
        @log_return
        def f():
            return [1, 2, 3]

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == [1, 2, 3]
        assert "f returned list[len=3]: [1, 2, 3]" in caplog.text

    def test_dict(self, caplog):
        @log_return
        def f():
            return {"a": 1, "b": 2}

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == {"a": 1, "b": 2}
        assert "f returned dict[len=2]:" in caplog.text

    def test_tuple(self, caplog):
        @log_return
        def f():
            return (1, 2)

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == (1, 2)
        assert "f returned tuple[len=2]: (1, 2)" in caplog.text

    def test_set(self, caplog):
        @log_return
        def f():
            return {1}

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == {1}
        assert "f returned set[len=1]: {1}" in caplog.text

    def test_empty_list(self, caplog):
        @log_return
        def f():
            return []

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == []
        assert "f returned list[len=0]: []" in caplog.text


# ---------------------------------------------------------------------------
# Complex types
# ---------------------------------------------------------------------------


class TestComplexTypes:
    def test_dataclass(self, caplog):
        @dataclass
        class Point:
            x: int
            y: int

        @log_return
        def f():
            return Point(1, 2)

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == Point(1, 2)
        assert "f returned Point:" in caplog.text
        assert "Point(x=1, y=2)" in caplog.text

    def test_namedtuple(self, caplog):
        class Coord(NamedTuple):
            x: int
            y: int

        @log_return
        def f():
            return Coord(3, 4)

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == Coord(3, 4)
        assert "f returned Coord[len=2]:" in caplog.text

    def test_custom_len(self, caplog):
        class Bag:
            def __init__(self, n):
                self._n = n

            def __len__(self):
                return self._n

        @log_return
        def f():
            return Bag(5)

        with caplog.at_level(logging.DEBUG):
            f()

        assert "f returned Bag[len=5]:" in caplog.text

    def test_custom_len_type_error(self, caplog):
        class BadLen:
            def __len__(self):
                raise TypeError("no len")

        @log_return
        def f():
            return BadLen()

        with caplog.at_level(logging.DEBUG):
            f()

        assert "f returned BadLen:" in caplog.text
        assert "[len=" not in caplog.text


# ---------------------------------------------------------------------------
# Async functions
# ---------------------------------------------------------------------------


class TestAsync:
    async def test_async_simple(self, caplog):
        @log_return
        async def f():
            return 10

        with caplog.at_level(logging.DEBUG):
            result = await f()

        assert result == 10
        assert "f returned int: 10" in caplog.text

    async def test_async_with_level(self, caplog):
        @log_return(level=logging.INFO)
        async def f():
            return "async_val"

        with caplog.at_level(logging.INFO):
            result = await f()

        assert result == "async_val"
        assert "f returned str[len=9]: 'async_val'" in caplog.text


# ---------------------------------------------------------------------------
# Class methods
# ---------------------------------------------------------------------------


class TestClassMethods:
    def test_instance_method(self, caplog):
        class MyClass:
            @log_return
            def greet(self):
                return "hi"

        with caplog.at_level(logging.DEBUG):
            result = MyClass().greet()

        assert result == "hi"
        assert "MyClass.greet returned str[len=2]: 'hi'" in caplog.text

    def test_static_method(self, caplog):
        class MyClass:
            @staticmethod
            @log_return
            def compute():
                return 7

        with caplog.at_level(logging.DEBUG):
            result = MyClass.compute()

        assert result == 7
        assert "compute returned int: 7" in caplog.text

    def test_class_method(self, caplog):
        class MyClass:
            @classmethod
            @log_return
            def create(cls):
                return cls()

        with caplog.at_level(logging.DEBUG):
            result = MyClass.create()

        assert isinstance(result, MyClass)
        assert "create returned MyClass:" in caplog.text


# ---------------------------------------------------------------------------
# Log levels
# ---------------------------------------------------------------------------


class TestLogLevels:
    def test_default_debug(self, caplog):
        @log_return
        def f():
            return 1

        with caplog.at_level(logging.DEBUG):
            f()

        assert caplog.records[0].levelno == logging.DEBUG

    def test_info_level(self, caplog):
        @log_return(level=logging.INFO)
        def f():
            return 1

        with caplog.at_level(logging.DEBUG):
            f()

        assert caplog.records[0].levelno == logging.INFO

    def test_warning_level(self, caplog):
        @log_return(level=logging.WARNING)
        def f():
            return 1

        with caplog.at_level(logging.DEBUG):
            f()

        assert caplog.records[0].levelno == logging.WARNING


# ---------------------------------------------------------------------------
# No side effect
# ---------------------------------------------------------------------------


class TestNoSideEffect:
    def test_same_object_returned(self):
        sentinel = [1, 2, 3]

        @log_return
        def f():
            return sentinel

        result = f()
        assert result is sentinel

    def test_same_object_dict(self):
        sentinel = {"key": "value"}

        @log_return
        def f():
            return sentinel

        result = f()
        assert result is sentinel


# ---------------------------------------------------------------------------
# Signature preservation
# ---------------------------------------------------------------------------


class TestSignaturePreservation:
    def test_name_and_doc_preserved(self):
        @log_return
        def my_function():
            """My docstring."""

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."
        assert my_function.__module__ == __name__

    def test_inspect_signature_preserved(self):
        @log_return
        def my_function(a: int, b: str = "x") -> bool:
            pass

        sig = inspect.signature(my_function)
        params = list(sig.parameters)
        assert params == ["a", "b"]
        assert sig.parameters["b"].default == "x"

    def test_signature_with_parentheses(self):
        @log_return(level=logging.INFO)
        def my_function(x, y, z=10):
            pass

        sig = inspect.signature(my_function)
        assert list(sig.parameters) == ["x", "y", "z"]


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------


class TestGenerators:
    def test_generator_logged_and_iterable(self, caplog):
        @log_return
        def gen():
            yield 1
            yield 2
            yield 3

        with caplog.at_level(logging.DEBUG):
            g = gen()

        assert "gen returned generator:" in caplog.text
        assert list(g) == [1, 2, 3]


# ---------------------------------------------------------------------------
# max_length
# ---------------------------------------------------------------------------


class TestMaxLength:
    def test_truncation(self, caplog):
        @log_return(max_length=10)
        def f():
            return "a" * 100

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == "a" * 100
        assert "..." in caplog.text
        assert repr("a" * 100) not in caplog.text

    def test_max_length_very_small(self, caplog):
        @log_return(max_length=3)
        def f():
            return "abcdefgh"

        with caplog.at_level(logging.DEBUG):
            result = f()

        assert result == "abcdefgh"
        # Verify repr is truncated and not longer than max_length
        log_msg = caplog.records[0].message
        # The value part after ": " should be at most 3 chars
        value_part = log_msg.split(": ", 1)[1]
        assert len(value_part) <= 3

    def test_no_truncation_when_short(self, caplog):
        @log_return(max_length=100)
        def f():
            return "hi"

        with caplog.at_level(logging.DEBUG):
            f()

        assert "'hi'" in caplog.text
        assert "..." not in caplog.text


# ---------------------------------------------------------------------------
# Custom logger
# ---------------------------------------------------------------------------


class TestCustomLogger:
    def test_custom_logger_receives_log(self, caplog):
        custom_logger = logging.getLogger("my.custom.logger")

        @log_return(logger=custom_logger)
        def f():
            return 42

        with caplog.at_level(logging.DEBUG, logger="my.custom.logger"):
            f()

        assert any(r.name == "my.custom.logger" for r in caplog.records)
        assert "f returned int: 42" in caplog.text

    def test_default_logger_uses_module(self, caplog):
        @log_return
        def f():
            return 1

        with caplog.at_level(logging.DEBUG):
            f()

        assert caplog.records[0].name == __name__


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_exception_propagates(self):
        @log_return
        def f():
            raise ValueError("boom")

        with pytest.raises(ValueError, match="boom"):
            f()

    async def test_async_exception_propagates(self):
        @log_return
        async def f():
            raise RuntimeError("async boom")

        with pytest.raises(RuntimeError, match="async boom"):
            await f()
