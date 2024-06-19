# utils

Folder Cleaner

Folder Cleaner is a Python script designed to find and delete empty folders within a specified directory. It uses multithreading for efficient folder traversal and deletion, and it provides logging capabilities to track operations and errors.
Features

    Multithreaded Execution: Utilizes ThreadPoolExecutor for concurrent operations, enhancing performance by processing multiple folders simultaneously.
    Logging: Implements logging to capture informational messages, errors, and debug information based on user-defined debug mode.
    Timestamped Output: Saves a list of deleted folders with a timestamp to facilitate tracking and auditing.

Requirements

    Python 3.x
    argparse library (typically included with Python standard library)
    logging library (included with Python standard library)

Installation

    Clone the repository:

    ```bash

git clone https://github.com/yourusername/folder-cleaner.git
cd folder-cleaner
```
Install dependencies (if any):
```
    pip install -r requirements.txt
```
Usage

```css

python folder_cleaner.py <path> [-o OUTPUT_FILE] [--debug]
```
Arguments

    <path>: Required. Path to the directory where empty folders will be searched and deleted.
    -o OUTPUT_FILE, --output OUTPUT_FILE: Optional. Output file path for saving the list of deleted folders. Default is output/deleted_folders.txt.
    --debug: Optional flag to enable debug mode. Displays detailed debug messages.

Example

Find and delete empty folders in C:\Projects directory, enable debug mode, and save deleted folders to logs/deleted_folders.log:

```lua

python folder_cleaner.py C:\Projects -o logs/deleted_folders.log --debug
```
Logging

    Logs are generated in the console and optionally in a log file (logs/folder_cleaner.log by default).
    Debug mode (--debug) enables detailed logging, including permission errors and folder operations.

Notes

    Ensure proper permissions are set for deleting folders, especially on systems with restricted access.
    Use caution when deleting folders as data loss may occur if not used correctly.

License

This project is licensed under the MIT License - see the LICENSE file for details.
