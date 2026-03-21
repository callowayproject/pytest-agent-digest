"""Tests for the pytest_agent_digest plugin skeleton."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

import pytest_agent_digest.plugin as plugin


def test_plugin_module_is_importable() -> None:
    """The plugin module must be importable without error."""
    import pytest_agent_digest.plugin  # noqa: F401


def test_pytest_addoption_exists() -> None:
    """pytest_addoption hook stub must exist and be callable."""
    assert callable(plugin.pytest_addoption)


def test_pytest_configure_exists() -> None:
    """pytest_configure hook stub must exist and be callable."""
    assert callable(plugin.pytest_configure)


def test_pytest_sessionfinish_exists() -> None:
    """pytest_sessionfinish hook must exist on AgentDigestPlugin and be callable."""
    assert callable(plugin.AgentDigestPlugin.pytest_sessionfinish)


def test_hooks_exposed_from_package() -> None:
    """Module-level hooks must be re-exported from the top-level package."""
    import pytest_agent_digest as pkg

    assert callable(pkg.pytest_addoption)
    assert callable(pkg.pytest_configure)


def test_pytest_addoption_accepts_parser(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """pytest_addoption must accept a parser argument without raising."""
    pytester.makepyfile("def test_dummy(): pass")
    result = pytester.runpytest("--co", "-q")
    assert result.ret == 0


def test_plugin_loads_without_error(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """Plugin must load cleanly — collection must succeed."""
    pytester.makepyfile("def test_dummy(): pass")
    result = pytester.runpytest("--co", "-q")
    assert result.ret == 0


# --- Tests for get_output_modes ---


def _make_config(agent_digest=None, agent_digest_file=None) -> MagicMock:
    """Create a mock pytest.Config with the given option values."""
    config = MagicMock()

    def getoption(name, default=None):
        if name == "--agent-digest":
            return agent_digest if agent_digest is not None else default
        if name == "--agent-digest-file":
            return agent_digest_file if agent_digest_file is not None else default
        return default

    def getini(name):
        if name == "agent_digest_file":
            return "test-results.md"
        return ""

    config.getoption.side_effect = getoption
    config.getini.side_effect = getini
    return config


class TestGetOutputModes:
    """Test the get_output_modes function."""

    def test_no_flag_returns_empty_set(self) -> None:
        """No --agent-digest flag returns empty set."""
        config = _make_config()
        assert plugin.get_output_modes(config) == set()

    def test_term_flag_returns_term(self) -> None:
        """--agent-digest=term returns {'term'}."""
        config = _make_config(agent_digest=["term"])
        assert plugin.get_output_modes(config) == {"term"}

    def test_file_flag_returns_file(self) -> None:
        """--agent-digest=file returns {'file'}."""
        config = _make_config(agent_digest=["file"])
        assert plugin.get_output_modes(config) == {"file"}

    def test_both_flags_returns_both(self) -> None:
        """--agent-digest=term --agent-digest=file returns {'term', 'file'}."""
        config = _make_config(agent_digest=["term", "file"])
        assert plugin.get_output_modes(config) == {"term", "file"}


class TestGetReportPath:
    """Test the get_report_path function."""

    def test_cli_value_takes_precedence(self) -> None:
        """CLI --agent-digest-file takes precedence and returns Path of that value."""
        config = _make_config(agent_digest_file="my-report.md")
        assert plugin.get_report_path(config) == Path("my-report.md")

    def test_ini_fallback_when_cli_not_set(self) -> None:
        """When CLI flag not set, falls back to ini value."""
        config = MagicMock()
        config.getoption.return_value = None
        config.getini.return_value = "custom-ini.md"
        assert plugin.get_report_path(config) == Path("custom-ini.md")

    def test_returns_default_when_neither_cli_nor_ini_set(self) -> None:
        """When neither CLI nor custom ini set, returns Path('test-results.md')."""
        config = _make_config()
        assert plugin.get_report_path(config) == Path("test-results.md")
