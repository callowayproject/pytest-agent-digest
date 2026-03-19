---
title: Options Reference
summary: Complete reference for all pytest-agent-digest command-line and ini options.
date: 2026-03-16T00:00:00.000000+00:00
---

Complete reference for every user-visible option provided by `pytest-agent-digest`.


## `--agent-digest`

**Type:** CLI flag (repeatable)

**Choices:** `term`, `file`

**Default:** *(not set — plugin is inactive)*

Activates the agent digest for the current session. Pass the flag once to enable a single output mode, or twice to enable both simultaneously.

`term`
:   Renders the Markdown digest to **stdout**. The built-in pytest terminal reporter is
    suppressed so only the Markdown output appears on the console.

`file`
:   Writes the Markdown digest to a file on disk (see [`--agent-digest-file`](#--agent-digest-file)
    for the output path). Normal pytest terminal output is preserved.

**Examples:**

```bash
# stdout only
pytest --agent-digest=term

# file only
pytest --agent-digest=file

# both at once (flag is repeatable)
pytest --agent-digest=term --agent-digest=file
```

!!! note
    When neither `term` nor `file` is passed, the plugin is registered but does nothing —
    normal pytest output is unaffected.


## `--agent-digest-file`

**Type:** CLI flag
**Default:** *(falls back to ini option or `test-results.md`)*

Overrides the output path for the Markdown file written by `--agent-digest=file`.

**Example:**

```bash
pytest --agent-digest=file --agent-digest-file=reports/results.md
```


## `agent_digest_file`

**Type:** ini option
**Default:** `test-results.md`

Sets the project-wide default output path for the Markdown digest file. Recognised in
`pytest.ini`, `pyproject.toml` (`[tool.pytest.ini_options]`), `setup.cfg`, and `tox.ini`.

**Example (`pyproject.toml`):**

```toml
[tool.pytest.ini_options]
agent_digest_file = "reports/ci-results.md"
```

**Example (`pytest.ini`):**

```ini
[pytest]
agent_digest_file = reports/ci-results.md
```

## Resolution order for the output path

When `--agent-digest=file` is active, the output path is resolved in this order:

1. `--agent-digest-file` CLI flag *(highest priority)*
2. `agent_digest_file` ini option
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
    Agent digest written to test-results.md
    ```

    Parent directories are created automatically if they do not exist.
