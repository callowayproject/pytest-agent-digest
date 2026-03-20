"""pytest plugin hooks for pytest-agent-digest."""

from pathlib import Path

import pytest

from pytest_agent_digest.collector import ReportCollector
from pytest_agent_digest.renderer import render_report

_PLUGIN_NAME = "agent_digest_plugin"


class AgentDigestPlugin:
    """
    Internal plugin class that holds the per-session state.

    Registered by `pytest_configure` so that `pytest_runtest_logreport` and
    `pytest_sessionfinish` share the same `~pytest_agent_digest.collector.ReportCollector`
    without a global.
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

    def pytest_sessionfinish(self, session: pytest.Session, exitstatus: int) -> None:
        """
        Finalize the digest at the end of the test session.

        When ``term`` mode is active, renders the Markdown digest and prints it to stdout.
        When ``file`` mode is active, writes the Markdown digest to disk and prints a confirmation line.
        Both modes may be active simultaneously.

        Args:
            session: The pytest session object.
            exitstatus: The exit status code for the session.
        """
        config = session.config
        modes = get_output_modes(config)
        if not modes:
            return

        report = render_report(self.collector, verbose=config.option.verbose, tb_style=config.option.tbstyle)

        if "term" in modes:
            print(report, end="")

        if "file" in modes:
            path = get_report_path(config)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(report, encoding="utf-8")
            print(f"Agent digest written to {path}")


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Register pytest-agent-digest command-line options.

    Args:
        parser: The pytest argument parser.
    """
    parser.addoption(
        "--agent-digest",
        action="append",
        choices=["term", "file"],
        default=None,
        help=(
            "Generate Agent-friendly Markdown digest. Use 'term' for stdout, "
            "'file' for file output. Can be passed twice."
        ),
    )
    parser.addoption(
        "--agent-digest-file",
        action="store",
        default=None,
        help="Path for the Markdown digest file (default: test-results.md).",
    )
    parser.addini(
        "agent_digest_file",
        default="test-results.md",
        help="Default path for the Agent digest file.",
    )


@pytest.hookimpl(trylast=True)
def pytest_configure(config: pytest.Config) -> None:
    """
    Configure the pytest-agent-digest plugin.

    Instantiates the `AgentDigestPlugin` class and registers it so its hooks are active for the session.
    When ``term`` mode is active, unregisters pytest's built-in terminal reporter so only the Markdown
    digest appears on stdout.

    Marked ``trylast=True`` so that the built-in terminal reporter is already registered by the time
    this hook runs, making it safe to unregister.

    Args:
        config: The pytest configuration object.
    """
    plugin = AgentDigestPlugin()
    config.pluginmanager.register(plugin, _PLUGIN_NAME)

    if "term" in get_output_modes(config):
        tr = config.pluginmanager.get_plugin("terminalreporter")
        if tr is not None:
            config.pluginmanager.unregister(tr)


def get_output_modes(config: pytest.Config) -> set[str]:
    """
    Return the set of output modes requested via --agent-digest.

    Args:
        config: The pytest configuration object.

    Returns:
        A set of mode strings (`"term"`, `"file"`), or an empty set if the flag was not passed.
    """
    modes = config.getoption("--agent-digest", default=None)
    if not modes:
        return set()
    return set(modes)


def get_report_path(config: pytest.Config) -> Path:
    """
    Return the output path for the Markdown digest file.

    Resolution order:

    1. `--agent-digest-file` CLI flag
    2. `agent_digest_file` ini option
    3. Hard-coded default `test-results.md`

    Args:
        config: The pytest configuration object.

    Returns:
        A `pathlib.Path` pointing to the desired report file location.
    """
    cli_value = config.getoption("--agent-digest-file", default=None)
    if cli_value is not None:
        return Path(cli_value)
    return Path(config.getini("agent_digest_file"))
