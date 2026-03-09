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

## Commands
- `ruff check src/ tests/` — lint
- `mypy src/` — type check (strict mode)
- `python -m pytest tests/ -v` — run tests

## Adding a New Element
1. Create file in appropriate submodule (e.g., `src/jsi_tools/decorators/new_thing.py`)
2. Export in submodule `__init__.py`
3. Export in top-level `__init__.py`
4. Write tests in `tests/test_<submodule>/test_new_thing.py`

## Gotchas
- Python 3.14: `asyncio.iscoroutinefunction` deprecated → use `inspect.iscoroutinefunction`
- hatchling build-backend is `hatchling.build` (NOT `hatchling.backends`)
- pytest-asyncio: `asyncio_mode = "auto"` — no need for `@pytest.mark.asyncio`
