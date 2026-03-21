"""Tests for the Markdown renderer (Ticket 4)."""

import pytest

from pytest_agent_digest.collector import ReportCollector, TestResult, strip_ansi
from pytest_agent_digest.renderer import render_report

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_collector(*results: TestResult) -> ReportCollector:
    """Build a ReportCollector pre-populated with the given TestResult objects."""
    collector = ReportCollector()
    collector.results = list(results)
    return collector


def _passed(node_id: str = "tests/test_foo.py::test_pass", duration: float = 0.1) -> TestResult:
    """Build a passed TestResult."""
    return TestResult(node_id=node_id, outcome="passed", longrepr=None, duration=duration, skip_reason=None)


def _failed(
    node_id: str = "tests/test_foo.py::test_fail",
    duration: float = 0.5,
    longrepr: str | None = "AssertionError: assert 1 == 2",
) -> TestResult:
    """Build a failed TestResult."""
    return TestResult(node_id=node_id, outcome="failed", longrepr=longrepr, duration=duration, skip_reason=None)


def _skipped(
    node_id: str = "tests/test_foo.py::test_skip",
    duration: float = 0.0,
    skip_reason: str = "not ready",
) -> TestResult:
    """Build a skipped TestResult."""
    return TestResult(
        node_id=node_id, outcome="skipped", longrepr=skip_reason, duration=duration, skip_reason=skip_reason
    )


def _xfailed(node_id: str = "tests/test_foo.py::test_xfail", duration: float = 0.1) -> TestResult:
    """Build an xfailed TestResult."""
    return TestResult(
        node_id=node_id, outcome="xfailed", longrepr="expected failure", duration=duration, skip_reason=None
    )


def _xpassed(node_id: str = "tests/test_foo.py::test_xpass", duration: float = 0.1) -> TestResult:
    """Build an xpassed TestResult."""
    return TestResult(node_id=node_id, outcome="xpassed", longrepr=None, duration=duration, skip_reason=None)


# ---------------------------------------------------------------------------
# Summary line
# ---------------------------------------------------------------------------


class TestSummaryLine:
    """The summary line is always present and lists non-zero outcome counts."""

    def test_no_tests_produces_empty_summary_line(self) -> None:
        """An empty collector renders a blank summary line."""
        result = render_report(_make_collector(), verbose=False, tb_style="short")
        assert result.splitlines()[0] == ""  # noqa: PLC1901

    def test_all_passed_summary(self) -> None:
        """Two passed results produce '2 passed' summary."""
        collector = _make_collector(_passed("t1"), _passed("t2"))
        result = render_report(collector, verbose=False, tb_style="short")
        assert result.splitlines()[0] == "2 passed"

    def test_mixed_outcomes_summary_in_canonical_order(self) -> None:
        """Summary lists categories in passed/failed/skipped/xfailed/xpassed order."""
        collector = _make_collector(_passed(), _failed(), _skipped(), _xfailed(), _xpassed())
        first_line = render_report(collector, verbose=False, tb_style="short").splitlines()[0]
        assert first_line == "1 passed, 1 failed, 1 skipped, 1 xfailed, 1 xpassed"

    def test_summary_omits_zero_count_categories(self) -> None:
        """Categories with zero results do not appear in the summary."""
        collector = _make_collector(_passed(), _failed())
        first_line = render_report(collector, verbose=False, tb_style="short").splitlines()[0]
        assert first_line == "1 passed, 1 failed"
        assert "skipped" not in first_line
        assert "xfailed" not in first_line
        assert "xpassed" not in first_line


# ---------------------------------------------------------------------------
# Failures section
# ---------------------------------------------------------------------------


