#!/bin/bash

# Script: print_project_contents.sh
# Description: Prints the contents of all relevant project files with headers.

# Define the list of files to include
FILES=(
    "board.py"
    "gpt.txt"
    "main.py"
    "pieces.py"
    "README.md"
    "requirements.txt"
    "run_tests.sh"
    "test.py"
    "utils.py"
)

# Iterate over each file
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "===== $file ====="
        cat "$file"
        echo -e "\n\n"
    else
        echo "===== $file ====="
        echo "File does not exist."
        echo -e "\n\n"
    fi
done
