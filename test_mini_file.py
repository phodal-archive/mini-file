#!/usr/bin/env python3
"""
Tests for Mini File Manager

Simple tests to validate the file manager functionality.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path to import mini_file
sys.path.insert(0, str(Path(__file__).parent))

from mini_file import MiniFileManager


def test_create_and_read_file():
    """Test creating and reading a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        fm = MiniFileManager(tmpdir)
        
        # Create a file
        result = fm.create_file("test.txt", "Test content")
        assert "✓" in result, f"Failed to create file: {result}"
        
        # Read the file
        result = fm.read_file("test.txt")
        assert "Test content" in result, f"Failed to read correct content: {result}"
        
        print("✓ test_create_and_read_file passed")


def test_list_files():
    """Test listing files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        fm = MiniFileManager(tmpdir)
        
        # Create multiple files
        fm.create_file("file1.txt", "Content 1")
        fm.create_file("file2.txt", "Content 2")
        
        # List files
        result = fm.list_files()
        assert "file1.txt" in result, "file1.txt not found in list"
        assert "file2.txt" in result, "file2.txt not found in list"
        
        print("✓ test_list_files passed")


def test_delete_file():
    """Test deleting a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        fm = MiniFileManager(tmpdir)
        
        # Create a file
        fm.create_file("delete_me.txt", "Delete this")
        
        # Verify it exists
        assert fm.file_exists("delete_me.txt"), "File should exist"
        
        # Delete the file
        result = fm.delete_file("delete_me.txt")
        assert "✓" in result, f"Failed to delete file: {result}"
        
        # Verify it's gone
        assert not fm.file_exists("delete_me.txt"), "File should not exist after deletion"
        
        print("✓ test_delete_file passed")


def test_file_existence():
    """Test checking file existence."""
    with tempfile.TemporaryDirectory() as tmpdir:
        fm = MiniFileManager(tmpdir)
        
        # Check non-existent file
        assert not fm.file_exists("nonexistent.txt"), "Nonexistent file should return False"
        
        # Create and check existent file
        fm.create_file("exists.txt", "I exist")
        assert fm.file_exists("exists.txt"), "Existent file should return True"
        
        print("✓ test_file_existence passed")


def test_file_info():
    """Test getting file information."""
    with tempfile.TemporaryDirectory() as tmpdir:
        fm = MiniFileManager(tmpdir)
        
        # Create a file
        content = "Test content for info"
        fm.create_file("info.txt", content)
        
        # Get file info
        result = fm.get_file_info("info.txt")
        assert "info.txt" in result, "Filename not in info"
        assert "bytes" in result, "Size info not present"
        
        print("✓ test_file_info passed")


def test_read_nonexistent_file():
    """Test reading a file that doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        fm = MiniFileManager(tmpdir)
        
        result = fm.read_file("nonexistent.txt")
        assert "✗" in result or "not found" in result.lower(), "Should report file not found"
        
        print("✓ test_read_nonexistent_file passed")


def test_delete_nonexistent_file():
    """Test deleting a file that doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        fm = MiniFileManager(tmpdir)
        
        result = fm.delete_file("nonexistent.txt")
        assert "✗" in result or "not found" in result.lower(), "Should report file not found"
        
        print("✓ test_delete_nonexistent_file passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Running Mini File Manager Tests")
    print("=" * 50)
    print()
    
    tests = [
        test_create_and_read_file,
        test_list_files,
        test_delete_file,
        test_file_existence,
        test_file_info,
        test_read_nonexistent_file,
        test_delete_nonexistent_file,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 50)
    total = len(tests)
    passed = total - failed
    print(f"Tests: {passed}/{total} passed")
    if failed == 0:
        print("All tests passed! ✓")
    else:
        print(f"{failed} test(s) failed ✗")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
