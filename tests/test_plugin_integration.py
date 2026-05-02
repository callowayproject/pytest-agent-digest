"""Pytester integration tests for CLI option acceptance (Tickets 2, 5)."""

import re

import pytest

# ---------------------------------------------------------------------------
# Ticket 2 — CLI option acceptance
# ---------------------------------------------------------------------------


def test_agent_digest_term_collection(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=term exits 0 during collection."""
    pytester.makepyfile("def test_dummy(): pass")
    result = pytester.runpytest("--agent-digest=term", "--co", "-q")
    assert result.ret == 0


def test_agent_digest_file_collection(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=file exits 0 during collection."""
    pytester.makepyfile("def test_dummy(): pass")
    result = pytester.runpytest("--agent-digest=file", "--co", "-q")
    assert result.ret == 0


def test_agent_digest_both_collection(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=term --agent-digest=file exits 0 during collection."""
    pytester.makepyfile("def test_dummy(): pass")
    result = pytester.runpytest("--agent-digest=term", "--agent-digest=file", "--co", "-q")
    assert result.ret == 0


def test_agent_digest_invalid_value(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=bad exits non-zero (invalid choice)."""
    pytester.makepyfile("def test_dummy(): pass")
    result = pytester.runpytest("--agent-digest=bad", "--co", "-q")
    assert result.ret != 0


# ---------------------------------------------------------------------------
# Ticket 5 — Terminal output mode
# ---------------------------------------------------------------------------


def test_term_mode_prints_markdown_summary(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=term prints a Markdown summary line to stdout."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--agent-digest=term")
    assert result.ret == 0
    assert "1 passed" in result.stdout.str()


def test_term_mode_suppresses_default_reporter(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=term suppresses pytest's default session header from stdout."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--agent-digest=term")
    assert "=== test session starts ===" not in result.stdout.str()


def test_without_term_mode_default_output_is_unchanged(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """Without --agent-digest=term, pytest's default terminal output is present."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest()
    assert "=== test session starts ===" in result.stdout.str()


def test_term_mode_includes_failures_section(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=term includes a ## Failures section when tests fail."""
    pytester.makepyfile("""
        def test_fails():
            assert False, "intentional failure"
    """)
    result = pytester.runpytest("--agent-digest=term")
    assert "## Failures" in result.stdout.str()


def test_term_and_file_modes_together(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=term --agent-digest=file both activate without error."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--agent-digest=term", "--agent-digest=file")
    assert result.ret == 0


def test_term_mode_output_has_no_ansi_codes(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=term output contains no ANSI escape sequences."""
    pytester.makepyfile("""
        def test_fails():
            assert False, "intentional failure"
    """)
    result = pytester.runpytest("--agent-digest=term")
    assert not re.search(r"\x1b\[[0-9;]*m", result.stdout.str())


def test_term_mode_verbose_includes_passes_section(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=term -v includes a ## Passes section for passing tests."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--agent-digest=term", "-v")
    assert "## Passes" in result.stdout.str()


def test_term_mode_non_verbose_omits_passes_section(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=term without -v omits the ## Passes section."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--agent-digest=term")
    assert "## Passes" not in result.stdout.str()


# ---------------------------------------------------------------------------
# Ticket 6 — File output mode
# ---------------------------------------------------------------------------


def test_file_mode_creates_default_report(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=file creates test-results.md in cwd."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--agent-digest=file")
    assert result.ret == 0
    assert (pytester.path / "test-results.md").exists()


def test_file_mode_content_matches_markdown(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """File content is valid Markdown with expected summary."""
    pytester.makepyfile("def test_passes(): pass")
    pytester.runpytest("--agent-digest=file")
    content = (pytester.path / "test-results.md").read_text()
    assert "1 passed" in content


def test_file_mode_custom_path(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest-file=out/results.md writes to that path, creating parent dirs."""
    pytester.makepyfile("def test_passes(): pass")
    pytester.runpytest("--agent-digest=file", "--agent-digest-file=out/results.md")
    assert (pytester.path / "out" / "results.md").exists()


def test_file_mode_overwrites_on_second_run(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """Running twice overwrites, not appends."""
    pytester.makepyfile("def test_passes(): pass")
    pytester.runpytest("--agent-digest=file")
    pytester.runpytest("--agent-digest=file")
    content = (pytester.path / "test-results.md").read_text()
    assert content.count("1 passed") == 1  # not duplicated


def test_file_mode_default_output_unchanged(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=file alone does not suppress pytest's default output."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--agent-digest=file")
    assert "=== test session starts ===" in result.stdout.str()


def test_file_mode_prints_confirmation_line(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=file prints 'Agent digest written to <path>' to stdout."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--agent-digest=file")
    assert "Agent digest written to" in result.stdout.str()


def test_file_mode_ini_option_respected(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """agent_digest_file ini option sets the default output path."""
    pytester.makeini("[pytest]\nagent_digest_file = custom-report.md\n")
    pytester.makepyfile("def test_passes(): pass")
    pytester.runpytest("--agent-digest=file")
    assert (pytester.path / "custom-report.md").exists()


# ---------------------------------------------------------------------------
# Ticket 7 — Additional integration tests
# ---------------------------------------------------------------------------


def test_tb_no_omits_traceback_block(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--tb=no suppresses the traceback code block in failure entries."""
    pytester.makepyfile("""
        def test_fails():
            assert False, "intentional failure"
    """)
    result = pytester.runpytest("--agent-digest=term", "--tb=no")
    stdout = result.stdout.str()
    assert "## Failures" in stdout
    assert "```" not in stdout  # no code block when tb=no


def test_empty_session_no_crash(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """An empty test session produces a graceful report without crashing."""
    pytester.makepyfile("")  # no test functions
    result = pytester.runpytest("--agent-digest=term", "--collect-only")
    assert result.ret in (0, 5)  # no crash (5 = no tests collected)


def test_mixed_outcomes_section_order(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """Mixed outcomes: ## Failures appears before ## Skipped, ## Skipped before ## Passes."""
    pytester.makepyfile("""
        import pytest

        def test_passes():
            pass

        def test_fails():
            assert False, "intentional failure"

        @pytest.mark.skip(reason="skipped test")
        def test_skipped():
            pass
    """)
    result = pytester.runpytest("--agent-digest=term", "-v")
    stdout = result.stdout.str()
    failures_pos = stdout.find("## Failures")
    skipped_pos = stdout.find("## Skipped")
    passes_pos = stdout.find("## Passes")
    assert failures_pos != -1
    assert skipped_pos != -1
    assert passes_pos != -1
    assert failures_pos < skipped_pos < passes_pos


def test_term_and_file_both_produce_output(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """--agent-digest=term --agent-digest=file produces both stdout markdown and a file."""
    pytester.makepyfile("def test_passes(): pass")
    result = pytester.runpytest("--agent-digest=term", "--agent-digest=file")
    assert result.ret == 0
    assert "1 passed" in result.stdout.str()  # term output
    assert (pytester.path / "test-results.md").exists()  # file output


# ---------------------------------------------------------------------------
# Warnings collection
# ---------------------------------------------------------------------------


def test_warnings_section_in_term_output(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """Warnings emitted during a test appear in the ## Warnings section."""
    pytester.makepyfile("""
        import warnings
        def test_with_warning():
            warnings.warn("old API", DeprecationWarning)
            assert True
    """)
    result = pytester.runpytest("--agent-digest=term")
    assert result.ret == 0
    stdout = result.stdout.str()
    assert "## Warnings" in stdout
    assert "DeprecationWarning" in stdout
    assert "old API" in stdout
    assert "1 warning" in stdout


def test_warnings_count_in_summary(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """Warning count appears in the summary line alongside test outcome counts."""
    pytester.makepyfile("""
        import warnings
        def test_a():
            warnings.warn("w1", UserWarning)
        def test_b():
            warnings.warn("w2", UserWarning)
    """)
    result = pytester.runpytest("--agent-digest=term")
    assert result.ret == 0
    first_line = result.stdout.str().splitlines()[0]
    assert "warnings" in first_line


def test_no_warnings_section_when_no_warnings(pytester: pytest.Pytester) -> None:  # type: ignore[name-defined]
    """## Warnings section is absent when the test suite emits no warnings."""
    pytester.makepyfile("def test_clean(): assert True")
    result = pytester.runpytest("--agent-digest=term")
    assert result.ret == 0
    assert "## Warnings" not in result.stdout.str()
