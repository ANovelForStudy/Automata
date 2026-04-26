# 📂 File Organizer

A lightweight CLI tool to automatically organize files into a structured directory hierarchy based on file extensions.

## Features
- **Smart Grouping**: Categorizes files into Documents, Images, Videos, Music, Archives, and more.
- **Dry Run Mode**: Preview all operations before any files are moved.
- **Safety First**: Automatically renames files if a collision occurs (no data loss).
- **Non-destructive**: Skips files that are already inside the organized structure.
- **Modern Stack**: Built with `pathlib`, `click`, and `rich`.

## Usage

### Basic organization
Organize the current directory:
```bash
python main.py .
```

### Recursive organization
Organize the current directory and all subdirectories:
```bash
python main.py . --recursive
```

### Preview changes (Dry Run)
See what would happen without moving any files:
```bash
python main.py . --dry-run
```

### Structure Example
- `00-Documents`: Word, PDF, Excel, Text
- `01-Images`
- `02-Videos`
- `03-Music`
- `04-Archives`
- `05-Executables`
- `06-Other`: Fonts, Torrents, Scripts, Models
