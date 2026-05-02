"""Top-level package for pytest_agent_digest.

The pytest11 entry point points to this package, so pytest hook functions
are imported here from ``plugin`` to make them discoverable.
"""

from pytest_agent_digest.plugin import (
    AgentDigestPlugin,
    get_output_modes,
    get_report_path,
    pytest_addoption,
    pytest_configure,
)

__version__ = "0.3.2"

__all__ = [
    "AgentDigestPlugin",
    "get_output_modes",
    "get_report_path",
    "pytest_addoption",
    "pytest_configure",
]
