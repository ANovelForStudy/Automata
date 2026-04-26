from collections import defaultdict
from pathlib import Path
from shutil import move

import blake3
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

IMAGE_EXTENSIONS: set[str] = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
    ".tiff",
    ".svg",
    ".heic",
}


def get_file_hash(file_path: Path) -> str:
    hasher = blake3.blake3()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


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


@click.command()
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, path_type=Path)
)
@click.option("--recursive", "-r", is_flag=True)
@click.option("--dry-run", is_flag=True)
@click.option("--group", "-g", is_flag=True)
def main(directory: Path, recursive: bool, dry_run: bool, group: bool) -> None:
    pattern = "**/*" if recursive else "*"
    all_files = [
        f
        for f in directory.glob(pattern)
        if f.is_file()
        and f.suffix.lower() in IMAGE_EXTENSIONS
        and "duplicates_found" not in f.parts
    ]

    if not all_files:
        console.print(
            Panel("[yellow]No images found to scan.[/]", title="Status")
        )
        return

    hashes: dict[str, list[Path]] = defaultdict(list)

    with Progress(
        SpinnerColumn(),
        TextColumn("[cyan]Analyzing images (BLAKE3)...[/]"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        hash_task = progress.add_task("Hashing", total=len(all_files))
        for file_path in all_files:
            try:
                file_hash = get_file_hash(file_path)
                hashes[file_hash].append(file_path)
            except (PermissionError, OSError):
                console.print(
                    f"[red]Skip:[/] Access denied to {file_path.name}"
                )
            progress.advance(hash_task)

    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}

    if not duplicates:
        console.print(
            Panel(
                "[bold green]No duplicates found![/] Your library is clean.",
                expand=False,
            )
        )
        return

    if dry_run:
        table = Table(
            title="Dry Run: Duplicates Detected", header_style="bold magenta"
        )
        table.add_column("Original (stays)", style="green")
        table.add_column("Duplicate (will move)", style="yellow")

        for file_paths in duplicates.values():
            original = file_paths[0]
            for dupe in file_paths[1:]:
                table.add_row(
                    str(original.name), str(dupe.relative_to(directory))
                )

        console.print(table)
        return

    dest_root = directory / "duplicates_found"
    moved_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[magenta]Moving duplicates...[/]"),
        console=console,
    ) as progress:
        move_task = progress.add_task(
            "Moving", total=sum(len(p) - 1 for p in duplicates.values())
        )

        for h, file_paths in duplicates.items():
            # Определяем целевую папку: либо по хешу, либо в корень
            target_dir = dest_root / h[:12] if group else dest_root

            for dupe_path in file_paths[1:]:
                target_dir.mkdir(parents=True, exist_ok=True)
                target_file = target_dir / dupe_path.name
                move(dupe_path, get_unique_path(target_file))
                moved_count += 1
                progress.advance(move_task)

    console.print(
        Panel(
            f"[bold green]Done![/] Moved [white]{moved_count}[/] duplicates to [blue]{dest_root.name}/[/]",
            title="Success",
            expand=False,
        )
    )


if __name__ == "__main__":
    main()
