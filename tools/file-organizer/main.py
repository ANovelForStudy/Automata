from pathlib import Path
from shutil import move

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Table

console = Console()

GROUPS: dict[str, tuple[str, ...]] = {
    "00-Documents/00-Word": (".docx", ".doc"),
    "00-Documents/01-PDF": (".pdf",),
    "00-Documents/02-Excel": (".xlsx", ".xls"),
    "00-Documents/03-Text": (".txt", ".md"),
    "00-Documents/04-LaTeX": (".tex"),
    "01-Images": (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"),
    "02-Videos": (".mp4", ".mkv", ".mov", ".avi"),
    "03-Music": (".mp3", ".flac", ".wav", ".aac"),
    "04-Archives": (".zip", ".rar", ".7z", ".tar", ".gz"),
    "05-Executables": (".exe", ".msi", ".bin", ".app", ".dmg"),
    "06-Other/00-Fonts": (".ttf", ".otf", ".woff", ".woff2"),
    "06-Other/01-Torrents": (".torrent",),
    "06-Other/02-Scripts": (
        ".py",
        ".js",
        ".cpp",
        ".cs",
        ".go",
        ".sh",
        ".rs",
        ".ts",
    ),
    "06-Other/03-Models": (".blend", ".obj", ".fbx"),
}

MAPPING: dict[str, str] = {
    ext: path for path, exts in GROUPS.items() for ext in exts
}

PROTECTED_PREFIXES: tuple[str, ...] = tuple(
    path.split("/")[0] for path in GROUPS.keys()
)


def get_unique_path(target_path: Path) -> Path:
    if not target_path.exists():
        return target_path

    counter = 1
    while True:
        new_path = target_path.with_name(
            f"{target_path.stem}_{counter}{target_path.suffix}"
        )
        if not new_path.exists():
            return new_path
        counter += 1


def is_already_organized(file: Path, root: Path) -> bool:
    try:
        relative_parts = file.relative_to(root).parts
        return relative_parts[0] in PROTECTED_PREFIXES
    except (ValueError, IndexError):
        return False


@click.command()
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, path_type=Path)
)
@click.option("--recursive", "-r", is_flag=True)
@click.option("--dry-run", is_flag=True)
def main(directory: Path, recursive: bool, dry_run: bool) -> None:
    pattern = "**/*" if recursive else "*"
    all_items = list(directory.glob(pattern))

    files = [
        f
        for f in all_items
        if f.is_file() and not is_already_organized(f, directory)
    ]

    if not files:
        console.print(
            Panel("[yellow]No new files found to organize.[/]", title="Status")
        )
        return

    if dry_run:
        table = Table(
            title="Dry Run: Planned Operations",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Original File", style="dim")
        table.add_column("Target Path", style="cyan")

        for file in files:
            suffix = file.suffix.lower()
            sub_path = MAPPING.get(suffix, "06-Other/04-Misc")
            table.add_row(str(file.relative_to(directory)), sub_path)

        console.print(table)
        console.print(
            f"\n[bold yellow]Total files to move: {len(files)}[/] (No changes applied)"
        )
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None, pulse_style="magenta"),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Organizing files...", total=len(files))

        for file in files:
            suffix = file.suffix.lower()
            sub_path = MAPPING.get(suffix, "06-Other/04-Misc")

            target_dir = directory / sub_path
            target_file = target_dir / file.name

            target_dir.mkdir(parents=True, exist_ok=True)
            safe_target = get_unique_path(target_file)
            move(file, safe_target)

            progress.advance(task)

    console.print(
        Panel(
            f"[bold green]Success![/] Organized [white]{len(files)}[/] files in [blue]{directory}[/]",
            expand=False,
        )
    )


if __name__ == "__main__":
    main()
