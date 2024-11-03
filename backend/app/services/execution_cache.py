# app/services/execution_cache.py
from typing import Dict, Optional
import hashlib
import json
from datetime import datetime, timedelta

class ExecutionCache:
    def __init__(self, cache_duration: int = 3600):  # Default 1 hour cache
        self._cache: Dict[str, Dict] = {}
        self._cache_duration = timedelta(seconds=cache_duration)

    def _generate_cache_key(self, code: str, language: str) -> str:
        """Generate unique cache key for code execution"""
        content = f"{code}:{language}".encode('utf-8')
        return hashlib.sha256(content).hexdigest()

    async def get_cached_result(self, code: str, language: str) -> Optional[Dict]:
        """Get cached execution result if available and valid"""
        cache_key = self._generate_cache_key(code, language)
        cached_data = self._cache.get(cache_key)
        
        if cached_data:
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.utcnow() - cached_time < self._cache_duration:
                return cached_data['result']
            
        return None

    async def cache_result(self, code: str, language: str, result: Dict):
        """Cache execution result"""
        cache_key = self._generate_cache_key(code, language)
        self._cache[cache_key] = {
            'timestamp': datetime.utcnow().isoformat(),
            'result': result
        }
