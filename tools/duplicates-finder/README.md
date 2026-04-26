# 🖼️ Duplicate Image Finder

A high-performance CLI tool to isolate duplicate images using the BLAKE3 hashing algorithm.

## Features
- **Ultra-fast hashing**: Powered by `blake3`.
- **Flexible Sorting**: Moves duplicates to a single folder by default, or groups them by hash using a flag.
- **Safety First**: No files are deleted. Renames files automatically on name collisions.
- **Dry Run**: Preview results before moving files.

## Usage

### Run simple scan
Duplicates will be moved to `duplicates_found/`:
```bash
python main.py /path/to/images
```