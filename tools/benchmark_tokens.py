"""Benchmark script comparing token counts of normal pytest output vs LLM report output.

Validates the core success metric: ≥20% token reduction vs. raw pytest output.

Usage:
    uv run python tools/benchmark_tokens.py

Requires ANTHROPIC_API_KEY environment variable.
"""

import subprocess
import tempfile
import textwrap
from pathlib import Path

import anthropic

_MODEL = "claude-3-haiku-20240307"

_SAMPLE_TEST_FILE = textwrap.dedent("""\
    def test_addition():
        assert 1 + 1 == 2

    def test_subtraction():
        assert 5 - 3 == 2

    def test_failure():
        assert 1 == 2, "intentional failure"

    def test_string_upper():
        assert "hello".upper() == "HELLO"

    def test_list_length():
        assert len([1, 2, 3]) == 3
""")


def run_pytest(extra_args: list[str], cwd: Path) -> str:
    """Run pytest with the given extra arguments and return combined stdout+stderr.

    Args:
        extra_args: Additional arguments to pass to pytest.
        cwd: Working directory for the subprocess.

    Returns:
        Combined stdout and stderr as a single string.
    """
    result = subprocess.run(
        ["python", "-m", "pytest", *extra_args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr


def count_tokens(text: str) -> int:
    """Count the number of tokens in the given text using the Anthropic API.

    Args:
        text: The text to count tokens for.

    Returns:
        The number of input tokens.
    """
    client = anthropic.Anthropic()
    response = client.messages.count_tokens(
        model=_MODEL,
        messages=[{"role": "user", "content": text}],
    )
    return response.input_tokens


def print_comparison_table(normal: int, llm: int) -> None:
    """Print a comparison table showing token counts and reduction percentage.

    Args:
        normal: Token count for normal pytest output.
        llm: Token count for LLM report output.
    """
    reduction_pct = (normal - llm) / normal * 100 if normal > 0 else 0.0
    status = "PASS" if reduction_pct >= 20.0 else "FAIL"

    print()
    print(f"{'Output Type':<20} {'Tokens':>10}")
    print("-" * 32)
    print(f"{'Normal':<20} {normal:>10,}")
    print(f"{'LLM Report':<20} {llm:>10,}")
    print("-" * 32)
    print(f"{'Reduction':<20} {reduction_pct:>9.1f}%")
    print()
    print(f"Target: ≥20% reduction  →  {status}")
    print()


def main() -> None:
    """Run the benchmark comparing normal pytest output against LLM report output.

    Creates a temporary directory with a sample test file, runs pytest in both
    normal and LLM report modes, counts tokens for each output, and prints a
    comparison table.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        test_file = tmp_path / "test_sample.py"
        test_file.write_text(_SAMPLE_TEST_FILE)

        print("Running normal pytest...")
        normal_output = run_pytest(["test_sample.py", "-v"], tmp_path)

        print("Running pytest with --llm-report=term...")
        llm_output = run_pytest(["test_sample.py", "--llm-report=term"], tmp_path)

    print("Counting tokens via Anthropic API...")
    normal_tokens = count_tokens(normal_output)
    llm_tokens = count_tokens(llm_output)

    print_comparison_table(normal_tokens, llm_tokens)


if __name__ == "__main__":
    main()
