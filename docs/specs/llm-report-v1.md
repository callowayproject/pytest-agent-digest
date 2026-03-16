# Token-Efficient Markdown Test Reports

## Problem Statement

LLM-based TDD agents running pytest receive console output filled with ANSI escape codes, Unicode symbols, decorative separators, and verbose formatting optimized for human terminal readability — not token efficiency. This forces agents to spend unnecessary tokens parsing noise, increases API costs, and reduces the signal-to-noise ratio for agents trying to act on test results. There is no standard way to get structured, LLM-optimized test output from pytest without writing custom reporters from scratch.

## Goals

1. Reduce token consumption of pytest output for LLM agents by eliminating ANSI codes, Unicode symbols, and decorative formatting.
2. Enable agents to receive test results as clean Markdown via terminal output (replacing default console output) or as a written `.md` file.
3. Support both output modes simultaneously so agents and developers can use the tool together.
4. Integrate with pytest's existing flag conventions (`-v`, `--tb`) so no new mental model is required.
5. Provide a zero-config path to useful output with sensible defaults (default filename, default traceback style).

## Non-Goals

- **HTML or JSON report formats** — other plugins (pytest-html, pytest-json-report) serve this need; this plugin focuses exclusively on Markdown.
- **Custom test runners or test collection changes** — this plugin only affects output, not how tests are discovered or executed.
- **Real-time streaming output** — reports are assembled at session end, not streamed incrementally during the run.
- **LLM API integration** — the plugin produces Markdown for agents to consume; it does not call any LLM API itself.
- **Replacing pytest-cov or other reporting plugins** — coverage and other metrics are out of scope for v1.

## User Stories

### LLM TDD Agent

- As an LLM TDD agent, I want pytest output in Markdown format so that I can parse test results without wasting tokens on ANSI codes and decorative formatting.
- As an LLM TDD agent, I want failures surfaced first with short tracebacks so that I can identify what to fix without reading through passing tests.
- As an LLM TDD agent, I want a summary line with counts for passed, failed, skipped, and xfail so that I can assess overall test health in a single line.
- As an LLM TDD agent reading a file, I want the report written to a predictable path so that I can read it after the test run without parsing stdout.

### Developer / Human Using the Plugin

- As a developer, I want to pass `--llm-report=file` to write a Markdown report without losing normal console output so that I can inspect what an agent will receive while still seeing my usual test feedback.
- As a developer, I want to pass `--llm-report=term` to replace console output with Markdown so that I can verify the report format looks correct.
- As a developer, I want to use both `--llm-report=term` and `--llm-report=file` in the same run so that I can see the Markdown output and capture it.
- As a developer, I want to configure the output filename in `pyproject.toml` so that I don't have to pass it on every invocation.
- As a developer, I want the plugin to respect `-v` and `--tb` flags so that I don't need to learn a new set of options.

## Requirements

### Must-Have (P0)

**`--llm-report` CLI flag accepting `term` and/or `file` values**
- `--llm-report=term`: replaces pytest's default terminal output with Markdown-formatted output
- `--llm-report=file`: writes Markdown report to a file; default console output is unaffected
- Both flags may be used in the same invocation: `--llm-report=term --llm-report=file`
- Acceptance criteria:
  - Given `--llm-report=term`, when the test session ends, the terminal shows Markdown output and no default pytest console output
  - Given `--llm-report=file`, when the test session ends, a `.md` file is written and the default pytest console output is unchanged
  - Given both flags, both behaviors occur

**Token-efficient Markdown formatting**
- No ANSI escape codes in any output
- Status labels use text: `PASSED`, `FAILED`, `SKIPPED`, `XFAIL`, `XPASS` — no Unicode symbols
- Metadata fields formatted as `**Label:**` (colon inside bold)
- Summary counts separated by `, ` (comma-space)
- `xfail` shown as its own count, separate from `skipped`
- Acceptance criteria:
  - Given any output mode, the Markdown output contains no ANSI sequences
  - Given a test summary, xfail count is distinct from skipped count

