# utils

## Folder Cleaner

Folder Cleaner is a Python script designed to find and delete empty folders within a specified directory. It uses multithreading for efficient folder traversal and deletion, and it provides logging capabilities to track operations and errors.

### Features
- Multithreaded Execution: Utilizes ThreadPoolExecutor for concurrent operations, enhancing performance by processing multiple folders simultaneously.
- Logging: Implements logging to capture informational messages, errors, and debug information based on user-defined debug mode.
- Timestamped Output: Saves a list of deleted folders with a timestamp to facilitate tracking and auditing.

### Requirements
Python 3.x
argparse library (typically included with Python standard library)
logging library (included with Python standard library)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/folder-cleaner.git
cd folder-cleaner
```
2. Install dependencies (if any):
```
pip install -r requirements.txt
```
### Usage
```bash
python folder_cleaner.py <path> [-o OUTPUT_FILE] [--debug]
```
Arguments
    <path>: Required. Path to the directory where empty folders will be searched and deleted.
    -o OUTPUT_FILE, --output OUTPUT_FILE: Optional. Output file path for saving the list of deleted folders. Default is output/deleted_folders.txt.
    --debug: Optional flag to enable debug mode. Displays detailed debug messages.

### Example
Find and delete empty folders in C:\Projects directory, enable debug mode, and save deleted folders to logs/deleted_folders.log:
```python
python folder_cleaner.py C:\Projects -o logs/deleted_folders.log --debug
```
### Logging
Logs are generated in the console and optionally in a log file (logs/folder_cleaner.log by default).
Debug mode (--debug) enables detailed logging, including permission errors and folder operations.

### Notes
Ensure proper permissions are set for deleting folders, especially on systems with restricted access.
Use caution when deleting folders as data loss may occur if not used correctly.

# File Extension Utility
This script is designed to append a specified extension to files in a given directory if they don't already have a recognized extension. The default extension to append is `.mp4`, but this can be easily changed.

## Features
- Checks files in a specified directory.
- Appends a target extension (default `.mp4`) to files without a recognized extension.
- Utilizes the Strategy design pattern for handling files with known and unknown extensions.
- Comprehensive error handling for robustness.
- Extensible and maintainable code with detailed comments and type hints.

## Common Extensions
The script recognizes a wide range of common file extensions including but not limited to:
- Document formats: `.pdf`, `.doc`, `.docx`, `.txt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`
- Media formats: `.mp3`, `.mp4`, `.mkv`, `.avi`, `.wav`, `.mov`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tif`, `.tiff`
- Archives and executables: `.zip`, `.rar`, `.tar`, `.gz`, `.iso`, `.exe`, `.msi`
- Web and code files: `.html`, `.css`, `.js`, `.json`, `.xml`, `.sql`, `.py`, `.java`, `.class`, `.jar`
- Configuration and system files: `.ini`, `.cfg`, `.log`, `.bat`, `.dll`, `.sh`, `.bin`, `.key`, `.pem`

## Usage
1. Clone the repository or download the script.
2. Open a terminal and navigate to the directory containing the script.
3. Run the script with the following command:
```bash
python extension_util.py <directory_path>
```
Replace `<directory_path>` with the path to the directory you want to process.

### Example
```bash
python extension_util.py /path/to/directory
```

# License
This project is licensed under the MIT License - see the LICENSE file for details.
