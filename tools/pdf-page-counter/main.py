import json
from pathlib import Path
from typing import Annotated, Optional

import pymupdf
from rich.console import Console
from rich.progress import track
from rich.table import Table
from typer import Argument, Option, Typer

console = Console()

app = Typer(
    add_completion=False,
)


def find_pdf_files(target_path: Path) -> list[Path]:
    if not target_path.exists():
        console.print(
            f"[bold red]Error:[/bold red] Path {target_path} does not exist."
        )
        return []

    if target_path.is_file():
        if target_path.suffix.lower() == ".pdf":
            return [target_path]
        else:
            console.print(
                f"[bold yellow]Warning:[/bold yellow] {target_path.name} is not a PDF file."
            )
            return []

    pdf_files = []
    with console.status(
        "[bold green]Scanning directory for PDFs...", spinner="dots"
    ) as status:
        for file in target_path.rglob("*.pdf"):
            pdf_files.append(file)
            status.update(
                f"[bold green]Scanning... Found [cyan]{len(pdf_files)}[/cyan] files"
            )

    return pdf_files


def get_pdf_info(pdf_paths: list[Path]) -> list[dict]:
    results = []
    description = "[blue]Processing PDF pages..."
    iterator = (
        track(pdf_paths, description=description)
        if len(pdf_paths) > 1
        else pdf_paths
    )

    for file_path in iterator:
        try:
            with pymupdf.open(file_path) as doc:
                page_count = doc.page_count

            results.append(
                {
                    "name": file_path.name,
                    "pages": page_count,
                    "path": str(file_path.absolute()),
                }
            )
        except Exception as e:
            console.print(f"[red]Could not read {file_path.name}: {e}[/red]")

    return results


def display_table(data: list[dict]):
    table = Table(
        title="PDF Page Count Report",
        header_style="bold magenta",
        show_lines=True,
    )

    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("File Name", style="green")
    table.add_column("Pages", justify="center", style="bold yellow")
    table.add_column("Full Path", style="dim")

    sorted_data = sorted(data, key=lambda x: x["pages"], reverse=True)

    for i, item in enumerate(sorted_data, 1):
        table.add_row(str(i), item["name"], str(item["pages"]), item["path"])

    console.print(table)


def save_to_json(data: list[dict], output_path: Path):
    sorted_data = sorted(data, key=lambda x: x["pages"], reverse=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, indent=4, ensure_ascii=False)

    console.print(f"\n[bold blue]Report saved to:[/bold blue] {output_path}")


@app.command()
def main(
    target_path: Annotated[
        Path,
        Argument(help="Path to a PDF file or directory to scan"),
    ],
    output: Annotated[
        Optional[Path],
        Option(
            "--output", "-o", help="Optional path to save the report as JSON"
        ),
    ] = None,
):
    pdf_paths = find_pdf_files(target_path=target_path)

    if not pdf_paths:
        console.print("[yellow]No PDF files found to process.[/yellow]")
        return

    pdf_info = get_pdf_info(pdf_paths)

    if pdf_info:
        display_table(pdf_info)
        if output:
            save_to_json(pdf_info, output)


if __name__ == "__main__":
    app()
