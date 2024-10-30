# File: backend/app/services/file_validation.py
from typing import Optional, Tuple
import magic  # For MIME type validation
import re

class FileValidator:
    ALLOWED_EXTENSIONS = {'.py', '.cpp', '.java', '.js', '.html', '.css'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def validate_content(content: str, file_extension: str) -> Tuple[bool, Optional[str]]:
        """
        Validates file content based on size and file extension.

        Parameters:
            content (str): The content of the file as a string.
            file_extension (str): The file extension (e.g., ".py", ".js").

        Returns:
            Tuple[bool, Optional[str]]: A tuple where the first element indicates
                                        validation success, and the second element
                                        is an error message if validation fails.
        """
        # Validate file size
        content_size = len(content.encode('utf-8'))
        if content_size > FileValidator.MAX_FILE_SIZE:
            return False, "File size exceeds maximum limit"
        
        # Validate file extension
        if file_extension.lower() not in FileValidator.ALLOWED_EXTENSIONS:
            return False, f"Unsupported file extension: {file_extension}"
        
        return True, None
