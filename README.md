# Minesweeper

A classic Minesweeper clone based on the Windows 7 style, implemented in Python using Tkinter.

## Overview

This project recreates the classic Minesweeper game with a 16x16 grid containing 40 mines, mimicking the Windows 7 visual style. It's developed for Linux desktop environments.

## Features

- 16x16 grid with 40 randomly placed mines
- Timer to track game duration
- Mine counter showing remaining unflagged mines
- Flagging capability to mark suspected mines
- Reset button with smiley face
- High score board tracking player name, date, and completion time

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd minesweeper

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Development

This project follows test-driven development principles. To run tests:

```bash
pytest
```

## License

[MIT](LICENSE)
