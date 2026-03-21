# Changelog

## 0.2.0 (2026-03-21)

[Compare the full difference.](https://github.com/callowayproject/pytest-agent-digest/compare/0.1.0...0.2.0)

### Fixes

- Fix linting errors. [711d308](https://github.com/callowayproject/pytest-agent-digest/commit/711d308f647ffe69e2d562878490f2c7c5fab420)

- Fix 8 code quality and latent bug issues identified in code roast. [b85aa81](https://github.com/callowayproject/pytest-agent-digest/commit/b85aa81e84ea8c35b46f1ded9fb645ae47b2e473)

  - Strip ANSI from skip_reason in \_extract_skip_reason (bug fix)
  - Deduplicate pytest_sessionfinish: shared setup, branch only on destination
  - Pass verbose as int instead of bool to render_report
  - Remove empty pytest_runtest_logreport module-level stub
  - Use sys.executable instead of hardcoded "python" in benchmark
  - Update benchmark model to claude-haiku-4-5-20251001
  - Replace manual counts loop with collections.Counter
  - Remove defensive len-check on skip longrepr tuple (trust the contract)

  **co-authored-by:** Claude Sonnet 4.6 <noreply@anthropic.com>

### New

- Add token benchmarking script and integrate Anthropic API. [04bd2b1](https://github.com/callowayproject/pytest-agent-digest/commit/04bd2b107513949dc13fac5c22d0dc15fb418d39)

  - Introduce `benchmark_tokens.py` for comparing token counts between raw pytest output and LLM reports.
  - Use Anthropic API for token counting to validate a core success metric: ≥20% token reduction.
  - Add unit tests for benchmarking functionality, API integration, and output comparison.
  - Update `uv.lock` to include `anthropic` dependency.
  - Generate and restructure documentation using `gen_doc_stubs.py`.
  - Refactor existing files for improved organization: move docs structure to `docs/reference/api`.
  - Add `zensical.toml` for streamlined configuration of Markdown rendering and documentation features.

- Add CLAUDE.md for development guidelines and lockfile for dependency management. [0c6725b](https://github.com/callowayproject/pytest-agent-digest/commit/0c6725bb7760f1b8ed5d1131293cdda79caf0f18)

### Other

- Bump the github-actions group with 9 updates. [6b54c69](https://github.com/callowayproject/pytest-agent-digest/commit/6b54c692ce78ecfde14cc2759cb32448508dfa5e)

  Bumps the github-actions group with 9 updates:

  | Package | From | To |
  | --- | --- | --- |
  | [actions/checkout](https://github.com/actions/checkout) | `4` | `6` |
  | [actions/download-artifact](https://github.com/actions/download-artifact) | `4` | `8` |
  | [actions/setup-python](https://github.com/actions/setup-python) | `5` | `6` |
  | [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv) | `5` | `7` |
  | [github/codeql-action](https://github.com/github/codeql-action) | `3` | `4` |
  | [docker/login-action](https://github.com/docker/login-action) | `3` | `4` |
  | [docker/metadata-action](https://github.com/docker/metadata-action) | `5` | `6` |
  | [docker/build-push-action](https://github.com/docker/build-push-action) | `6` | `7` |
  | [actions/attest-build-provenance](https://github.com/actions/attest-build-provenance) | `2` | `4` |

  Updates `actions/checkout` from 4 to 6

  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v4...v6)

  Updates `actions/download-artifact` from 4 to 8

  - [Release notes](https://github.com/actions/download-artifact/releases)
  - [Commits](https://github.com/actions/download-artifact/compare/v4...v8)

  Updates `actions/setup-python` from 5 to 6

  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v5...v6)

  Updates `astral-sh/setup-uv` from 5 to 7

  - [Release notes](https://github.com/astral-sh/setup-uv/releases)
  - [Commits](https://github.com/astral-sh/setup-uv/compare/v5...v7)

  Updates `github/codeql-action` from 3 to 4

  - [Release notes](https://github.com/github/codeql-action/releases)
  - [Changelog](https://github.com/github/codeql-action/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/github/codeql-action/compare/v3...v4)

  Updates `docker/login-action` from 3 to 4

  - [Release notes](https://github.com/docker/login-action/releases)
  - [Commits](https://github.com/docker/login-action/compare/v3...v4)

  Updates `docker/metadata-action` from 5 to 6

  - [Release notes](https://github.com/docker/metadata-action/releases)
  - [Commits](https://github.com/docker/metadata-action/compare/v5...v6)

  Updates `docker/build-push-action` from 6 to 7

  - [Release notes](https://github.com/docker/build-push-action/releases)
  - [Commits](https://github.com/docker/build-push-action/compare/v6...v7)

  Updates `actions/attest-build-provenance` from 2 to 4

  - [Release notes](https://github.com/actions/attest-build-provenance/releases)
  - [Changelog](https://github.com/actions/attest-build-provenance/blob/main/RELEASE.md)
  - [Commits](https://github.com/actions/attest-build-provenance/compare/v2...v4)

  ______________________________________________________________________

  **updated-dependencies:** - dependency-name: actions/checkout
  dependency-version: '6'
  dependency-type: direct:production
  update-type: version-update:semver-major
  dependency-group: github-actions

  **signed-off-by:** dependabot[bot] <support@github.com>

- Handle missing outcome in renderer by falling back to uppercase string of the outcome. [210a2aa](https://github.com/callowayproject/pytest-agent-digest/commit/210a2aa619c9713cfc4a615dd37fdde2aa9ced69)

- Migrate `pytest_llm_report` to `pytest_agent_digest`, renaming all modules, classes, and references accordingly. Remove unfinished doc stubs and update package metadata (`__init__.py`) for new plugin. [e2f95c8](https://github.com/callowayproject/pytest-agent-digest/commit/e2f95c85cdc1481751f1de3cf037f9885cac3c91)

- Implement Ticket 7: add integration tests and skipped test handling. [a776968](https://github.com/callowayproject/pytest-agent-digest/commit/a7769686b200e224faf73b3864f72d8c4351fdfb)

  - Add four new integration tests to validate `--llm-report` behavior under various scenarios: mixed outcomes order, empty sessions, `tb=no`, and combined term/file outputs.
  - Update `collector.py` to handle skipped tests during the `setup` phase by capturing their results for accurate Markdown reporting.

- Implement Ticket 6: file output mode (--llm-report=file). [538ea3f](https://github.com/callowayproject/pytest-agent-digest/commit/538ea3fdbb9cf5dc08a536f5a793bb6ca2d2ea73)

  - Save test results to a Markdown file (default path: `test-results.md`) and confirm output in stdout.
  - Support custom output paths via `--llm-report-file` and `llm_report_file` ini option.
  - New behavior overwrites files on subsequent runs instead of appending.
  - File output mode does not suppress pytest default output.
  - Add integration tests for all acceptance criteria.

- Implement Ticket 5: terminal output mode (--llm-report=term). [3d914df](https://github.com/callowayproject/pytest-agent-digest/commit/3d914df363971e3aef79142d1ec522fc323f2f5b)

  - Unregister pytest's built-in terminalreporter when term mode is active
    (uses trylast=True on pytest_configure so the reporter is already
    registered before we remove it)
  - Render and print the Markdown report to stdout in pytest_sessionfinish
  - Add integration tests: Markdown in stdout, reporter suppressed, verbose
    passes section, no ANSI codes, both modes together

  **co-authored-by:** Claude Sonnet 4.6 <noreply@anthropic.com>

- Implement Ticket 4: Markdown renderer. [5f22ad2](https://github.com/callowayproject/pytest-agent-digest/commit/5f22ad20a6af7dc5f5a1eeb8040c595153fa545a)

  Add `pytest_llm_report/renderer.py` with `render_report()` that converts a
  populated `ReportCollector` into a Markdown string. The output includes a
  summary line, a `## Failures` section (failed + xpassed), a `## Skipped`
  section, and an optional `## Passes` section (verbose mode only). Traceback
  code blocks are suppressed when `tb_style="no"` or `longrepr` is absent.

  34 new unit tests in `tests/test_renderer.py` cover all acceptance criteria:
  no tests, all-passed (non-verbose + verbose), mixed outcomes, `--tb=no`, ANSI
  round-trip, no trailing whitespace, and single blank-line separation between
  sections.

  **co-authored-by:** Claude Sonnet 4.6 <noreply@anthropic.com>

- Implement Ticket 3: test result collector. [faf2e08](https://github.com/callowayproject/pytest-agent-digest/commit/faf2e08b6ed8970f12f33cf941ccf7d2b2695b46)

  - Add collector.py with TestResult dataclass, ReportCollector class,
    and strip_ansi helper covering all five outcome classifications
  - Wire ReportCollector into plugin via LLMReportPlugin class so
    pytest_runtest_logreport has access to session-scoped state
  - 29 new unit tests cover all outcome paths, ANSI stripping, counts
    property, and has_failures property

  **co-authored-by:** Claude Sonnet 4.6 <noreply@anthropic.com>

- Set up basic pytest plugin structure with hook implementations and tests. [98e58f3](https://github.com/callowayproject/pytest-agent-digest/commit/98e58f37ebb2ef052df8558e7d01935e65e80cac)

### Updates

- Delete .github/workflows/release-container.yaml. [7a682a8](https://github.com/callowayproject/pytest-agent-digest/commit/7a682a82106d1ca6cabcc32fb0db2c2a83b9538f)

- Remove unused container release workflow, update Anthropic and Coverage dependencies, and refine documentation build and deployment steps. [126b0f7](https://github.com/callowayproject/pytest-agent-digest/commit/126b0f79e56d82f34713d55a21b8fca16f74b524)

- Refactor `_extract_longrepr` and `_extract_skip_reason` to deduplicate logic for handling `longrepr`, moving shared functionality to `_longrepr_reason`. Remove unused `pytest_sessionfinish` export. [6abf199](https://github.com/callowayproject/pytest-agent-digest/commit/6abf199feee5f3c322d7cd2819a898f575665460)

- Refactor `render_report` to avoid reusing generic variable names for section lines (e.g., `lines`), improving clarity and maintainability. [2af8595](https://github.com/callowayproject/pytest-agent-digest/commit/2af859568cebcf209494eb361cbfa0b9b882557b)

- Refactor `pytest_sessionfinish` to integrate directly into `AgentDigestPlugin`, removing redundant module-level hook implementation. Update related unit tests accordingly. [d258540](https://github.com/callowayproject/pytest-agent-digest/commit/d258540250576ef96c5138c7d7266e7d8d0b0bfd)

- Update charset-normalizer to version 3.4.6 in dependency lockfile. [c52384e](https://github.com/callowayproject/pytest-agent-digest/commit/c52384e541e412ffbcd0deafcdce41fa4ab46bd0)

## 0.1.0 (2026-03-14)

### Other

- Initial commit. [8f45839](https://github.com/callowayproject/pytest-agent-digest/commit/8f45839f16ab45070a85a0311e2a0897ba385300)
