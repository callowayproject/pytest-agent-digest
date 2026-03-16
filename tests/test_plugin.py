"""Tests for the pytest_llm_report plugin skeleton (Ticket 1)."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

import pytest_llm_report.plugin as plugin


def test_plugin_module_is_importable() -> None:
    """The plugin module must be importable without error."""
    import pytest_llm_report.plugin  # noqa: F401


def test_pytest_addoption_exists() -> None:
    """pytest_addoption hook stub must exist and be callable."""
    assert callable(plugin.pytest_addoption)


def test_pytest_configure_exists() -> None:
    """pytest_configure hook stub must exist and be callable."""
    assert callable(plugin.pytest_configure)


def test_pytest_sessionfinish_exists() -> None:
    """pytest_sessionfinish hook stub must exist and be callable."""
    assert callable(plugin.pytest_sessionfinish)


def test_hooks_exposed_from_package() -> None:
    """All hooks must be re-exported from the top-level package."""
    import pytest_llm_report as pkg

    assert callable(pkg.pytest_addoption)
    assert callable(pkg.pytest_configure)
    assert callable(pkg.pytest_sessionfinish)


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


def _make_config(llm_report=None, llm_report_file=None) -> MagicMock:
    """Create a mock pytest.Config with the given option values."""
    config = MagicMock()

    def getoption(name, default=None):
        if name == "--llm-report":
            return llm_report if llm_report is not None else default
        if name == "--llm-report-file":
            return llm_report_file if llm_report_file is not None else default
        return default

    def getini(name):
        if name == "llm_report_file":
            return "test-results.md"
        return ""

    config.getoption.side_effect = getoption
    config.getini.side_effect = getini
    return config


class TestGetOutputModes:
    """Test the get_output_modes function."""

    def test_no_flag_returns_empty_set(self) -> None:
        """No --llm-report flag returns empty set."""
        config = _make_config()
        assert plugin.get_output_modes(config) == set()

    def test_term_flag_returns_term(self) -> None:
        """--llm-report=term returns {'term'}."""
        config = _make_config(llm_report=["term"])
        assert plugin.get_output_modes(config) == {"term"}

    def test_file_flag_returns_file(self) -> None:
        """--llm-report=file returns {'file'}."""
        config = _make_config(llm_report=["file"])
        assert plugin.get_output_modes(config) == {"file"}

    def test_both_flags_returns_both(self) -> None:
        """--llm-report=term --llm-report=file returns {'term', 'file'}."""
        config = _make_config(llm_report=["term", "file"])
        assert plugin.get_output_modes(config) == {"term", "file"}


class TestGetReportPath:
    """Test the get_report_path function."""
    def test_cli_value_takes_precedence(self) -> None:
        """CLI --llm-report-file takes precedence and returns Path of that value."""
        config = _make_config(llm_report_file="my-report.md")
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
