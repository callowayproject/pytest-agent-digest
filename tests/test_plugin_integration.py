"""Pytester integration tests for CLI option acceptance (Tickets 2, 5)."""

import re

import pytest

# ---------------------------------------------------------------------------
# Ticket 2 — CLI option acceptance
# ---------------------------------------------------------------------------


def test_llm_report_term_collection(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=term exits 0 during collection."""
    pytester.makepyfile("def test_dummy(): pass")
    result = pytester.runpytest("--llm-report=term", "--co", "-q")
    assert result.ret == 0


def test_llm_report_file_collection(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=file exits 0 during collection."""
    pytester.makepyfile("def test_dummy(): pass")
    result = pytester.runpytest("--llm-report=file", "--co", "-q")
    assert result.ret == 0


def test_llm_report_both_collection(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=term --llm-report=file exits 0 during collection."""
    pytester.makepyfile("def test_dummy(): pass")
    result = pytester.runpytest("--llm-report=term", "--llm-report=file", "--co", "-q")
    assert result.ret == 0


def test_llm_report_invalid_value(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=bad exits non-zero (invalid choice)."""
    pytester.makepyfile("def test_dummy(): pass")
    result = pytester.runpytest("--llm-report=bad", "--co", "-q")
    assert result.ret != 0


# ---------------------------------------------------------------------------
# Ticket 5 — Terminal output mode
# ---------------------------------------------------------------------------


def test_term_mode_prints_markdown_summary(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=term prints a Markdown summary line to stdout."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--llm-report=term")
    assert result.ret == 0
    assert "1 passed" in result.stdout.str()


def test_term_mode_suppresses_default_reporter(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=term suppresses pytest's default session header from stdout."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--llm-report=term")
    assert "=== test session starts ===" not in result.stdout.str()


def test_without_term_mode_default_output_is_unchanged(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """Without --llm-report=term, pytest's default terminal output is present."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest()
    assert "=== test session starts ===" in result.stdout.str()


def test_term_mode_includes_failures_section(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=term includes a ## Failures section when tests fail."""
    pytester.makepyfile("""
        def test_fails():
            assert False, "intentional failure"
    """)
    result = pytester.runpytest("--llm-report=term")
    assert "## Failures" in result.stdout.str()


def test_term_and_file_modes_together(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=term --llm-report=file both activate without error."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--llm-report=term", "--llm-report=file")
    assert result.ret == 0


def test_term_mode_output_has_no_ansi_codes(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=term output contains no ANSI escape sequences."""
    pytester.makepyfile("""
        def test_fails():
            assert False, "intentional failure"
    """)
    result = pytester.runpytest("--llm-report=term")
    assert not re.search(r"\x1b\[[0-9;]*m", result.stdout.str())


def test_term_mode_verbose_includes_passes_section(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=term -v includes a ## Passes section for passing tests."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--llm-report=term", "-v")
    assert "## Passes" in result.stdout.str()


def test_term_mode_non_verbose_omits_passes_section(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=term without -v omits the ## Passes section."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--llm-report=term")
    assert "## Passes" not in result.stdout.str()


# ---------------------------------------------------------------------------
# Ticket 6 — File output mode
# ---------------------------------------------------------------------------


def test_file_mode_creates_default_report(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=file creates test-results.md in cwd."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--llm-report=file")
    assert result.ret == 0
    assert (pytester.path / "test-results.md").exists()


def test_file_mode_content_matches_markdown(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """File content is valid Markdown with expected summary."""
    pytester.makepyfile("def test_passes(): pass")
    pytester.runpytest("--llm-report=file")
    content = (pytester.path / "test-results.md").read_text()
    assert "1 passed" in content


def test_file_mode_custom_path(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report-file=out/results.md writes to that path, creating parent dirs."""
    pytester.makepyfile("def test_passes(): pass")
    pytester.runpytest("--llm-report=file", "--llm-report-file=out/results.md")
    assert (pytester.path / "out" / "results.md").exists()


def test_file_mode_overwrites_on_second_run(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """Running twice overwrites, not appends."""
    pytester.makepyfile("def test_passes(): pass")
    pytester.runpytest("--llm-report=file")
    pytester.runpytest("--llm-report=file")
    content = (pytester.path / "test-results.md").read_text()
    assert content.count("1 passed") == 1  # not duplicated


def test_file_mode_default_output_unchanged(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=file alone does not suppress pytest's default output."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--llm-report=file")
    assert "=== test session starts ===" in result.stdout.str()


def test_file_mode_prints_confirmation_line(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--llm-report=file prints 'LLM report written to <path>' to stdout."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--llm-report=file")
    assert "LLM report written to" in result.stdout.str()


def test_file_mode_ini_option_respected(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """llm_report_file ini option sets the default output path."""
    pytester.makeini("[pytest]\nllm_report_file = custom-report.md\n")
    pytester.makepyfile("def test_passes(): pass")
    pytester.runpytest("--llm-report=file")
    assert (pytester.path / "custom-report.md").exists()
