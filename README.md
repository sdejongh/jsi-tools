# jsi-tools

[![CI](https://github.com/sdejongh/jsi-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/sdejongh/jsi-tools/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/jsi-tools)](https://pypi.org/project/jsi-tools/)
[![Python](https://img.shields.io/pypi/pyversions/jsi-tools)](https://pypi.org/project/jsi-tools/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Personal Python utility library — decorators, helpers, classes, and utils.

## Installation

```bash
pip install jsi-tools
```

## Decorators

### `@log_return`

Logs the return value of a function with type and size information. Zero side effects — the return value is never modified.

```python
import logging
from jsi_tools import log_return

@log_return
def get_users():
    return ["alice", "bob", "charlie"]

get_users()
# DEBUG — get_users returned list[len=3]: ['alice', 'bob', 'charlie']
```

Works with or without arguments:

```python
@log_return(level=logging.INFO, max_length=50)
def fetch_config():
    return {"host": "localhost", "port": 8080, "debug": True}

fetch_config()
# INFO — fetch_config returned dict[len=3]: {'host': 'localhost', 'port': 8080, ...
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `level` | `int` | `logging.DEBUG` | Log level |
| `logger` | `Logger \| None` | `None` | Custom logger (defaults to function's module logger) |
| `max_length` | `int \| None` | `None` | Truncate repr output |

**Supports:** sync functions, async functions, generators, instance/static/class methods, all Python types.

**Log format:** `{qualname} returned {type}[len={n}]: {repr}`

Type info examples:

| Return value | Type info |
|---|---|
| `42` | `int` |
| `"hello"` | `str[len=5]` |
| `[1, 2, 3]` | `list[len=3]` |
| `{"a": 1}` | `dict[len=1]` |
| `None` | `None` |
| `(generator)` | `generator` |

## Helpers

### `diff`

Computes a structured diff between two collections of the same type. Supports lists, sets, frozensets, and dicts. Returns an immutable result object.

```python
from jsi_tools import diff

# Lists — multiset semantics
result = diff([1, 2, 2, 3], [2, 3, 4, 4])
result.added    # (4, 4)
result.removed  # (1, 2)
result.common   # (2, 3)

# Sets
result = diff({"a", "b", "c"}, {"b", "c", "d"})
result.added    # frozenset({"d"})
result.removed  # frozenset({"a"})
result.common   # frozenset({"b", "c"})

# Dicts — tracks added, removed, changed, and unchanged keys
result = diff({"a": 1, "b": 2, "c": 3}, {"b": 20, "c": 3, "d": 4})
result.added     # {"d": 4}
result.removed   # {"a": 1}
result.changed   # {"b": (2, 20)}
result.unchanged # {"c": 3}
```

**Return types:**

| Input type | Return type | Fields |
|---|---|---|
| `list` | `ListDiff[T]` | `added`, `removed`, `common` (tuples) |
| `set` / `frozenset` | `SetDiff[T]` | `added`, `removed`, `common` (frozensets) |
| `dict` | `DictDiff[KT, VT]` | `added`, `removed`, `changed`, `unchanged` (read-only mappings) |

All results are immutable (`frozen` dataclasses with immutable field types).

Raises `TypeError` if types differ, are unsupported, or are tuples (with a hint to convert to list).

## Development

```bash
git clone https://github.com/sdejongh/jsi-tools.git
cd jsi-tools
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

```bash
pytest tests/ -v       # tests
ruff check src/ tests/ # lint
mypy src/              # type check
```

## License

[GPL-3.0](LICENSE)
