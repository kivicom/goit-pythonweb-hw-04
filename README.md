# Asynchronous File Sorting Script

This script reads all files in the specified source folder (recursively) and copies them into corresponding subfolders in the destination folder based on the file extensions. By leveraging asynchronous operations, it efficiently handles large numbers of files.

## Features

- Uses `argparse` to handle command-line arguments (source and destination folder paths).
- Asynchronously reads all files in the source folder (including subfolders).
- Asynchronously copies each file to a subfolder in the destination folder according to its extension.
- Includes logging of errors for better monitoring and troubleshooting.

## Usage

1. Install required libraries (e.g., `asyncio`, `aiopath`, etc.).
2. Run the script from the command line, specifying the source and destination folder paths:
   ```bash
   python sort_files.py --source /path/to/source --destination /path/to/destination
   ```
