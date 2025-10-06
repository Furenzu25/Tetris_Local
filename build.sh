#!/bin/bash
# Build script for macOS/Linux

echo "========================================"
echo "  Building Tetris for $(uname -s)"
echo "========================================"
echo ""

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install -q -r requirements-dev.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies"
    exit 1
fi

# Run build script
echo ""
echo "Building executable..."
python3 build.py

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "  Build Complete!"
    echo "========================================"
    echo ""
    echo "The executable is in the 'dist' folder"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "File: Tetris_Launcher.app"
    else
        echo "File: Tetris_Launcher"
    fi
    
    echo ""
    echo "You can now share this file with your friends!"
    echo "No Python installation needed to run it."
    echo ""
else
    echo ""
    echo "Build failed!"
    exit 1
fi

