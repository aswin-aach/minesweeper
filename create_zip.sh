#!/bin/bash

# Script to create a downloadable ZIP file of the Minesweeper project
# Usage: ./create_zip.sh

# Set variables
PROJECT_NAME="minesweeper"
ZIP_NAME="${PROJECT_NAME}.zip"
WORKSPACE_DIR="/workspaces"
PROJECT_DIR="${WORKSPACE_DIR}/${PROJECT_NAME}"

# Navigate to workspace directory
cd "${WORKSPACE_DIR}" || { echo "Error: Could not navigate to workspace directory"; exit 1; }

# Create the ZIP file, excluding unnecessary files
echo "Creating ${ZIP_NAME}..."
zip -r "${ZIP_NAME}" "${PROJECT_NAME}" \
    -x "${PROJECT_NAME}/.git/*" \
    -x "${PROJECT_NAME}/__pycache__/*" \
    -x "${PROJECT_NAME}/*/__pycache__/*" \
    -x "${PROJECT_NAME}/*/*/__pycache__/*" \
    -x "${PROJECT_NAME}/*/*/*/__pycache__/*"

# Check if ZIP creation was successful
if [ $? -eq 0 ]; then
    echo "ZIP file created successfully at: ${WORKSPACE_DIR}/${ZIP_NAME}"
    echo "File size: $(du -h "${ZIP_NAME}" | cut -f1)"
    echo "To download, right-click on the file in the Explorer and select 'Download'"
else
    echo "Error: Failed to create ZIP file"
    exit 1
fi
