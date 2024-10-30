# File: backend/app/services/file_search.py
from pathlib import Path
from typing import List
import asyncio
import re

class FileSearchService:
    def __init__(self, base_directory: str):
        self.base_directory = Path(base_directory)
    
    async def search_files(self, query: str, user_id: int) -> List[dict]:
        results = []
        async for file in self._scan_directory(self.base_directory, query, user_id):
            results.append({
                "path": str(file.relative_to(self.base_directory)),
                "name": file.name,
                "type": "file" if file.is_file() else "directory"
            })
        return results
    
    async def _scan_directory(self, directory: Path, query: str, user_id: int):
        pattern = re.compile(query, re.IGNORECASE)
        for item in directory.iterdir():
            if pattern.search(item.name):
                yield item
            if item.is_dir():
                async for subitem in self._scan_directory(item, query, user_id):
                    yield subitem
