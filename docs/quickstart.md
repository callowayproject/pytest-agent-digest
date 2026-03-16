---
title: Quickstart
summary: Quickstart instructions for Pytest LLM Report.
date: 2026-03-14T12:01:58.856377+00:00
---

Get up and running with `pytest-llm-report` in minutes.

## Installation

=== "pip"

    ```bash
    pip install pytest-llm-report
    ```

=== "uv"

    ```bash
    uv add pytest-llm-report
    ```

No additional configuration is required — the plugin registers itself automatically via pytest's entry-point mechanism.

## Usage

### Print Markdown report to stdout

```bash
pytest --llm-report=term
```

This replaces the normal terminal output with a compact Markdown report, ideal for piping directly into an LLM prompt.

Expected output (abbreviated):

```markdown
# Test Results

**Status:** FAILED  **Tests:** 10  **Passed:** 8  **Failed:** 2  **Skipped:** 0

## Failures

### `tests/test_math.py::test_divide_by_zero`

```
FAILED tests/test_math.py::test_divide_by_zero
E   ZeroDivisionError: division by zero
```

...
```

### Write Markdown report to a file

```bash
pytest --llm-report=file
```

Creates `test-results.md` in the current directory and prints a confirmation line:

```
LLM report written to test-results.md
```

Normal pytest terminal output is preserved alongside the file write.

### Both at once

```bash
pytest --llm-report=term --llm-report=file
```

`--llm-report` is a repeatable flag. Passing it twice activates both output modes simultaneously: the Markdown report goes to stdout **and** is written to disk.

## Including passing tests

By default the `## Passes` section is omitted. Pass `-v` to include it:

```bash
pytest -v --llm-report=term
```

## Customising the output file path

Override the default `test-results.md` filename with the `--llm-report-file` CLI flag:

```bash
pytest --llm-report=file --llm-report-file=reports/ci-results.md
```

Or set a project-wide default in `pytest.ini` / `pyproject.toml`:

```ini
# pytest.ini
[pytest]
llm_report_file = reports/ci-results.md
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
llm_report_file = "reports/ci-results.md"
```

The resolution order is: CLI flag > ini option > built-in default (`test-results.md`).

## Further reading

- [Options reference](reference/options.md) — full documentation of every option
