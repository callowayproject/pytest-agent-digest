# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`pytest-llm-report` is a pytest plugin (in early development) that generates Markdown reports for AI agents. The plugin hooks into pytest to capture test results and produce structured Markdown output suitable for LLM consumption.

## Package Manager

Use `uv` for all dependency management. Install all dependency groups with:
```
uv sync
```

## Commands

### Testing
```bash
uv run pytest                          # Run all tests with coverage
uv run pytest tests/test_foo.py        # Run a single test file
uv run pytest tests/test_foo.py::test_bar  # Run a single test
uv run pytest -x                       # Stop on first failure
```

### Linting & Formatting
```bash
uv run ruff check .                    # Lint
uv run ruff check --fix .              # Lint with auto-fix
uv run ruff format .                   # Format code
uv run mypy pytest_llm_report/         # Type checking
uv run interrogate pytest_llm_report/  # Check docstring coverage (must be ≥90%)
```

### Pre-commit Hooks
```bash
uv run pre-commit install              # Install hooks (run once after setup)
uv run pre-commit run --all-files      # Run all hooks manually
```

### Documentation
```bash
uv run mkdocs serve                    # Serve docs locally
uv run mkdocs build                    # Build docs
```

### Versioning
```bash
uv run bump-my-version bump patch      # Bump patch version
uv run bump-my-version bump minor      # Bump minor version
```

## Code Style

- **Line length:** 119 characters
- **Docstrings:** Google style (enforced by ruff `D` rules and pydoclint)
- **Docstring coverage:** ≥90% required (interrogate)
- **Type annotations:** Required on all public functions (ANN rules enabled)
- Tests are in `tests/` and are exempt from annotation and some complexity rules

## Architecture

The plugin is in early scaffold phase. The intended architecture for a pytest plugin:

- **`pytest_llm_report/__init__.py`** — Package version; pytest plugin entry point will be registered via `project.entry-points."pytest11"` in `pyproject.toml` when implemented
- Plugin hooks (`pytest_configure`, `pytest_runtest_logreport`, `pytest_sessionfinish`, etc.) should be implemented here or in a dedicated `plugin.py` module
- The plugin captures test outcomes, metadata, and generates a Markdown report at session end

## Version Management

Version is stored in `pytest_llm_report/__init__.py` as `__version__` and managed by `bump-my-version`. The `CHANGELOG.md` is updated automatically during version bumps.
