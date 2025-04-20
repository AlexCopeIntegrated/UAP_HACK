#!/bin/bash
# Script to build the rtlsdr-tool binary executable

# Exit on error
set -e

# Detect macOS
if [[ "$(uname)" == "Darwin" ]]; then
    echo "Detected macOS. Using Docker for cross-compilation to Raspberry Pi..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "Docker is required for cross-compilation but not found."
        echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"
        exit 1
    fi
    
    # Create a Dockerfile for cross-compilation
    cat > Dockerfile.rpi << EOF
FROM python:3.9-slim-buster

# Install dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    libusb-1.0-0-dev \\
    upx-ucl

# Create working directory
WORKDIR /app

# Copy the application files
COPY . /app/

# Install Python dependencies
RUN pip install -e .
RUN pip install pyinstaller

# Build the binary
RUN pyinstaller rtlsdr_tool.spec --clean

# Fix permissions
RUN chmod +x dist/rtlsdr-tool
EOF

    # Build the Docker image
    echo "Building Docker image for Raspberry Pi cross-compilation..."
    docker build -t rtlsdr-tool-builder -f Dockerfile.rpi .
    
    # Create output directory if it doesn't exist
    mkdir -p dist
    
    # Extract the binary from the container
    echo "Extracting binary from Docker container..."
    docker create --name rtlsdr-tool-container rtlsdr-tool-builder
    docker cp rtlsdr-tool-container:/app/dist/rtlsdr-tool dist/
    docker rm rtlsdr-tool-container
    
    echo "Cross-compilation complete! Binary executable is available at dist/rtlsdr-tool"
    echo "Note: This binary is compiled for Raspberry Pi ARM architecture and won't run on macOS."
    echo "Copy this binary to your Raspberry Pi and run it without Python installed."

else
    # Original build process for Raspberry Pi
    
    # Check if PyInstaller is installed, if not install it
    pip show pyinstaller > /dev/null 2>&1 || pip install pyinstaller

    # Install UPX for compression if not already installed
    if ! command -v upx &> /dev/null; then
        echo "UPX not found, installing..."
        # For Raspberry Pi (Debian/Raspbian)
        if [[ -f /etc/debian_version ]]; then
            sudo apt-get update
            sudo apt-get install -y upx-ucl
        else
            echo "UPX not automatically installed. Please install manually for better compression."
        fi
    fi

    # Install the package in development mode
    pip install -e .

    # Build the binary using PyInstaller
    pyinstaller rtlsdr_tool.spec --clean

    # Make the binary executable
    chmod +x dist/rtlsdr-tool

    echo "Build complete! Binary executable is available at dist/rtlsdr-tool"
    echo "You can copy this binary to any compatible Raspberry Pi and run it without Python installed."
fi 