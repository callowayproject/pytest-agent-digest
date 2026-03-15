"""pytest plugin hooks for pytest-llm-report."""

from pathlib import Path

import pytest

from pytest_llm_report.collector import ReportCollector

_PLUGIN_NAME = "llm_report_plugin"


class LLMReportPlugin:
    """
    Internal plugin class that holds the per-session state.

    Registered by `pytest_configure` so that `pytest_runtest_logreport` can access the shared
    `~pytest_llm_report.collector.ReportCollector` without a global.
    """

    def __init__(self) -> None:
        """Initialize the plugin with a fresh collector."""
        self.collector: ReportCollector = ReportCollector()

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        """
        Forward each test report to the collector.

        Args:
            report: The test report for the current phase.
        """
        self.collector.add(report)


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Register pytest-llm-report command-line options.

    Args:
        parser: The pytest argument parser.
    """
    parser.addoption(
        "--llm-report",
        action="append",
        choices=["term", "file"],
        default=None,
        help=(
            "Generate LLM-friendly Markdown report. Use 'term' for stdout, "
            "'file' for file output. Can be passed twice."
        )
    )
    parser.addoption(
        "--llm-report-file",
        action="store",
        default=None,
        help="Path for the Markdown report file (default: test-results.md).",
    )
    parser.addini(
        "llm_report_file",
        default="test-results.md",
        help="Default path for the LLM report file.",
    )


def pytest_configure(config: pytest.Config) -> None:
    """
    Configure the pytest-llm-report plugin.

    Instantiates the `LLMReportPlugin` class and registers it so its hooks are active for the session.

    Args:
        config: The pytest configuration object.
    """
    plugin = LLMReportPlugin()
    config.pluginmanager.register(plugin, _PLUGIN_NAME)


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """
    Process a test report after each test phase.

    The actual collection is handled by the `LLMReportPlugin` class; this stub satisfies the entry-point contract,
    so pytest discovers the hook.

    Args:
        report: The test report for the current phase.
    """


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """
    Finalize the report at the end of the test session.

    Args:
        session: The pytest session object.
        exitstatus: The exit status code for the session.
    """


def get_output_modes(config: pytest.Config) -> set[str]:
    """
    Return the set of output modes requested via --llm-report.

    Args:
        config: The pytest configuration object.

    Returns:
        A set of mode strings (`"term"`, `"file"`), or an empty set if the flag was not passed.
    """
    modes = config.getoption("--llm-report", default=None)
    if not modes:
        return set()
    return set(modes)


def get_report_path(config: pytest.Config) -> Path:
    """
    Return the output path for the Markdown report file.

    Resolution order:

    1. `--llm-report-file` CLI flag
    2. `llm_report_file` ini option
    3. Hard-coded default `test-results.md`

    Args:
        config: The pytest configuration object.

    Returns:
        A `pathlib.Path` pointing to the desired report file location.
    """
    cli_value = config.getoption("--llm-report-file", default=None)
    if cli_value is not None:
        return Path(cli_value)
    return Path(config.getini("llm_report_file"))
