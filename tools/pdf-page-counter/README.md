# 📄 PDF Page Counter

A tool to scan directories or individual files to calculate PDF page counts with beautiful terminal output.

## Features

* **Dynamic Scanning**: Real-time file discovery with a live spinner and counter.
* **Deep Analysis**: Powered by `PyMuPDF` for high-performance page counting.
* **Visual Reports**: Generates clean, formatted, and sortable tables using `rich`.
* **Flexible Targets**: Supports both individual PDF files and recursive directory scanning.
* **Data Export**: Optional export to JSON for further integration or reporting.
* **Smart Progress**: Tracks processing status with a modern progress bar.

## Usage

### Scan a Directory

Recursively find and count pages for all PDFs in a folder:

```bash
python main.py /path/to/your/library
```

### Scan a Single File

Check the page count of a specific document:

```bash
python main.py document.pdf
```

### Export to JSON

Generate a report and save the results to a file:

```bash
python main.py /path/to/pdfs --output report.json
```

### Sorting Logic

The tool automatically sorts the results by **Page Count** in descending order, putting your largest documents at the top of the list.

## Requirements

* `PyMuPDF (fitz)`: High-speed PDF processing.
* `Rich`: Beautiful terminal formatting and progress tracking.
* `Typer`: Intuitive CLI interface.

## Structure Example

The generated table and JSON include:

* `#`: Numerical index
* **File Name**: Name of the PDF file
* **Pages**: Total number of pages
* **Full Path**: Absolute location on your system