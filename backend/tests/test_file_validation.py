# File: backend/tests/test_file_validation.py
import pytest
from app.services.file_validation import FileValidator

def test_file_size_validation():
    """Tests that FileValidator correctly limits file size."""
    large_content = "x" * (FileValidator.MAX_FILE_SIZE + 1)
    small_content = "print('hello')"
    
    # Test: Oversized file should fail validation
    is_valid, error = FileValidator.validate_content(large_content, ".py")
    assert not is_valid, "Expected failure for oversized file"
    assert "size exceeds" in error, "Expected size limit error message"
    
    # Test: Valid file size should pass
    is_valid, error = FileValidator.validate_content(small_content, ".py")
    assert is_valid, "Expected successful validation for valid file size"
    assert error is None

def test_file_extension_validation():
    """Tests that FileValidator allows only specific file extensions."""
    content = "print('hello')"
    
    # Test: Valid extension should pass
    is_valid, error = FileValidator.validate_content(content, ".py")
    assert is_valid, "Expected successful validation for .py extension"
    assert error is None
    
    # Test: Invalid extension should fail
    is_valid, error = FileValidator.validate_content(content, ".invalid")
    assert not is_valid, "Expected failure for unsupported extension"
    assert "Unsupported file extension" in error
