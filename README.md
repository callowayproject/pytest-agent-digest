# pytest-llm-report

A pytest plugin that generates compact Markdown reports designed for consumption by AI agents and LLMs. Instead of the standard terminal output, `pytest-llm-report` produces structured Markdown that is typically **≥20% smaller in token count** than raw pytest output — keeping your context window budget under control.

[![PyPI](https://img.shields.io/pypi/v/pytest-llm-report)](https://pypi.org/project/pytest-llm-report/)
[![Python](https://img.shields.io/pypi/pyversions/pytest-llm-report)](https://pypi.org/project/pytest-llm-report/)

## Quick start

```bash
# Install
pip install pytest-llm-report

# Print Markdown report to stdout (replaces normal output)
pytest --llm-report=term

# Write report to test-results.md (normal output preserved)
pytest --llm-report=file

# Both at once
pytest --llm-report=term --llm-report=file
```

## Documentation

Full documentation is available at **<https://callowayproject.github.io/pytest_llm_report>**, including:

- [Quickstart guide](https://callowayproject.github.io/pytest_llm_report/quickstart/)
- [Options reference](https://callowayproject.github.io/pytest_llm_report/reference/options/)
