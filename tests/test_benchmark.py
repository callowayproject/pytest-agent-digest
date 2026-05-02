"""Tests for tools/benchmark_tokens.py."""

import sys
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import MagicMock, patch

# Add tools/ to sys.path so we can import benchmark_tokens
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
import benchmark_tokens


def test_run_pytest_returns_string():
    """run_pytest returns a str combining stdout and stderr."""
    fake_result = CompletedProcess(args=[], returncode=0, stdout="hello\n", stderr="warn\n")
    with patch("benchmark_tokens.subprocess.run", return_value=fake_result) as mock_run:
        result = benchmark_tokens.run_pytest(["--version"], Path("/tmp"))  # noqa: S108
    assert isinstance(result, str)
    assert "hello" in result
    mock_run.assert_called_once()


def test_count_tokens_calls_anthropic():
    """count_tokens calls the Anthropic API with the correct shape and returns input_tokens."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.input_tokens = 42
    mock_client.messages.count_tokens.return_value = mock_response

    with patch("benchmark_tokens.anthropic.Anthropic", return_value=mock_client):
        result = benchmark_tokens.count_tokens("some test output")

    assert result == 42
    mock_client.messages.count_tokens.assert_called_once()
    call_kwargs = mock_client.messages.count_tokens.call_args
    # Verify messages kwarg has the text content
    messages = call_kwargs.kwargs.get("messages") or call_kwargs.args[1]
    assert any("some test output" in str(m) for m in messages)


def test_print_comparison_table_shows_reduction(capsys):
    """print_comparison_table outputs columns for Normal, LLM Report, and Reduction."""
    benchmark_tokens.print_comparison_table(1000, 750)
    captured = capsys.readouterr()
    assert "Normal" in captured.out
    assert "LLM Report" in captured.out
    assert "Reduction" in captured.out


def test_print_comparison_table_pass_when_over_20pct(capsys):
    """print_comparison_table shows PASS when reduction is >= 20%."""
    benchmark_tokens.print_comparison_table(1000, 700)  # 30% reduction
    captured = capsys.readouterr()
    assert "PASS" in captured.out


def test_print_comparison_table_fail_when_under_20pct(capsys):
    """print_comparison_table shows FAIL when reduction is < 20%."""
    benchmark_tokens.print_comparison_table(1000, 900)  # 10% reduction
    captured = capsys.readouterr()
    assert "FAIL" in captured.out


def test_main_end_to_end():
    """main() calls run_pytest twice, count_tokens twice, and print_comparison_table once."""
    with (
        patch("benchmark_tokens.run_pytest", side_effect=["normal output", "llm output"]) as mock_run,
        patch("benchmark_tokens.count_tokens", side_effect=[500, 350]) as mock_count,
        patch("benchmark_tokens.print_comparison_table") as mock_table,
    ):
        benchmark_tokens.main()

    assert mock_run.call_count == 2
    assert mock_count.call_count == 2
    mock_table.assert_called_once_with(500, 350)
