# conda-setup

This project demonstrates how to set up a Conda environment with specific Python and package versions, and run a Python script within that environment.

## Prerequisites

- Linux-based operating system
- Bash shell

## Files

- `main.sh`: Main script to set up the Conda environment and run the Python script
- `install_miniconda.sh`: Script to install Miniconda
- `uninstall_miniconda.sh`: Script to uninstall Miniconda
- `requirements.txt`: List of Python packages and their versions
- `run_me.py`: Python script to be executed in the Conda environment

## Setup

1. Clone this repository or download the files.
2. Make the scripts executable:
   ```
   chmod +x main.sh install_miniconda.sh uninstall_miniconda.sh
   ```

## Usage

1. Run the main script:
   ```
   ./main.sh
   ```
   This script will:
   - Check if Conda is installed, and install Miniconda if necessary
   - Create a Conda environment named "test-conda-env" with Python 2.7
   - Install the required packages specified in `requirements.txt`
   - Run the `run_me.py` script

## Customization

- To change the Conda environment name or Python version, modify the variables in `main.sh`:
  ```bash
  CONDA_ENV_NAME="test-conda-env"
  PYTHON_VERSION="2.7"
  ```
- To modify the required packages, edit `requirements.txt`.

## Uninstallation

To remove Miniconda, run:
```
./uninstall_miniconda.sh
```

## Troubleshooting

If you encounter any issues, ensure that:
- You have sufficient permissions to execute the scripts and install software
- Your system meets the minimum requirements for Miniconda and the specified Python version
- You have a stable internet connection for downloading Miniconda and packages

For further assistance, please open an issue in the project repository.
