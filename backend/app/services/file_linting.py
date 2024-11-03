
# app/services/file_linting.py
from typing import Dict, List
import re

class FileLinter:
    def __init__(self):
        self.linters = {
            '.py': self._lint_python,
            '.js': self._lint_javascript,
            '.html': self._lint_html,
            '.css': self._lint_css
        }

    async def lint_file(self, file_path: str, content: str) -> List[Dict]:
        """Lint file based on its extension"""
        ext = file_path[file_path.rfind('.'):]
        linter = self.linters.get(ext)
        return await linter(content) if linter else []

    async def _lint_python(self, content: str) -> List[Dict]:
        """Python-specific linting rules"""
        issues = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 79:
                issues.append({
                    'line': i,
                    'message': 'Line too long (>79 characters)',
                    'severity': 'warning'
                })
            
            # Check indentation
            if line.startswith(' ') and not line.startswith('    '):
                issues.append({
                    'line': i,
                    'message': 'Inconsistent indentation',
                    'severity': 'error'
                })

        return issues

    async def _lint_javascript(self, content: str) -> List[Dict]:
        """JavaScript-specific linting rules"""
        issues = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            # Check semicolon usage
            if not line.strip().endswith(';') and not line.strip().endswith('{'):
                issues.append({
                    'line': i,
                    'message': 'Missing semicolon',
                    'severity': 'warning'
                })

        return issues

    async def _lint_html(self, content: str) -> List[Dict]:
        """HTML-specific linting rules"""
        issues = []
        unclosed_tags = []
        
        for match in re.finditer(r'<(/?)(\w+)[^>]*>', content):
            is_closing = bool(match.group(1))
            tag = match.group(2)
            
            if not is_closing:
                unclosed_tags.append(tag)
            elif unclosed_tags and unclosed_tags[-1] == tag:
                unclosed_tags.pop()
            else:
                issues.append({
                    'line': content[:match.start()].count('\n') + 1,
                    'message': f'Mismatched HTML tag: {tag}',
                    'severity': 'error'
                })

        return issues

    async def _lint_css(self, content: str) -> List[Dict]:
        """CSS-specific linting rules"""
        issues = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            # Check for vendor prefixes
            if re.search(r'-webkit-|-moz-|-ms-|-o-', line):
                issues.append({
                    'line': i,
                    'message': 'Consider using autoprefixer',
                    'severity': 'info'
                })

        return issues