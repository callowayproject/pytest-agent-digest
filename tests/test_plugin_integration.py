"""Pytester integration tests for CLI option acceptance (Ticket 2)."""

import pytest


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
