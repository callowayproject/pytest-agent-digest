"""Tests for the ReportCollector and TestResult (Ticket 3)."""

import warnings
from typing import Optional
from unittest.mock import MagicMock

import pytest

from pytest_agent_digest.collector import ReportCollector, TestResult, WarningRecord, strip_ansi

# ---------------------------------------------------------------------------
# strip_ansi
# ---------------------------------------------------------------------------


class TestStripAnsi:
    """Tests for the strip_ansi helper."""

    def test_removes_color_escape_sequences(self) -> None:
        """ANSI color codes are stripped from the string."""
        assert strip_ansi("\x1b[31mred text\x1b[0m") == "red text"

    def test_removes_bold_escape_sequences(self) -> None:
        """ANSI bold codes are stripped."""
        assert strip_ansi("\x1b[1mbold\x1b[0m") == "bold"

    def test_removes_compound_escape_sequences(self) -> None:
        """Compound ANSI codes (e.g. ;) are stripped."""
        assert strip_ansi("\x1b[1;32mgreen bold\x1b[0m") == "green bold"

    def test_plain_string_unchanged(self) -> None:
        """Strings without ANSI codes are returned unchanged."""
        assert strip_ansi("plain text") == "plain text"

    def test_empty_string(self) -> None:
        """Empty string returns empty string."""
        assert strip_ansi("") == ""  # noqa: PLC1901


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_report(
    when: str = "call",
    passed: bool = False,
    failed: bool = False,
    skipped: bool = False,
    longrepr: object = None,
    duration: float = 0.1,
    node_id: str = "test_mod.py::test_foo",
    wasxfail: Optional[str] = None,
) -> MagicMock:
    """Build a minimal mock pytest.TestReport."""
    report = MagicMock(spec=pytest.TestReport)
    report.when = when
    report.passed = passed
    report.failed = failed
    report.skipped = skipped
    report.longrepr = longrepr
    report.duration = duration
    report.nodeid = node_id

    # xfail/xpass detection uses the wasxfail attribute
    if wasxfail is not None:
        report.wasxfail = wasxfail
    else:
        # Make attribute access raise AttributeError (not present)
        del report.wasxfail

    return report


# ---------------------------------------------------------------------------
# TestResult
# ---------------------------------------------------------------------------


class TestTestResultDataclass:
    """TestResult dataclass fields and defaults."""

    def test_has_required_fields(self) -> None:
        """TestResult can be constructed with all required fields."""
        result = TestResult(
            node_id="test_mod.py::test_foo",
            outcome="passed",
            longrepr=None,
            duration=0.5,
            skip_reason=None,
        )
        assert result.node_id == "test_mod.py::test_foo"
        assert result.outcome == "passed"
        assert result.longrepr is None
        assert result.duration == 0.5  # noqa: RUF069
        assert result.skip_reason is None


# ---------------------------------------------------------------------------
# ReportCollector — outcome classification
# ---------------------------------------------------------------------------


