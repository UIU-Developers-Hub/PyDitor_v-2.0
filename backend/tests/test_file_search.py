# File: backend/tests/test_file_search.py
import pytest
from app.services.file_search import FileSearchService
from pathlib import Path

@pytest.fixture
def temp_directory(tmp_path: Path) -> Path:
    """Creates a temporary directory for test files."""
    # Setup test files
    (tmp_path / "test1.py").write_text("test content")
    (tmp_path / "test2.py").write_text("test content")
    (tmp_path / "other.txt").write_text("test content")
    return tmp_path

@pytest.mark.asyncio
async def test_file_search(temp_directory: Path):
    """Tests file search functionality with exact and partial matches."""
    search_service = FileSearchService(str(temp_directory))
    
    # Test: Exact match for "test1"
    results = await search_service.search_files("test1", user_id=1)
    assert len(results) == 1, "Expected one exact match"
    assert results[0]["name"] == "test1.py"
    
    # Test: Partial match for "test"
    results = await search_service.search_files("test", user_id=1)
    assert len(results) == 2, "Expected two partial matches"
    assert all(r["name"].startswith("test") for r in results), "Expected results to start with 'test'"
