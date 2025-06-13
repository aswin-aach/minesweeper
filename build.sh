#!/bin/bash
# Simple wrapper script for building Minesweeper executable

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Run the build script
echo "Running build script..."
python build_executable.py

# Exit with the same status as the build script
exit $?