class TestReportCollectorAdd:
    """ReportCollector.add classifies reports by outcome."""

    def test_passed_report_classified_as_passed(self) -> None:
        """A call-phase passed report is stored as 'passed'."""
        collector = ReportCollector()
        report = _make_report(when="call", passed=True, duration=0.2)
        collector.add(report)
        assert len(collector.results) == 1
        assert collector.results[0].outcome == "passed"
        assert collector.results[0].duration == 0.2  # noqa: RUF069

    def test_failed_report_classified_as_failed(self) -> None:
        """A call-phase failed report is stored as 'failed'."""
        collector = ReportCollector()
        report = _make_report(when="call", failed=True, longrepr="AssertionError: ...")
        collector.add(report)
        assert collector.results[0].outcome == "failed"

    def test_skipped_report_classified_as_skipped(self) -> None:
        """A call-phase skipped report is stored as 'skipped'."""
        collector = ReportCollector()
        report = _make_report(when="call", skipped=True)
        report.longrepr = ("file.py", 1, "Skipped: reason")
        collector.add(report)
        assert collector.results[0].outcome == "skipped"

    def test_xfailed_report_classified_as_xfailed(self) -> None:
        """A passed report with wasxfail attribute is classified as 'xfailed'."""
        collector = ReportCollector()
        report = _make_report(when="call", skipped=True, wasxfail="reason")
        collector.add(report)
        assert collector.results[0].outcome == "xfailed"

    def test_xpassed_report_classified_as_xpassed(self) -> None:
        """A passed report with wasxfail attribute is classified as 'xpassed'."""
        collector = ReportCollector()
        report = _make_report(when="call", passed=True, wasxfail="reason")
        collector.add(report)
        assert collector.results[0].outcome == "xpassed"

    def test_non_call_phase_reports_are_ignored(self) -> None:
        """Setup and teardown phase reports are not collected."""
        collector = ReportCollector()
        collector.add(_make_report(when="setup", passed=True))
        collector.add(_make_report(when="teardown", passed=True))
        assert collector.results == []

    def test_longrepr_ansi_stripped(self) -> None:
        """ANSI codes in longrepr are stripped when stored."""
        collector = ReportCollector()
        report = _make_report(when="call", failed=True, longrepr="\x1b[31mERROR\x1b[0m")
        collector.add(report)
        assert collector.results[0].longrepr == "ERROR"

    def test_node_id_stored(self) -> None:
        """The node_id from report.nodeid is stored on TestResult."""
        collector = ReportCollector()
        report = _make_report(when="call", passed=True, node_id="tests/test_x.py::test_bar")
        collector.add(report)
        assert collector.results[0].node_id == "tests/test_x.py::test_bar"

    def test_skip_reason_extracted_from_tuple_longrepr(self) -> None:
        """For skipped tests, skip_reason is extracted from the longrepr tuple."""
        collector = ReportCollector()
        report = _make_report(when="call", skipped=True)
        report.longrepr = ("file.py", 10, "Skipped: needs network")
        collector.add(report)
        assert collector.results[0].skip_reason == "Skipped: needs network"

    def test_skip_reason_none_for_non_skipped(self) -> None:
        """Non-skipped results have skip_reason=None."""
        collector = ReportCollector()
        report = _make_report(when="call", passed=True)
        collector.add(report)
        assert collector.results[0].skip_reason is None


# ---------------------------------------------------------------------------
# ReportCollector — counts property
# ---------------------------------------------------------------------------


class TestReportCollectorCounts:
    """Tests for the counts property."""

    def test_empty_collector_returns_empty_dict(self) -> None:
        """No results means empty counts dict."""
        collector = ReportCollector()
        assert collector.counts == {}

    def test_zero_count_categories_omitted(self) -> None:
        """Outcomes with count 0 are not included in counts."""
        collector = ReportCollector()
        collector.add(_make_report(when="call", passed=True))
        counts = collector.counts
        assert "failed" not in counts
        assert "skipped" not in counts

    def test_counts_reflect_all_added_results(self) -> None:
        """Counts match the number of results per outcome."""
        collector = ReportCollector()
        collector.add(_make_report(when="call", passed=True, node_id="t1"))
        collector.add(_make_report(when="call", passed=True, node_id="t2"))
        collector.add(_make_report(when="call", failed=True, node_id="t3"))
        assert collector.counts == {"passed": 2, "failed": 1}

    @pytest.mark.parametrize(
        "outcome,kwargs",
        [
            pytest.param("passed", {"passed": True}, id="passed"),
            pytest.param("failed", {"failed": True}, id="failed"),
            pytest.param("skipped", {"skipped": True}, id="skipped"),
            pytest.param("xfailed", {"skipped": True, "wasxfail": "r"}, id="xfailed"),
            pytest.param("xpassed", {"passed": True, "wasxfail": "r"}, id="xpassed"),
        ],
    )
    def test_each_outcome_counted(self, outcome: str, kwargs: dict) -> None:
        """Each of the five outcomes is counted correctly."""
        collector = ReportCollector()
        report = _make_report(when="call", **kwargs)
        collector.add(report)
        assert collector.counts.get(outcome) == 1


# ---------------------------------------------------------------------------
# ReportCollector — has_failures property
# ---------------------------------------------------------------------------


