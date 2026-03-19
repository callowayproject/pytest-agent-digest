---
title: Quickstart
summary: Quickstart instructions for Pytest Agent Digest.
date: 2026-03-14T12:01:58.856377+00:00
---

Get up and running with `pytest-agent-digest` in minutes.

## Installation

=== "pip"

    ```bash
    pip install pytest-agent-digest
    ```

=== "uv"

    ```bash
    uv add pytest-agent-digest
    ```

No additional configuration is required — the plugin registers itself automatically via pytest's entry-point mechanism.

## Usage

### Print Markdown digest to stdout

```bash
pytest --agent-digest=term
```

This replaces the normal terminal output with a compact Markdown digest, ideal for piping directly into an AI agent prompt.

Expected output (abbreviated):

````markdown
8 passed, 2 failed, 1 skipped, 1 xfailed, 1 xpassed

## Failures

### `tests/test_math.py::test_divide_by_zero`

**Status:** FAILED
**Duration:** 0.50s

```
self = <tests.test_math.test_divide_by_zero object at 0x10b3f43e0>

    def test_divide_by_zero(self) -> None:
        """Example test showing how to divide by zero."""
>       1/0
E       ZeroDivisionError: division by zero

tests/test_math.py:78: ZeroDivisionError
```

...
````

### Write the Markdown digest to a file

```bash
pytest --agent-digest=file
```

Creates `test-results.md` in the current directory and prints a confirmation line:

```
Agent digest written to test-results.md
```

Normal pytest terminal output is preserved alongside the file write.

### Both at once

```bash
pytest --agent-digest=term --agent-digest=file
```

`--agent-digest` is a repeatable flag. Passing it twice activates both output modes simultaneously: the Markdown digest is written to stdout and to disk.

## Including passing tests

By default, the `## Passes` section is omitted. Pass `-v` to include it:

```bash
pytest -v --agent-digest=term
```

## Customising the output file path

Override the default `test-results.md` filename with the `--agent-digest-file` CLI flag:

```bash
pytest --agent-digest=file --agent-digest-file=reports/ci-results.md
```

Or set a project-wide default in `pytest.ini` / `pyproject.toml`:

```ini
# pytest.ini
[pytest]
agent_digest_file = reports/ci-results.md
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
agent_digest_file = "reports/ci-results.md"
```

The resolution order is: CLI flag > ini option > built-in default (`test-results.md`).

## Further reading

- [Options reference](reference/options.md) — full documentation of every option
