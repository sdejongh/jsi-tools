# jsi-tools

## Project
- Python utility library (decorators, helpers, classes, utils)
- Build: hatchling (`hatchling.build`), src-layout (`src/jsi_tools/`)
- License: GPL-3.0-only
- Python: >=3.10

## Environment
- Always use venv: `source .venv/bin/activate`
- Install dev: `pip install -e ".[dev]"`

## Code Style
- Docstrings: Google format (Args:, Returns:, Raises:)
- No overengineering — keep it simple and pragmatic
- One primary element per file (e.g., `log_return.py`)
- Eager re-exports with `__all__` at every level
- `from __future__ import annotations` in all modules
- Runtime-only imports at top; typing imports in `TYPE_CHECKING` block
- Immutable results: `tuple[T, ...]` for sequences, `frozenset` for sets, `MappingProxyType` for dicts

## Commands
- `ruff check src/ tests/` — lint
- `mypy src/` — type check (strict mode)
- `python -m pytest tests/ -v` — run tests

## Before Committing / Pushing
- Always update `README.md` and `CHANGELOG.md` before committing or pushing

## Releasing
- Version is defined in TWO places: `pyproject.toml` and `src/jsi_tools/__init__.py` — update both
- Tag format: `v0.X.0` — pushing a tag triggers `.github/workflows/release.yml` (build + PyPI publish)
- After push: purge GitHub camo cache if badges are stale (`curl -X PURGE <camo-url>`)

## Adding a New Element
1. Create file in appropriate submodule (e.g., `src/jsi_tools/decorators/new_thing.py`)
2. Export in submodule `__init__.py`
3. Export in top-level `__init__.py`
4. Write tests in `tests/test_<submodule>/test_new_thing.py`

## Gotchas
- Python 3.14: `asyncio.iscoroutinefunction` deprecated → use `inspect.iscoroutinefunction`
- hatchling build-backend is `hatchling.build` (NOT `hatchling.backends`)
- pytest-asyncio: `asyncio_mode = "auto"` — no need for `@pytest.mark.asyncio`
- `@dataclass(slots=True)` requires Python 3.11+ — do NOT use (project targets >=3.10)
- ruff I001: local imports with `as` alias must be one-per-line, not combined
