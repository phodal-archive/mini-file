# mini-file

A collection of Python demonstration projects including a simple file manager and a comprehensive FastAPI blog example.

## Projects

### 1. Mini File Manager

A simple demonstration of file management operations in Python.

#### Features
- Creating files with content
- Reading file contents
- Listing files in a directory
- Deleting files
- Checking file existence
- Getting file information

### 2. Blog API (FastAPI Example)

A comprehensive blog API built with FastAPI demonstrating complex multi-file architecture, perfect for code review demonstrations.

#### Features
- RESTful API with full CRUD operations
- Multi-layered architecture (API → Service → Database)
- User management, blog posts, comments, and tags
- Search and filtering capabilities
- Statistics and analytics
- Thread-safe in-memory database
- Comprehensive Mermaid diagrams showing architecture

See [blog_api/README.md](blog_api/README.md) for detailed documentation including architecture diagrams.

## Usage

### Mini File Manager

#### Running the Demo

To see the file manager in action, simply run:

```bash
python3 mini_file.py
```

This will demonstrate all the core features of the file manager.

#### Using as a Library

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

### Blog API

#### Installation

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

#### Running the API Server

```bash
# Run with uvicorn
python -m uvicorn blog_api.main:app --reload

# Or run directly
python -m blog_api.main
```

The API will be available at:
- API Base: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

See [blog_api/README.md](blog_api/README.md) for complete API documentation and examples.

## Testing

### Mini File Manager Tests

Run the test suite to verify file manager functionality:

```bash
python3 test_mini_file.py
```

### Blog API Tests

Run the blog API test suite:

```bash
python3 test_blog_api.py
```

## Features

- **Simple API**: Easy-to-use methods for common file operations
- **Error Handling**: Graceful error messages for common issues
- **Isolated Demo Directory**: Uses a `demo_files` directory by default to avoid cluttering your workspace
- **Cross-platform**: Works on Windows, macOS, and Linux

## Requirements

### Mini File Manager
- Python 3.6 or higher (uses pathlib and modern Python features)

### Blog API
- Python 3.7 or higher
- FastAPI 0.109.1+
- Uvicorn
- Pydantic 2.5.0+

Install all requirements with:
```bash
pip install -r requirements.txt
```

## License

This is a demonstration project for educational purposes.
