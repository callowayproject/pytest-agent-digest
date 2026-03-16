---
title: Options Reference
summary: Complete reference for all pytest-llm-report command-line and ini options.
date: 2026-03-16T00:00:00.000000+00:00
---

Complete reference for every user-visible option provided by `pytest-llm-report`.

---

## `--llm-report`

**Type:** CLI flag (repeatable)

**Choices:** `term`, `file`

**Default:** *(not set — plugin is inactive)*

Activates the LLM report for the current session. Pass the flag once to enable a single output mode, or twice to enable both simultaneously.

`term`
:   Renders the Markdown report to **stdout**. The built-in pytest terminal reporter is
    suppressed so only the Markdown output appears on the console.

`file`
:   Writes the Markdown report to a file on disk (see [`--llm-report-file`](#--llm-report-file)
    for the output path). Normal pytest terminal output is preserved.

**Examples:**

```bash
# stdout only
pytest --llm-report=term

# file only
pytest --llm-report=file

# both at once (flag is repeatable)
pytest --llm-report=term --llm-report=file
```

!!! note
    When neither `term` nor `file` is passed, the plugin is registered but does nothing —
    normal pytest output is unaffected.

---

## `--llm-report-file`

**Type:** CLI flag
**Default:** *(falls back to ini option or `test-results.md`)*

Overrides the output path for the Markdown file written by `--llm-report=file`.

**Example:**

```bash
pytest --llm-report=file --llm-report-file=reports/results.md
```

---

## `llm_report_file`

**Type:** ini option
**Default:** `test-results.md`

Sets the project-wide default output path for the Markdown report file. Recognised in
`pytest.ini`, `pyproject.toml` (`[tool.pytest.ini_options]`), `setup.cfg`, and `tox.ini`.

**Example (`pyproject.toml`):**

```toml
[tool.pytest.ini_options]
llm_report_file = "reports/ci-results.md"
```

**Example (`pytest.ini`):**

```ini
[pytest]
llm_report_file = reports/ci-results.md
```

---

## Resolution order for the output path

When `--llm-report=file` is active, the output path is resolved in this order:

1. `--llm-report-file` CLI flag *(highest priority)*
2. `llm_report_file` ini option
3. Built-in default: `test-results.md` *(lowest priority)*

---

## Exit behaviour

`term`
:   Markdown is printed to stdout. No files are written. Exit code follows the normal
    pytest convention (0 = all passed, non-zero = failures/errors).

`file`
:   Markdown is written to the resolved output path. A confirmation line is printed to
    stdout:

    ```
    LLM report written to test-results.md
    ```

    Parent directories are created automatically if they do not exist.
