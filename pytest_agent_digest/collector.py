"""Test result collector for pytest-agent-digest."""

import re
import warnings
from collections import Counter
from dataclasses import dataclass
from typing import Optional

import pytest


def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape sequences from *text*.

    Args:
        text: The string that may contain ANSI escape sequences.

    Returns:
        The input string with all ANSI color/style codes removed.
    """
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


@dataclass
class WarningRecord:
    """Represents a single warning captured during a pytest session.

    Attributes:
        message: The warning message text.
        category: The warning category class name (e.g. ``"DeprecationWarning"``).
        nodeid: The pytest node ID that triggered the warning, or ``""`` for session-level warnings.
        when: The phase when the warning was recorded (``"config"``, ``"collect"``, or ``"runtest"``).
        location: A ``(filename, lineno, function)`` tuple identifying the warning site, or ``None``.
    """

    message: str
    category: str
    nodeid: str
    when: str
    location: Optional[tuple[str, int, str]]


@dataclass
class TestResult:
    """Represents a single test outcome captured during a pytest session.

    Attributes:
        node_id: The pytest node ID (e.g. `tests/test_foo.py::test_bar`).
        outcome: One of `"passed"`, `"failed"`, `"skipped"`, `"xfailed"`, `"xpassed"`.
        longrepr: Formatted traceback or reason string, stripped of ANSI codes.
            `None` when not applicable.
        duration: Test duration in seconds.
        skip_reason: Human-readable skip reason for skipped tests; `None` otherwise.
    """

    __test__ = False

    node_id: str
    outcome: str
    longrepr: Optional[str]
    duration: float
    skip_reason: Optional[str]


class ReportCollector:
    """
    Accumulates the `TestResult` objects while a pytest session runs.

    Wire this into `pytest_configure` (instantiate) and `pytest_runtest_logreport` (call `add`) so the renderer can
    consume a fully populated collector at the session end.
    """

    def __init__(self) -> None:
        """Initialize with empty result and warning lists."""
        self.results: list[TestResult] = []
        self.warnings: list[WarningRecord] = []

    def add(self, report: pytest.TestReport) -> None:
        """
        Classify *report* and append a `TestResult` class if it is a call phase.

        ``report.when == "call"`` reports are stored for normal outcomes.
        ``report.when == "setup"`` reports are stored only when skipped, because
        ``@pytest.mark.skip`` raises a ``Skipped`` exception during the setup phase
        and never produces a call-phase report.

        Args:
            report: The pytest test report to classify and store.
        """
        if report.when == "setup" and report.skipped:
            outcome = "skipped"
            longrepr = self._extract_longrepr(report)
            skip_reason = self._extract_skip_reason(report, outcome)
            self.results.append(
                TestResult(
                    node_id=report.nodeid,
                    outcome=outcome,
                    longrepr=longrepr,
                    duration=report.duration,
                    skip_reason=skip_reason,
                )
            )
            return

        if report.when != "call":
            return

        outcome = self._classify(report)
        longrepr = self._extract_longrepr(report)
        skip_reason = self._extract_skip_reason(report, outcome)

        self.results.append(
            TestResult(
                node_id=report.nodeid,
                outcome=outcome,
                longrepr=longrepr,
                duration=report.duration,
                skip_reason=skip_reason,
            )
        )

    def add_warning(
        self,
        warning_message: warnings.WarningMessage,
        when: str,
        nodeid: str,
        location: Optional[tuple[str, int, str]],
    ) -> None:
        """
        Capture a pytest warning and append a `WarningRecord`.

        Args:
            warning_message: The ``warnings.WarningMessage`` instance from the hook.
            when: The phase when the warning was recorded (``"config"``, ``"collect"``, or ``"runtest"``).
            nodeid: The node ID of the test that triggered the warning, or ``""`` for session-level warnings.
            location: A ``(filename, lineno, function)`` tuple, or ``None``.
        """
        self.warnings.append(
            WarningRecord(
                message=str(warning_message.message),
                category=warning_message.category.__name__,
                nodeid=nodeid,
                when=when,
                location=location,
            )
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def counts(self) -> dict[str, int]:
        """
        Return a dict of `{outcome: count}` with zero-count keys omitted.

        Returns:
            Mapping from the outcome string to the number of results with that outcome.
        """
        return dict(Counter(tr.outcome for tr in self.results))

    @property
    def has_failures(self) -> bool:
        """
        Return `True` if any result is `"failed"` or `"xpassed"`.

        Returns:
            `True` when there is at least one failure or unexpected pass.
        """
        return any(tr.outcome in {"failed", "xpassed"} for tr in self.results)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _classify(report: pytest.TestReport) -> str:
        """
        Return the outcome string for *report*.

        Args:
            report: The test report to classify.

        Returns:
            One of `"passed"`, `"failed"`, `"skipped"`, `"xfailed"`, `"xpassed"`.
        """
        has_xfail = hasattr(report, "wasxfail")
        if report.passed:
            return "xpassed" if has_xfail else "passed"
        if report.skipped:
            return "xfailed" if has_xfail else "skipped"
        return "failed"

    @staticmethod
    def _longrepr_reason(longrepr: object) -> str:
        """
        Extract and ANSI-strip a reason string from a longrepr value.

        Skipped reports store ``longrepr`` as a ``(filename, lineno, reason)`` tuple;
        all other reports store it as a string-like object.

        Args:
            longrepr: The raw ``report.longrepr`` value (tuple or str-like).

        Returns:
            A plain-text reason string.
        """
        if isinstance(longrepr, tuple):
            return strip_ansi(str(longrepr[2]))
        return strip_ansi(str(longrepr))

    @staticmethod
    def _extract_longrepr(report: pytest.TestReport) -> Optional[str]:
        """
        Extract and ANSI-strip the longrepr from *report*.

        Args:
            report: The test report whose longrepr should be extracted.

        Returns:
            A plain-text longrepr string, or `None` if absent.
        """
        if report.longrepr is None:
            return None
        return ReportCollector._longrepr_reason(report.longrepr)

    @staticmethod
    def _extract_skip_reason(report: pytest.TestReport, outcome: str) -> Optional[str]:
        """
        Return the skip reason for skipped tests, else `None`.

        Args:
            report: The test report to inspect.
            outcome: The already-classified outcome string.

        Returns:
            The skip reason string, or `None` for non-skipped outcomes.
        """
        if outcome != "skipped":
            return None
        if report.longrepr is None:
            return None
        return ReportCollector._longrepr_reason(report.longrepr)
