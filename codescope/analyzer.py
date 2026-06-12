import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()


def analyze_project(path, export=None):

    project_path = Path(path)

    total_files = 0
    total_dirs = 0
    total_lines = 0
    todo_count = 0
    function_count = 0
    class_count = 0
    import_count = 0

    extensions = {}
    largest_files = []
    languages = set()

    ignored_dirs = {"venv", "__pycache__", ".git", "node_modules"}

    for item in project_path.rglob("*"):

        if any(part in ignored_dirs for part in item.parts):
            continue

        if item.is_dir():
            total_dirs += 1

        elif item.is_file():

            total_files += 1

            ext = item.suffix.lower()

            if not ext.strip():
                ext = "[no extension]"

            extensions[ext] = extensions.get(ext, 0) + 1
            if ext == ".py":
                languages.add("Python")

            elif ext == ".md":
                languages.add("Markdown")

            elif ext == ".toml":
                languages.add("TOML")

            elif ext == ".js":
                languages.add("JavaScript")

            elif ext == ".java":
                languages.add("Java")

            size = item.stat().st_size
            largest_files.append((size, str(item)))

            try:

                with open(item, "r", encoding="utf-8") as f:

                    lines = f.readlines()

                    total_lines += len(lines)
                    if ext == ".py":

                        for line in lines:

                            stripped = line.strip()

                            if stripped.startswith("def "):
                                function_count += 1

                            elif stripped.startswith("class "):
                                class_count += 1

                            elif stripped.startswith("import ") or stripped.startswith(
                                "from "
                            ):
                                import_count += 1

                    for line in lines:

                        if "TODO" in line or "FIXME" in line:

                            todo_count += 1

            except:
                pass

    largest_files.sort(reverse=True)

    results = {
        "total_files": total_files,
        "total_directories": total_dirs,
        "total_lines": total_lines,
        "todo_count": todo_count,
        "languages": list(languages),
        "python_stats": {
            "functions": function_count,
            "classes": class_count,
            "imports": import_count,
        },
        "extensions": extensions,
    }

    if export:

        with open(export, "w") as f:
            json.dump(results, f, indent=4)

        console.print(f"[bold green]Exported report to {export}[/bold green]")

    table = Table(title="CodeScope Analysis")

    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Files", str(total_files))
    table.add_row("Total Directories", str(total_dirs))
    table.add_row("Total Lines", str(total_lines))
    table.add_row("TODO/FIXME Count", str(todo_count))

    console.print(table)

    ext_table = Table(title="File Types")

    ext_table.add_column("Extension", style="magenta")
    ext_table.add_column("Count", style="yellow")

    for ext, count in sorted(extensions.items()):
        ext_table.add_row(ext, str(count))

    console.print(ext_table)

    largest_table = Table(title="Largest Files")

    largest_table.add_column("Size (bytes)", style="red")
    largest_table.add_column("File", style="blue")

    for size, file in largest_files[:10]:
        largest_table.add_row(str(size), file)

    console.print(largest_table)
    console.print("\n[bold cyan]Languages Detected[/bold cyan]")

    for lang in sorted(languages):
        console.print(f"- {lang}")
    console.print("\n[bold cyan]Python Stats[/bold cyan]")

    console.print(f"- Functions: {function_count}")
    console.print(f"- Classes: {class_count}")
    console.print(f"- Imports: {import_count}")
    return results
