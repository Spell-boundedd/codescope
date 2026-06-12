from importlib.resources import path

import typer
from rich import print
from codescope.analyzer import analyze_project

app = typer.Typer()


@app.command()
def analyze(path: str = ".", export: str = None):
    print(f"[bold blue]Analyzing folder:[/bold blue] {path}")
    analyze_project(path, export)


@app.command()
def version():
    print("[bold green]CodeScope v1.0[/bold green]")


if __name__ == "__main__":
    app()
