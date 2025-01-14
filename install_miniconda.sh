#!/bin/bash

# Exit on error
set -e

# Check if Miniconda is already installed
if [ -d "$HOME/miniconda" ]; then
    echo "Miniconda is already installed in $HOME/miniconda"
    echo "Please uninstall it first if you want to reinstall"
    exit 1
fi

echo "Starting Miniconda installation..."

# Download the latest Miniconda installer for Linux
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

# Make the installer executable
chmod +x miniconda.sh

# Install Miniconda silently, accepting defaults
./miniconda.sh -b -p $HOME/miniconda

# Remove the installer
rm miniconda.sh

# Initialize conda for bash shell
eval "$($HOME/miniconda/bin/conda shell.bash hook)"

# Add conda to PATH
echo 'export PATH="$HOME/miniconda/bin:$PATH"' >> ~/.bashrc

# Update conda to the latest version
# conda update -n base -c defaults conda -y

echo "Miniconda installation completed successfully!"
# echo "Please restart your terminal or run 'source ~/.bashrc' to start using conda."

source ~/.bashrc
