"""Tests for topic functionality."""

import pytest
from services.study_material_service import StudyMaterialService


@pytest.fixture
def service():
    """Create a service instance."""
    return StudyMaterialService()


def test_explain_empty_topic(service):
    """Test explain with empty topic."""
    result = service.explain_topic("")
    assert not result.ok
    assert result.error.code == "INVALID_TOPIC"


def test_compare_empty_topics(service):
    """Test compare with empty topics."""
    result = service.compare_topics("", "")
    assert not result.ok
    assert result.error.code == "INVALID_TOPICS"


def test_list_topics(service):
    """Test listing topics."""
    result = service.list_topics()
    assert result.ok
    assert isinstance(result.data.get("topics"), list)
