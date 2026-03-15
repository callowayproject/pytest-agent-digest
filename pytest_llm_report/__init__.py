"""Top-level package for pytest_llm_report.

The pytest11 entry point points to this package, so pytest hook functions
are imported here from ``plugin`` to make them discoverable.
"""

from pytest_llm_report.plugin import (
    LLMReportPlugin,
    get_output_modes,
    get_report_path,
    pytest_addoption,
    pytest_configure,
    pytest_runtest_logreport,
    pytest_sessionfinish,
)

__version__ = "0.1.0"

__all__ = [
    "LLMReportPlugin",
    "get_output_modes",
    "get_report_path",
    "pytest_addoption",
    "pytest_configure",
    "pytest_runtest_logreport",
    "pytest_sessionfinish",
]
