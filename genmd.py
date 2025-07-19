import sys
import csv
from pathlib import Path


def read_csv_as_md_table(csv_path: Path) -> str:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return "_No data available._"

    header = rows[0]
    body = rows[1:]

    lines = ["| " + " | ".join(header) + " |"]
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    for row in body:
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


def inject_table(template: str, table: str) -> str:
    start_tag = "<!-- TABLE_START -->"
    end_tag = "<!-- TABLE_END -->"

    if start_tag not in template or end_tag not in template:
        raise ValueError(
            "Template must contain <!-- TABLE_START --> and <!-- TABLE_END -->"
        )

    before = template.split(start_tag)[0] + start_tag + "\n\n"
    after = "\n\n" + end_tag + template.split(end_tag)[1]
    return before + table + after


def generate_md(subfolder_name: str, template_name: str):
    proj_root = Path(__file__).resolve().parent
    benchmarks_dir = proj_root / "benchmarks"
    template_dir = proj_root / "template"

    benchmark_folder = benchmarks_dir / subfolder_name
    template_file = template_dir / template_name
    csv_file = benchmark_folder / "results.csv"
    output_md = benchmark_folder / "README.md"

    if not benchmark_folder.exists():
        raise FileNotFoundError(f"Benchmark folder not found: {benchmark_folder}")
    if not csv_file.exists():
        raise FileNotFoundError(f"Missing results.csv: {csv_file}")
    if not template_file.exists():
        raise FileNotFoundError(f"Missing template: {template_file}")

    table = read_csv_as_md_table(csv_file)
    template_text = template_file.read_text(encoding="utf-8")
    final_output = inject_table(template_text, table)
    output_md.write_text(final_output, encoding="utf-8")

    print(f"[I] README.md generated at: {output_md.relative_to(proj_root)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python genmd.py <benchmark-subfolder> <template-name>")
        sys.exit(1)

    folder = sys.argv[1]
    template = sys.argv[2]

    try:
        generate_md(folder, template)
    except Exception as e:
        print(f"[E] {e}")
        sys.exit(1)
