# mini-file

A simple demonstration of file management operations in Python.

## Overview

This project demonstrates basic file operations including:
- Creating files with content
- Reading file contents
- Listing files in a directory
- Deleting files
- Checking file existence
- Getting file information

## Usage

### Running the Demo

To see the file manager in action, simply run:

```bash
python3 mini_file.py
```

This will demonstrate all the core features of the file manager.

### Using as a Library

You can also import and use the `MiniFileManager` class in your own code:

```python
from mini_file import MiniFileManager

# Initialize the file manager
fm = MiniFileManager()

# Create a file
fm.create_file("example.txt", "Hello, World!")

# Read a file
content = fm.read_file("example.txt")
print(content)

# List all files
files = fm.list_files()
print(files)

# Delete a file
fm.delete_file("example.txt")
```

## Testing

Run the test suite to verify functionality:

```bash
python3 test_mini_file.py
```

## Features

- **Simple API**: Easy-to-use methods for common file operations
- **Error Handling**: Graceful error messages for common issues
- **Isolated Demo Directory**: Uses a `demo_files` directory by default to avoid cluttering your workspace
- **Cross-platform**: Works on Windows, macOS, and Linux

## Requirements

- Python 3.6 or higher (uses pathlib and modern Python features)

## License

This is a demonstration project for educational purposes.
