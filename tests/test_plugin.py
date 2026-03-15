"""Tests for the pytest_llm_report plugin skeleton (Ticket 1)."""

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


def test_pytest_runtest_logreport_exists() -> None:
    """pytest_runtest_logreport hook stub must exist and be callable."""
    assert callable(plugin.pytest_runtest_logreport)


def test_pytest_sessionfinish_exists() -> None:
    """pytest_sessionfinish hook stub must exist and be callable."""
    assert callable(plugin.pytest_sessionfinish)


def test_hooks_exposed_from_package() -> None:
    """All four hooks must be re-exported from the top-level package."""
    import pytest_llm_report as pkg

    assert callable(pkg.pytest_addoption)
    assert callable(pkg.pytest_configure)
    assert callable(pkg.pytest_runtest_logreport)
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
