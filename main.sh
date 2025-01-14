#!/bin/bash

# Exit on error
set -e

# Configuration variables
CONDA_ENV_NAME="test-conda-env"
PYTHON_VERSION="2.7"

# Function to check if conda command is available
check_conda() {
    if command -v conda >/dev/null 2>&1; then
        echo "Conda is already installed"
        return 0
    else
        echo "Conda is not installed"
        return 1
    fi
}

# Function to check if environment exists
check_env() {
    if conda env list | grep -q "^$CONDA_ENV_NAME "; then
        echo "Environment $CONDA_ENV_NAME already exists"
        return 0
    else
        echo "Environment $CONDA_ENV_NAME does not exist"
        return 1
    fi
}

# Check and install Miniconda if needed
if ! check_conda; then
    echo "Installing Miniconda..."
    ./install_miniconda.sh
    source ~/.bashrc
fi

# Initialize conda for shell
eval "$(conda shell.bash hook)"

# Check and create conda environment if needed
if ! check_env; then
    echo "Creating conda environment $CONDA_ENV_NAME with Python $PYTHON_VERSION..."
    conda create -n $CONDA_ENV_NAME python=$PYTHON_VERSION -y
fi

# Activate environment and install requirements if needed
echo "Activating environment $CONDA_ENV_NAME..."
conda activate $CONDA_ENV_NAME

# Check if requirements are already installed
if ! pip freeze | grep -q "numpy==1.16.6"; then
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "Requirements already installed"
fi

# Run the Python script
echo "Running run_me.py..."
python run_me.py
