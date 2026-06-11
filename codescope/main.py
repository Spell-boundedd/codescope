import typer
from rich import print
from analyzer import analyze_project

app = typer.Typer()

def analyze(path: str = "."):
    """
    Analyze a project folder.
    """

    print(f"[bold blue]Analyzing:[/bold blue] {path}")

    analyze_project(path)

def version():
    """
    Show application version.
    """

    print("[bold green]CodeScope v1.0[/bold green]")

app.command()(analyze)
app.command()(version)

if __name__ == "__main__":
    app()