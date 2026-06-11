from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def analyze_project(path):

    project_path = Path(path)

    total_files = 0
    todo_count = 0
    total_lines = 0
    total_dirs = 0
    total_lines = 0
    todo_count = 0

    extensions = {}
    largest_files = []

    ignored_dirs = {
        "venv",
        "__pycache__",
        ".git",
        "node_modules"
    }

    for item in project_path.rglob("*"):

        if any(part in ignored_dirs for part in item.parts):
            continue

        if item.is_dir():
            total_dirs += 1

        elif item.is_file():

            total_files += 1
            try:
                with open(item, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                    total_lines += len(lines)

                    for line in lines:

                        if "TODO" in line or "FIXME" in line:
                            todo_count += 1

            except:
                pass
            ext = item.suffix.lower()

            if ext == "":
                ext = "[no extension]"

            extensions[ext] = extensions.get(ext, 0) + 1

            size = item.stat().st_size
            largest_files.append((size, str(item)))

            try:

                with open(item, "r", encoding="utf-8") as f:

                    lines = f.readlines()

                    total_lines += len(lines)

                    for line in lines:

                        if "TODO" in line or "FIXME" in line:
                            todo_count += 1

            except:
                pass

    largest_files.sort(reverse=True)

    table = Table(title="CodeScope Analysis")

    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("Total Files", str(total_files))
    table.add_row("Total Directories", str(total_dirs))
    table.add_row("Total Lines", str(total_lines))
    table.add_row("TODO/FIXME Count", str(todo_count))

    console.print(table)

    ext_table = Table(title="File Types")

    ext_table.add_column("Extension")
    ext_table.add_column("Count")

    for ext, count in sorted(extensions.items()):
        ext_table.add_row(ext, str(count))

    console.print(ext_table)

    largest_table = Table(title="Largest Files")

    largest_table.add_column("Size (bytes)")
    largest_table.add_column("File")

    for size, file in largest_files[:10]:
        largest_table.add_row(str(size), file)

    console.print(largest_table)