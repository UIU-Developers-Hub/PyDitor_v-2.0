# app/services/collaborative_cursors.py
from typing import Dict, Set
import json
from datetime import datetime

class CollaborativeCursors:
    def __init__(self):
        self._cursors: Dict[str, Dict[str, Dict]] = {}  # file_path -> {user_id -> cursor_info}
        self._active_files: Dict[str, Set[str]] = {}    # file_path -> set of user_ids

    async def update_cursor(self, file_path: str, user_id: str, position: Dict) -> Dict:
        """Update cursor position for a user"""
        if file_path not in self._cursors:
            self._cursors[file_path] = {}
            self._active_files[file_path] = set()
        
        self._cursors[file_path][user_id] = {
            'position': position,
            'timestamp': datetime.utcnow().isoformat()
        }
        self._active_files[file_path].add(user_id)
        
        return self.get_file_cursors(file_path)

    def get_file_cursors(self, file_path: str) -> Dict:
        """Get all active cursors for a file"""
        return {
            'file_path': file_path,
            'cursors': self._cursors.get(file_path, {}),
            'active_users': list(self._active_files.get(file_path, set()))
        }
