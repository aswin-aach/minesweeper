#!/usr/bin/env python3
"""
Build script for creating Minesweeper executable
This script automates the process of building the Minesweeper executable
using PyInstaller with the appropriate settings.
"""

import os
import sys
import shutil
import subprocess
import platform

def clean_build():
    """Clean previous build artifacts"""
    print("Cleaning previous build artifacts...")
    
    # Directories to clean
    dirs_to_clean = ['build', 'dist']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name} directory...")
            shutil.rmtree(dir_name)
    
    # Remove spec file if it exists
    spec_file = 'Minesweeper.spec'
    if os.path.exists(spec_file):
        print(f"Removing {spec_file}...")
        os.remove(spec_file)

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building Minesweeper executable...")
    
    # Determine icon path based on platform
    icon_path = os.path.join('assets', 'mine.ico')
    
    # Base command
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name', 'Minesweeper',
        '--clean',
    ]
    
    # Add icon if platform supports it
    if platform.system() in ('Windows', 'Darwin'):
        cmd.extend(['--icon', icon_path])
    
    # Add main script
    cmd.append('main.py')
    
    # Execute PyInstaller
    print("Running PyInstaller with command:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    
    print("\nBuild completed successfully!")
    print(f"Executable created in: {os.path.abspath('dist')}")

def copy_assets():
    """Copy any additional assets needed for distribution"""
    print("Copying additional assets for distribution...")
    
    # Create assets directory in dist if it doesn't exist
    dist_assets = os.path.join('dist', 'assets')
    if not os.path.exists(dist_assets):
        os.makedirs(dist_assets)
    
    # Copy README and other documentation
    for doc_file in ['README.md', 'spec.md']:
        if os.path.exists(doc_file):
            shutil.copy(doc_file, 'dist')
            print(f"Copied {doc_file} to dist directory")

def create_distribution_package():
    """Create a zip file for distribution"""
    print("Creating distribution package...")
    
    # Get system info for filename
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Create zip filename
    zip_filename = f"minesweeper_{system}_{machine}.zip"
    
    # Change to dist directory
    os.chdir('dist')
    
    # Create zip file
    shutil.make_archive(
        os.path.splitext(zip_filename)[0],  # Base name
        'zip',                              # Format
        '.',                                # Root directory
        '.'                                 # Base directory
    )
    
    # Move back to original directory
    os.chdir('..')
    
    print(f"Distribution package created: dist/{zip_filename}")

def main():
    """Main build process"""
    print("=== Minesweeper Build Script ===")
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    build_executable()
    
    # Copy assets
    copy_assets()
    
    # Create distribution package
    create_distribution_package()
    
    print("\nBuild process completed successfully!")
    print("You can find the executable and distribution package in the 'dist' directory.")

if __name__ == "__main__":
    main()
