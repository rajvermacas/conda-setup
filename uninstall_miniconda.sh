#!/bin/bash

# Exit on error
set -e

echo "Starting Miniconda uninstallation..."

# Deactivate conda if it's active
if [[ ! -z "${CONDA_DEFAULT_ENV}" ]]; then
    conda deactivate
fi

# Remove Miniconda directory
if [ -d "$HOME/miniconda" ]; then
    rm -rf "$HOME/miniconda"
    echo "Removed Miniconda directory"
else
    echo "Miniconda directory not found in $HOME/miniconda"
fi

# # Remove conda initialization from .bashrc
# if grep -q "conda initialize" ~/.bashrc; then
#     # Create a temporary file without conda initialization
#     sed '/# >>> conda initialize/,/# <<< conda initialize/d' ~/.bashrc > ~/.bashrc.tmp
#     mv ~/.bashrc.tmp ~/.bashrc
#     echo "Removed conda initialization from .bashrc"
# fi

# # Remove conda PATH from .bashrc
# if grep -q "miniconda/bin" ~/.bashrc; then
#     sed -i '/export PATH="$HOME\/miniconda\/bin:$PATH"/d' ~/.bashrc
#     echo "Removed Miniconda PATH from .bashrc"
# fi

echo "Miniconda uninstallation completed successfully!"
echo "Please restart your terminal for the changes to take effect."
