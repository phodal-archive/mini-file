#!/usr/bin/env python3
"""
Mini File Manager Demo

A simple demonstration of file management operations including:
- Creating files
- Reading files
- Listing files
- Deleting files
"""

import os
import sys
from pathlib import Path


class MiniFileManager:
    """A simple file manager for demonstrating basic file operations."""
    
    def __init__(self, base_dir=None):
        """Initialize the file manager with a base directory."""
        if base_dir is None:
            base_dir = Path.cwd() / "demo_files"
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def create_file(self, filename, content=""):
        """Create a new file with optional content."""
        filepath = self.base_dir / filename
        try:
            filepath.write_text(content)
            return f"✓ Created file: {filename}"
        except Exception as e:
            return f"✗ Error creating file: {e}"
    
    def read_file(self, filename):
        """Read and return the content of a file."""
        filepath = self.base_dir / filename
        try:
            content = filepath.read_text()
            return f"Content of {filename}:\n{content}"
        except FileNotFoundError:
            return f"✗ File not found: {filename}"
        except Exception as e:
            return f"✗ Error reading file: {e}"
    
    def list_files(self):
        """List all files in the base directory."""
        try:
            files = [f.name for f in self.base_dir.iterdir() if f.is_file()]
            if files:
                return "Files:\n" + "\n".join(f"  - {f}" for f in sorted(files))
            else:
                return "No files found."
        except Exception as e:
            return f"✗ Error listing files: {e}"
    
    def delete_file(self, filename):
        """Delete a file."""
        filepath = self.base_dir / filename
        try:
            if filepath.exists():
                filepath.unlink()
                return f"✓ Deleted file: {filename}"
            else:
                return f"✗ File not found: {filename}"
        except Exception as e:
            return f"✗ Error deleting file: {e}"
    
    def file_exists(self, filename):
        """Check if a file exists."""
        filepath = self.base_dir / filename
        return filepath.exists()
    
    def get_file_info(self, filename):
        """Get information about a file."""
        filepath = self.base_dir / filename
        try:
            if filepath.exists():
                stat = filepath.stat()
                return (f"File: {filename}\n"
                       f"  Size: {stat.st_size} bytes\n"
                       f"  Modified: {stat.st_mtime}")
            else:
                return f"✗ File not found: {filename}"
        except Exception as e:
            return f"✗ Error getting file info: {e}"


def demo():
    """Run a demonstration of the file manager."""
    print("=" * 50)
    print("Mini File Manager Demo")
    print("=" * 50)
    print()
    
    # Initialize the file manager
    fm = MiniFileManager()
    print(f"Working directory: {fm.base_dir}")
    print()
    
    # Demo 1: Create files
    print("1. Creating files...")
    print(fm.create_file("hello.txt", "Hello, World!"))
    print(fm.create_file("demo.txt", "This is a demo file.\nIt has multiple lines."))
    print(fm.create_file("empty.txt"))
    print()
    
    # Demo 2: List files
    print("2. Listing files...")
    print(fm.list_files())
    print()
    
    # Demo 3: Read files
    print("3. Reading files...")
    print(fm.read_file("hello.txt"))
    print()
    print(fm.read_file("demo.txt"))
    print()
    
    # Demo 4: Get file info
    print("4. Getting file information...")
    print(fm.get_file_info("hello.txt"))
    print()
    
    # Demo 5: Check file existence
    print("5. Checking file existence...")
    print(f"  hello.txt exists: {fm.file_exists('hello.txt')}")
    print(f"  nonexistent.txt exists: {fm.file_exists('nonexistent.txt')}")
    print()
    
    # Demo 6: Delete a file
    print("6. Deleting a file...")
    print(fm.delete_file("empty.txt"))
    print()
    
    # Demo 7: List files again
    print("7. Listing files after deletion...")
    print(fm.list_files())
    print()
    
    print("=" * 50)
    print("Demo completed!")
    print("=" * 50)


if __name__ == "__main__":
    demo()
