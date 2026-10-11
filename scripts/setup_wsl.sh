#!/bin/bash

# Exit on error
set -e

echo "Starting Ubuntu WSL setup for skbase..."

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install necessary system dependencies
echo "Installing python3-venv and python3-pip..."
sudo apt install -y python3-venv python3-pip

# Create virtual environment
if [ ! -d ".venv_wsl" ]; then
    echo "Creating virtual environment .venv_wsl..."
    python3 -m venv .venv_wsl
else
    echo ".venv_wsl already exists, skipping creation."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv_wsl/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install skbase in editable mode with development and test dependencies
echo "Installing skbase with [dev,test] dependencies..."
pip install -e ".[dev,test]"

echo "Setup complete! To activate the environment, run: source .venv_wsl/bin/activate"
