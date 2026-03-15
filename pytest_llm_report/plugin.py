"""pytest plugin hooks for pytest-llm-report."""

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register pytest-llm-report command-line options."""


def pytest_configure(config: pytest.Config) -> None:
    """Configure the pytest-llm-report plugin."""


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """Process a test report after each test phase."""


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Finalize the report at the end of the test session."""
