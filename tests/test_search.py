"""Tests for search functionality."""

import os
import pytest
from services.study_material_service import StudyMaterialService


@pytest.fixture
def service():
    """Create a service instance."""
    return StudyMaterialService()


def test_search_empty_query(service):
    """Test search with empty query."""
    result = service.search_material("")
    assert not result.ok
    assert result.error.code == "INVALID_QUERY"


def test_search_no_materials(service):
    """Test search when no materials exist."""
    result = service.search_material("test")
    assert not result.ok or result.data.get("results_count") == 0