**Report section structure**
- `## Failures` — appears first; contains `FAILED`, `XFAIL`, and `XPASS` results
- `## Skipped` — contains tests marked skip or conditionally skipped
- `## Passes` — only present when `-v` flag is active
- Each failure entry includes: test node ID, short traceback (default `--tb=short`), and failure reason
- Acceptance criteria:
  - Given failures exist, `## Failures` is the first section
  - Given `-v` is not set, `## Passes` section is omitted
  - Given `-v` is set, `## Passes` section lists all passing test node IDs

**Summary line**
- Session summary formatted as: `X passed, X failed, X skipped, X xfailed` (omit zero-count categories)
- Acceptance criteria:
  - Given 3 passed and 1 failed with no skipped or xfail, summary reads `3 passed, 1 failed`

**Default filename**
- When `--llm-report=file` is used without `--llm-report-file`, output file is `test-results.md` in the current working directory
- Acceptance criteria:
  - Given `--llm-report=file` with no filename option, `test-results.md` is created in cwd

**`--llm-report-file` CLI option and `llm_report_file` ini option**
- Sets the path/name of the output file
- Configurable in `pyproject.toml` under `[tool.pytest.ini_options]`
- Acceptance criteria:
  - Given `--llm-report-file=output/results.md`, the report is written to that path
  - Given `llm_report_file = "output/results.md"` in `pyproject.toml`, the report is written to that path without a CLI flag

**Respect `-v` and `--tb` flags**
- `-v` controls whether the `## Passes` section appears
- `--tb=short` is the effective default for report tracebacks; `--tb=line`, `--tb=long`, `--tb=no` all work as expected
- Acceptance criteria:
  - Given `--tb=no`, failure entries contain no traceback
  - Given `--tb=long`, failure entries contain the full traceback
  - Given `-v`, passes section is included in the report

### Nice-to-Have (P1)

**Duration metadata per test**
- Include elapsed time for each test entry (especially failures) to help agents identify slow tests
- Format: `**Duration:** 0.42s`

**`--llm-report=both` shorthand**
- Single value that activates both `term` and `file` modes without requiring two flags

**Warning section**
- `## Warnings` section capturing pytest warnings for agent visibility

**Configurable section inclusion**
- `llm_report_sections` ini option to control which sections appear (e.g., exclude passes even with `-v`)

### Future Considerations (P2)

- **Machine-readable frontmatter**: YAML frontmatter block at top of file with structured summary metadata (total, passed, failed, duration) for agents that parse frontmatter
- **Per-test metadata**: capture markers, parametrize IDs, and custom metadata attached via `pytest.mark`
- **Multi-run diffing**: compare current report against a previous run and surface regressions

## Success Metrics

**Leading indicators** (days to weeks post-launch):

| Metric | Target | Method |
|--------|--------|--------|
| Plugin installs | 100 installs within 30 days of first PyPI release | PyPI download stats |
| CI passes on plugin's own test suite | 100% | GitHub Actions |
| Zero open P0 bugs at launch | 0 critical issues | GitHub Issues |

**Lagging indicators** (weeks to months):

| Metric | Target | Method |
|--------|--------|--------|
| GitHub stars | 50 within 90 days | GitHub |
| Reported token reduction | ≥20% fewer tokens vs. raw pytest output on a representative test suite | Manual benchmark using `claudeutils tokens` |
| User-reported issues citing format regression | 0 in first 60 days | GitHub Issues |

## Open Questions

| Question | Owner | Blocking? |
|----------|-------|-----------|
| Should `--llm-report=term` suppress all pytest plugins' terminal output (e.g., pytest-cov summary), or only pytest's own reporter? | Engineering | Yes — affects plugin hook implementation |
| When both `term` and `file` are active, are they guaranteed to produce identical content, or can they differ (e.g., file gets more detail)? | Product | No — can decide during implementation |
| Should the output file be overwritten on each run, or appended? | Product | No — default to overwrite; append can be P1 |
| Does `--llm-report=term` need to print anything for a completely empty test session (no tests collected)? | Engineering | No |

## Timeline Considerations

- No hard deadlines identified
- Suggested phase 1 scope: all P0 requirements — CLI flags, Markdown formatting, section structure, file output, ini config
- P1 features (duration, `both` shorthand, warnings section) deferred to a follow-up release after real-world agent feedback
- The plugin is currently in scaffold phase; the entry point in `pyproject.toml` needs to be registered before any plugin hooks will fire
