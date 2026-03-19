"""Markdown renderer for pytest-agent-digest."""

from pytest_agent_digest.collector import ReportCollector, TestResult

_OUTCOME_ORDER = ["passed", "failed", "skipped", "xfailed", "xpassed"]

_STATUS_LABEL: dict[str, str] = {
    "failed": "FAILED",
    "xpassed": "XPASSED",
}


def render_report(collector: ReportCollector, verbose: int, tb_style: str) -> str:
    """
    Render a Markdown report from a populated collector.

    Args:
        collector: The populated ``ReportCollector`` instance.
        verbose: If ``True``, include a ``## Passes`` section listing each passed test.
        tb_style: The pytest ``--tb`` style value.  When ``"no"``, traceback
            code blocks are omitted from failure entries.

    Returns:
        A Markdown string suitable for Agent consumption.  The document always
        ends with a newline and contains no ANSI escape sequences.
    """
    sections: list[str] = []

    # ------------------------------------------------------------------
    # Summary line (always present, even when empty)
    # ------------------------------------------------------------------
    counts = collector.counts
    summary_parts = [f"{counts[o]} {o}" for o in _OUTCOME_ORDER if o in counts]
    sections.append(", ".join(summary_parts))

    # ------------------------------------------------------------------
    # Failures section (failed + xpassed)
    # ------------------------------------------------------------------
    failures = [r for r in collector.results if r.outcome in {"failed", "xpassed"}]
    if failures:
        lines: list[str] = ["## Failures"]
        for result in failures:
            lines.extend(_failure_entry_lines(result, tb_style))
        sections.append("\n".join(lines))

    # ------------------------------------------------------------------
    # Skipped section
    # ------------------------------------------------------------------
    skipped = [r for r in collector.results if r.outcome == "skipped"]
    if skipped:
        lines = ["## Skipped", ""]
        for result in skipped:
            lines.append(f"- {result.node_id}: {result.skip_reason}")
        sections.append("\n".join(lines))

    # ------------------------------------------------------------------
    # Passes section (verbose only)
    # ------------------------------------------------------------------
    if verbose:
        passed = [r for r in collector.results if r.outcome == "passed"]
        if passed:
            lines = ["## Passes", ""]
            for result in passed:
                lines.append(f"- {result.node_id}")
            sections.append("\n".join(lines))

    return "\n\n".join(sections) + "\n"


def _failure_entry_lines(result: TestResult, tb_style: str) -> list[str]:
    """
    Build the lines for a single failure entry.

    Args:
        result: The ``TestResult`` to render (must be ``failed`` or ``xpassed``).
        tb_style: The pytest ``--tb`` style; ``"no"`` suppresses the traceback block.

    Returns:
        A list of strings (without a trailing blank line) representing the entry.
    """
    lines = [
        "",
        f"### {result.node_id}",
        "",
        f"**Status:** {_STATUS_LABEL[result.outcome]}",
        f"**Duration:** {result.duration:.2f}s",
    ]
    if tb_style != "no" and result.longrepr:
        lines.append("")
        lines.append("```")
        lines.extend(tb_line.rstrip() for tb_line in result.longrepr.splitlines())
        lines.append("```")
    return lines
