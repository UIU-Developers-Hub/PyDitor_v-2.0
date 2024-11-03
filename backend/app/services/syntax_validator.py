# app/services/syntax_validator.py
import ast
from typing import Dict, List, Tuple, Optional

class SyntaxValidator:
    @staticmethod
    def validate_python(code: str) -> Tuple[bool, Optional[str], List[Dict]]:
        """Validate Python syntax and return detailed error information"""
        try:
            ast.parse(code)
            return True, None, []
        except SyntaxError as e:
            error_info = {
                'line': e.lineno,
                'column': e.offset,
                'message': str(e),
                'text': e.text.strip() if e.text else ''
            }
            return False, f"Syntax error at line {e.lineno}", [error_info]
        except Exception as e:
            return False, str(e), []