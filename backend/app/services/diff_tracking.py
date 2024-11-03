# app/services/diff_tracking.py
from difflib import SequenceMatcher
from datetime import datetime
from typing import Dict, List, Optional
import json

class DiffTracker:
    def __init__(self):
        self._file_versions: Dict[str, List[Dict]] = {}

    async def track_changes(self, file_path: str, new_content: str, user_id: str) -> Dict:
        """Track file changes and store diff information"""
        current_version = self._get_latest_version(file_path)
        
        if current_version is None:
            diff_info = self._create_initial_version(file_path, new_content, user_id)
        else:
            diff = self._calculate_diff(current_version['content'], new_content)
            diff_info = {
                'timestamp': datetime.utcnow().isoformat(),
                'user_id': user_id,
                'content': new_content,
                'changes': diff
            }
            self._file_versions[file_path].append(diff_info)
        
        return diff_info

    def _get_latest_version(self, file_path: str) -> Optional[Dict]:
        """Get the latest version of a file"""
        versions = self._file_versions.get(file_path, [])
        return versions[-1] if versions else None

    def _calculate_diff(self, old_content: str, new_content: str) -> List[Dict]:
        """Calculate detailed diff between two versions"""
        matcher = SequenceMatcher(None, old_content.splitlines(), new_content.splitlines())
        changes = []
        
        for op, i1, i2, j1, j2 in matcher.get_opcodes():
            if op != 'equal':
                changes.append({
                    'operation': op,
                    'old_start': i1,
                    'old_end': i2,
                    'new_start': j1,
                    'new_end': j2
                })
        
        return changes

    def _create_initial_version(self, file_path: str, content: str, user_id: str) -> Dict:
        """Create initial version entry for a file"""
        version_info = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'content': content,
            'changes': []
        }
        self._file_versions[file_path] = [version_info]
        return version_info