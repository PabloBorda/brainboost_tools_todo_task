#!/bin/bash

# Exit on error
set -e

echo "=== Building Taggy Todo Flatpak package ==="

# Clean previous build
echo "Cleaning previous build..."
rm -rf build-dir

# Build the application
echo "Building the application..."
flatpak-builder build-dir flatpak-manifest.json

# Create/update the local repo
echo "Exporting to local repo..."
mkdir -p repo
flatpak build-export repo build-dir

# Create a Flatpak bundle file
echo "Creating Flatpak bundle..."
flatpak build-bundle repo com.github.subjective_technologies.taggy.flatpak com.github.subjective_technologies.taggy

# Check if reinstall is needed
if [ "$1" == "--install" ]; then
    echo "Uninstalling previous version..."
    flatpak uninstall -y com.github.subjective_technologies.taggy || true
    
    echo "Installing new version..."
    flatpak install --user -y com.github.subjective_technologies.taggy.flatpak
    
    echo "Installation complete. You can run the application with:"
    echo "flatpak run com.github.subjective_technologies.taggy"
fi

echo "=== Build complete ==="
echo "Flatpak bundle created: com.github.subjective_technologies.taggy.flatpak"
echo ""
echo "To install: flatpak install --user com.github.subjective_technologies.taggy.flatpak"
echo "To run: flatpak run com.github.subjective_technologies.taggy" 