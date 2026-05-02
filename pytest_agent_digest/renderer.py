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
        verbose: Verbosity level (``0`` = normal, ``1`` = verbose). When non-zero,
            includes a ``## Passes`` section listing each passed test.
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
    if collector.warnings:
        n = len(collector.warnings)
        summary_parts.append(f"{n} warning{'s' if n != 1 else ''}")
    sections.append(", ".join(summary_parts))

    # ------------------------------------------------------------------
    # Failures section (failed + xpassed)
    # ------------------------------------------------------------------
    failures = [r for r in collector.results if r.outcome in {"failed", "xpassed"}]
    if failures:
        failure_lines: list[str] = ["## Failures"]
        for result in failures:
            failure_lines.extend(_failure_entry_lines(result, tb_style))
        sections.append("\n".join(failure_lines))

    # ------------------------------------------------------------------
    # Warnings section
    # ------------------------------------------------------------------
    if collector.warnings:
        sections.append(_warnings_section(collector))

    # ------------------------------------------------------------------
    # Skipped section
    # ------------------------------------------------------------------
    skipped = [r for r in collector.results if r.outcome == "skipped"]
    if skipped:
        skipped_lines: list[str] = ["## Skipped", ""]
        skipped_lines.extend(f"- {r.node_id}: {r.skip_reason}" for r in skipped)
        sections.append("\n".join(skipped_lines))

    # ------------------------------------------------------------------
    # Passes section (verbose only)
    # ------------------------------------------------------------------
    if verbose:
        passed = [r for r in collector.results if r.outcome == "passed"]
        if passed:
            passed_lines: list[str] = ["## Passes", ""]
            passed_lines.extend(f"- {r.node_id}" for r in passed)
            sections.append("\n".join(passed_lines))

    return "\n\n".join(sections) + "\n"


def _warnings_section(collector: ReportCollector) -> str:
    """
    Build the ``## Warnings`` section string.

    Args:
        collector: The populated ``ReportCollector`` instance.

    Returns:
        A Markdown string for the warnings section (no trailing newline).
    """
    lines: list[str] = ["## Warnings", ""]
    for w in collector.warnings:
        if w.nodeid:
            source = w.nodeid
        elif w.location:
            source = f"{w.location[0]}:{w.location[1]}"
        else:
            source = ""
        if source:
            lines.append(f"- [{w.when}] {source}: {w.category}: {w.message}")
        else:
            lines.append(f"- [{w.when}] {w.category}: {w.message}")
    return "\n".join(lines)


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
        f"**Status:** {_STATUS_LABEL.get(result.outcome, result.outcome.upper())}",
        f"**Duration:** {result.duration:.2f}s",
    ]
    if tb_style != "no" and result.longrepr:
        lines.append("")
        lines.append("```")
        lines.extend(tb_line.rstrip() for tb_line in result.longrepr.splitlines())
        lines.append("```")
    return lines
