from pathlib import Path


def collect_python_files(project_dir: str, output_file: str = "project codes.txt"):
    project_path = Path(project_dir)
    src_path = project_path / "src"
    output_path = project_path / output_file

    with output_path.open("w", encoding="utf-8") as output:
        for py_file in src_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            if py_file.resolve() == Path(__file__).resolve():
                continue

            relative_path = py_file.relative_to(project_path)

            output.write(f"# {relative_path}\n")
            output.write(py_file.read_text(encoding="utf-8"))
            output.write("\n\n")


if __name__ == "__main__":
    collect_python_files(".")