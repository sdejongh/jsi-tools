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

## Quick Reference

### Decorators

| Name | Description |
|------|-------------|
| [`@log_return`](#log_return) | Log a function's return value with type and size info |

### Helpers

| Name | Description |
|------|-------------|
| [`diff(a, b)`](#diff) | Compute a structured diff between two collections |

### Classes

*No classes yet.*

### Utils

*No utils yet.*

---

## Feature Documentation

### `log_return`

Logs the return value of a function with type and size information.
Zero side effects — the return value is never modified.
Supports sync/async functions, generators, and instance/static/class methods.

```python
from jsi_tools import log_return

@log_return
def get_users():
    return ["alice", "bob", "charlie"]

get_users()
# DEBUG — get_users returned list[len=3]: ['alice', 'bob', 'charlie']
```

Can also be called with arguments: `@log_return(level=logging.INFO, max_length=50)`.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `level` | `int` | `logging.DEBUG` | Log level |
| `logger` | `Logger \| None` | `None` | Custom logger (defaults to function's module logger) |
| `max_length` | `int \| None` | `None` | Truncate repr output |

**Log format:** `{qualname} returned {type_info}: {repr}` — where `type_info` includes `[len=N]` for sized types.

---

### `diff`

Computes a structured diff between two collections of the same type.
All results are immutable (frozen dataclasses with immutable field types).

```python
from jsi_tools import diff

result = diff({"a": 1, "b": 2, "c": 3}, {"b": 20, "c": 3, "d": 4})
result.added      # {"d": 4}
result.removed    # {"a": 1}
result.changed    # {"b": (2, 20)}
result.unchanged  # {"c": 3}
```

**Return types:**

| Input type | Return type | Fields |
|------------|-------------|--------|
| `list` | `ListDiff[T]` | `added`, `removed`, `common` (tuples) |
| `set` / `frozenset` | `SetDiff[T]` | `added`, `removed`, `common` (frozensets) |
| `dict` | `DictDiff[KT, VT]` | `added`, `removed`, `changed`, `unchanged` (read-only mappings) |

Raises `TypeError` if types differ, are unsupported, or are tuples (with a hint to convert to list).

---

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
