# 🛠️📦 Automata

A modular collection of modern Python utilities for system automation and developer workflows.

### Core Principles
* **Modern Stack**: Built with Python 3.12+, utilizing `uv` for lightning-fast environment management.
* **Elegant CLI**: Informative terminal output powered by `Rich` and `Click`.

### Project Structure
This repository is managed as a monorepo. Each tool resides in its own directory within `tools/` with independent dependency management via `uv`.

### Quick Start
```bash
git clone https://github.com/ANovelForStudy/Automata.git
cd automata
uv run tools/file-organizer/main.py --help
