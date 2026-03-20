"""Generate documentation stubs."""

from pathlib import Path
from typing import Set

root_dir = Path(__file__).parent.parent
src_root = root_dir / "pytest_llm_report"
docs_root = root_dir / "docs"
exclude: Set[str] = set()

print(f"Generating {docs_root}")
for path in sorted(src_root.rglob("*.py")):
    module_path = path.relative_to(root_dir).with_suffix("")
    doc_path = path.relative_to(src_root).with_suffix(".md")
    full_doc_path = docs_root / "reference" / "api" / doc_path

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1].startswith("_"):
        continue

    ident = ".".join(parts)
    print(f"Generating {ident} to {doc_path}")
    full_doc_path.parent.mkdir(parents=True, exist_ok=True)
    full_doc_path.write_text(f"::: {ident}")