class TestFailuresSection:
    """## Failures section appears for failed and xpassed results."""

    def test_failures_section_present_when_failures_exist(self) -> None:
        """## Failures heading appears when any result is failed."""
        result = render_report(_make_collector(_failed()), verbose=False, tb_style="short")
        assert "## Failures" in result

    def test_failures_section_absent_when_no_failures(self) -> None:
        """## Failures heading is absent when all results are passed."""
        result = render_report(_make_collector(_passed()), verbose=False, tb_style="short")
        assert "## Failures" not in result

    def test_failure_entry_has_node_id_heading(self) -> None:
        """Each failure entry has a ### <node_id> heading."""
        node_id = "tests/test_foo.py::test_bar"
        result = render_report(_make_collector(_failed(node_id=node_id)), verbose=False, tb_style="short")
        assert f"### {node_id}" in result

    def test_failure_entry_has_status_failed(self) -> None:
        """A failed result shows **Status:** FAILED."""
        result = render_report(_make_collector(_failed()), verbose=False, tb_style="short")
        assert "**Status:** FAILED" in result

    def test_failure_entry_has_duration(self) -> None:
        """Duration is formatted to two decimal places with 's' suffix."""
        result = render_report(_make_collector(_failed(duration=0.42)), verbose=False, tb_style="short")
        assert "**Duration:** 0.42s" in result

    def test_failure_duration_formatted_to_two_decimal_places(self) -> None:
        """Integer duration is zero-padded to two decimal places."""
        result = render_report(_make_collector(_failed(duration=1.0)), verbose=False, tb_style="short")
        assert "**Duration:** 1.00s" in result

    def test_traceback_code_block_present_when_longrepr_set(self) -> None:
        """A fenced code block containing the traceback appears by default."""
        result = render_report(_make_collector(_failed(longrepr="AssertionError")), verbose=False, tb_style="short")
        assert "```" in result
        assert "AssertionError" in result

    def test_traceback_omitted_when_tb_style_is_no(self) -> None:
        """No code block is rendered when tb_style is 'no'."""
        result = render_report(_make_collector(_failed(longrepr="AssertionError")), verbose=False, tb_style="no")
        assert "```" not in result

    def test_traceback_omitted_when_longrepr_is_none(self) -> None:
        """No code block is rendered when longrepr is None."""
        result = render_report(_make_collector(_failed(longrepr=None)), verbose=False, tb_style="short")
        assert "```" not in result

    def test_xpassed_appears_in_failures_section(self) -> None:
        """xpassed results are included in ## Failures."""
        result = render_report(_make_collector(_xpassed()), verbose=False, tb_style="short")
        assert "## Failures" in result
        assert "### tests/test_foo.py::test_xpass" in result

    def test_xpassed_status_label(self) -> None:
        """xpassed results show **Status:** XPASSED."""
        result = render_report(_make_collector(_xpassed()), verbose=False, tb_style="short")
        assert "**Status:** XPASSED" in result

    def test_xfailed_not_in_failures_section(self) -> None:
        """xfailed results do not appear in ## Failures (only in summary)."""
        result = render_report(_make_collector(_xfailed()), verbose=False, tb_style="short")
        assert "## Failures" not in result


# ---------------------------------------------------------------------------
# Skipped section
# ---------------------------------------------------------------------------


class TestSkippedSection:
    """## Skipped section appears for skipped results."""

    def test_skipped_section_present_when_skipped_exist(self) -> None:
        """## Skipped heading appears when any result is skipped."""
        result = render_report(_make_collector(_skipped()), verbose=False, tb_style="short")
        assert "## Skipped" in result

    def test_skipped_section_absent_when_no_skipped(self) -> None:
        """## Skipped heading is absent when no results are skipped."""
        result = render_report(_make_collector(_passed()), verbose=False, tb_style="short")
        assert "## Skipped" not in result

    def test_skipped_entry_format(self) -> None:
        """Skipped entries are formatted as '- <node_id>: <skip_reason>'."""
        node_id = "tests/test_foo.py::test_skip"
        result = render_report(
            _make_collector(_skipped(node_id=node_id, skip_reason="not ready")), verbose=False, tb_style="short"
        )
        assert f"- {node_id}: not ready" in result


# ---------------------------------------------------------------------------
# Passes section
# ---------------------------------------------------------------------------