class TestReportCollectorHasFailures:
    """Tests for the has_failures property."""

    def test_false_when_no_results(self) -> None:
        """has_failures is False when there are no results."""
        assert ReportCollector().has_failures is False

    def test_false_when_only_passed(self) -> None:
        """has_failures is False when all results are passed."""
        collector = ReportCollector()
        collector.add(_make_report(when="call", passed=True))
        assert collector.has_failures is False

    def test_true_when_failed_present(self) -> None:
        """has_failures is True when any result is failed."""
        collector = ReportCollector()
        collector.add(_make_report(when="call", failed=True))
        assert collector.has_failures is True

    def test_true_when_xpassed_present(self) -> None:
        """has_failures is True when any result is xpassed (unexpected pass)."""
        collector = ReportCollector()
        collector.add(_make_report(when="call", passed=True, wasxfail="reason"))
        assert collector.has_failures is True

    def test_false_when_only_skipped(self) -> None:
        """has_failures is False when results are only skipped."""
        collector = ReportCollector()
        report = _make_report(when="call", skipped=True)
        report.longrepr = ("f.py", 1, "Skipped: x")
        collector.add(report)
        assert collector.has_failures is False


# ---------------------------------------------------------------------------
# Helpers for warning tests
# ---------------------------------------------------------------------------


def _make_warning_message(
    message: str = "use new API",
    category: type = DeprecationWarning,
) -> warnings.WarningMessage:
    """Build a minimal mock warnings.WarningMessage."""
    wm = MagicMock(spec=warnings.WarningMessage)
    wm.message = category(message)
    wm.category = category
    return wm


# ---------------------------------------------------------------------------
# WarningRecord dataclass
# ---------------------------------------------------------------------------


class TestWarningRecord:
    """WarningRecord dataclass fields."""

    def test_has_required_fields(self) -> None:
        """WarningRecord can be constructed with all required fields."""
        record = WarningRecord(
            message="use new API",
            category="DeprecationWarning",
            nodeid="tests/test_foo.py::test_bar",
            when="runtest",
            location=("path/to/file.py", 42, "test_bar"),
        )
        assert record.message == "use new API"
        assert record.category == "DeprecationWarning"
        assert record.nodeid == "tests/test_foo.py::test_bar"
        assert record.when == "runtest"
        assert record.location == ("path/to/file.py", 42, "test_bar")

    def test_location_can_be_none(self) -> None:
        """WarningRecord accepts None for location."""
        record = WarningRecord(
            message="msg",
            category="UserWarning",
            nodeid="",
            when="config",
            location=None,
        )
        assert record.location is None


# ---------------------------------------------------------------------------
# ReportCollector — warnings
# ---------------------------------------------------------------------------


class TestReportCollectorWarnings:
    """Tests for ReportCollector.add_warning and .warnings."""

    def test_warnings_empty_on_init(self) -> None:
        """Warnings list starts empty."""
        assert ReportCollector().warnings == []

    def test_add_warning_stores_record(self) -> None:
        """add_warning appends a WarningRecord to .warnings."""
        collector = ReportCollector()
        wm = _make_warning_message("old API", DeprecationWarning)
        collector.add_warning(wm, when="runtest", nodeid="tests/test_foo.py::test_bar", location=None)
        assert len(collector.warnings) == 1
        record = collector.warnings[0]
        assert record.message == "old API"
        assert record.category == "DeprecationWarning"
        assert record.nodeid == "tests/test_foo.py::test_bar"
        assert record.when == "runtest"

    def test_multiple_warnings_accumulate(self) -> None:
        """Each add_warning call appends a new record."""
        collector = ReportCollector()
        collector.add_warning(_make_warning_message("w1"), when="runtest", nodeid="t1", location=None)
        collector.add_warning(_make_warning_message("w2"), when="runtest", nodeid="t2", location=None)
        assert len(collector.warnings) == 2

    def test_category_name_extracted(self) -> None:
        """The category class name is stored as a string."""
        collector = ReportCollector()
        collector.add_warning(_make_warning_message("msg", UserWarning), when="runtest", nodeid="", location=None)
        assert collector.warnings[0].category == "UserWarning"

    def test_session_level_warning_empty_nodeid(self) -> None:
        """Session-level warnings store an empty nodeid."""
        collector = ReportCollector()
        collector.add_warning(_make_warning_message(), when="config", nodeid="", location=("cfg.py", 1, "<module>"))
        assert not collector.warnings[0].nodeid
        assert collector.warnings[0].when == "config"

    def test_location_stored(self) -> None:
        """The location tuple is stored on the WarningRecord."""
        collector = ReportCollector()
        loc = ("path/to/file.py", 42, "test_bar")
        collector.add_warning(_make_warning_message(), when="runtest", nodeid="", location=loc)
        assert collector.warnings[0].location == loc
