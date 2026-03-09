# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-03-09

### Added
- `diff(a, b)` — structured diff for lists, sets, frozensets, and dicts
- `ListDiff[T]` — immutable diff result for lists (multiset semantics via `Counter`)
- `SetDiff[T]` — immutable diff result for sets and frozensets
- `DictDiff[KT, VT]` — immutable diff result for dicts (added, removed, changed, unchanged)
- Type-safe `@overload` signatures: return type narrows based on input type
- Validation: same-type enforcement, tuple rejection with helpful message, unsupported type errors
- 52 tests covering all types, edge cases, immutability, and import paths

### Fixed
- Added missing `from __future__ import annotations` in `__init__.py` files

## [0.1.0] - 2025-05-01

### Added
- Initial release
- `@log_return` decorator — logs function return values with type info
- Support for sync/async functions, generators, class methods
- Configurable log level, logger, and max repr length
- Project scaffolding: hatchling build, ruff, mypy strict, pytest-asyncio
- CI/CD workflows