class TestPassesSection:
    """## Passes section appears only in verbose mode."""

    def test_passes_section_absent_when_verbose_false(self) -> None:
        """## Passes is not rendered when verbose=False."""
        result = render_report(_make_collector(_passed()), verbose=False, tb_style="short")
        assert "## Passes" not in result

    def test_passes_section_present_when_verbose_true(self) -> None:
        """## Passes is rendered when verbose=True and passed results exist."""
        result = render_report(_make_collector(_passed()), verbose=True, tb_style="short")
        assert "## Passes" in result

    def test_passes_section_absent_when_no_passed_even_if_verbose(self) -> None:
        """## Passes is absent even with verbose=True if there are no passed results."""
        result = render_report(_make_collector(_failed()), verbose=True, tb_style="short")
        assert "## Passes" not in result

    def test_passes_entry_format(self) -> None:
        """Passed entries are formatted as '- <node_id>'."""
        node_id = "tests/test_foo.py::test_pass"
        result = render_report(_make_collector(_passed(node_id=node_id)), verbose=True, tb_style="short")
        assert f"- {node_id}" in result


# ---------------------------------------------------------------------------
# Formatting rules
# ---------------------------------------------------------------------------


class TestFormatting:
    """Output follows strict formatting rules."""

    def test_document_ends_with_newline(self) -> None:
        """The rendered string always ends with a newline character."""
        result = render_report(_make_collector(_passed()), verbose=False, tb_style="short")
        assert result.endswith("\n")

    def test_empty_session_document_ends_with_newline(self) -> None:
        """Empty session output still ends with a newline."""
        result = render_report(_make_collector(), verbose=False, tb_style="short")
        assert result.endswith("\n")

    def test_no_trailing_whitespace_on_any_line(self) -> None:
        """No line in the rendered output has trailing whitespace."""
        collector = _make_collector(_passed(), _failed(), _skipped())
        result = render_report(collector, verbose=True, tb_style="short")
        for line in result.splitlines():
            assert line == line.rstrip(), f"Trailing whitespace on line: {line!r}"

    def test_no_ansi_sequences_in_output(self) -> None:
        """Rendered output contains no ANSI escape sequences."""
        collector = _make_collector(_failed(longrepr="plain error text"))
        result = render_report(collector, verbose=False, tb_style="short")
        assert strip_ansi(result) == result

    def test_single_blank_line_between_sections(self) -> None:
        """Sections are separated by exactly one blank line (no double-blank-lines)."""
        collector = _make_collector(_passed(), _failed(), _skipped())
        result = render_report(collector, verbose=True, tb_style="short")
        assert "\n\n\n" not in result

    def test_no_tests_renders_no_sections(self) -> None:
        """An empty session produces no section headings."""
        result = render_report(_make_collector(), verbose=False, tb_style="short")
        assert "## Failures" not in result
        assert "## Skipped" not in result
        assert "## Passes" not in result

    def test_all_passed_non_verbose_renders_no_sections(self) -> None:
        """All-passed, non-verbose output has only the summary line."""
        result = render_report(_make_collector(_passed()), verbose=False, tb_style="short")
        assert "##" not in result

    def test_all_passed_verbose_renders_only_passes_section(self) -> None:
        """All-passed, verbose output has only ## Passes, no ## Failures or ## Skipped."""
        result = render_report(_make_collector(_passed()), verbose=True, tb_style="short")
        assert "## Passes" in result
        assert "## Failures" not in result
        assert "## Skipped" not in result

    @pytest.mark.parametrize(
        "tb_style",
        [
            pytest.param("short", id="short"),
            pytest.param("long", id="long"),
            pytest.param("auto", id="auto"),
        ],
    )
    def test_traceback_shown_for_non_no_tb_styles(self, tb_style: str) -> None:
        """Traceback code block is shown for any tb_style other than 'no'."""
        result = render_report(_make_collector(_failed(longrepr="Error")), verbose=False, tb_style=tb_style)
        assert "```" in result
