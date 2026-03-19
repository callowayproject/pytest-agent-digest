# pytest-agent-digest

A pytest plugin that generates compact Markdown digests designed for consumption by AI agents and LLMs. Instead of the standard terminal output, `pytest-agent-digest` produces structured Markdown that is typically **≥20% smaller in token count** than raw pytest output — keeping your context window budget under control.

[![PyPI](https://img.shields.io/pypi/v/pytest-agent-digest)](https://pypi.org/project/pytest-agent-digest/)
[![Python](https://img.shields.io/pypi/pyversions/pytest-agent-digest)](https://pypi.org/project/pytest-agent-digest/)

## Quick start

```bash
# Install
pip install pytest-agent-digest

# Print Markdown digest to stdout (replaces normal output)
pytest --agent-digest=term

# Write digest to test-results.md (normal output preserved)
pytest --agent-digest=file

# Both at once
pytest --agent-digest=term --agent-digest=file
```

## Documentation

Full documentation is available at **<https://callowayproject.github.io/pytest-agent-digest>**, including:

- [Quickstart guide](https://callowayproject.github.io/pytest-agent-digest/quickstart/)
- [Options reference](https://callowayproject.github.io/pytest-agent-digest/reference/options/)
