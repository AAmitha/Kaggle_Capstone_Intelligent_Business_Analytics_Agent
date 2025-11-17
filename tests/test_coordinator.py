"""Tests for the Coordinator Agent."""

import pytest
import os
from src.coordinator import CoordinatorAgent


@pytest.fixture
def api_key():
    """Get API key from environment."""
    return os.getenv("GEMINI_API_KEY")


@pytest.fixture
def coordinator(api_key):
    """Create a coordinator instance."""
    if not api_key:
        pytest.skip("GEMINI_API_KEY not set")
    return CoordinatorAgent(user_id="test_user", api_key=api_key)


def test_coordinator_initialization(coordinator):
    """Test coordinator initialization."""
    assert coordinator is not None
    assert coordinator.session is not None
    assert coordinator.data_analyst is not None
    assert coordinator.report_generator is not None


def test_session_management(coordinator):
    """Test session management."""
    context = coordinator.get_session_context()
    assert "session_id" in context
    assert "user_id" in context


def test_memory_insights(coordinator):
    """Test memory bank retrieval."""
    insights = coordinator.get_memory_insights()
    assert isinstance(insights, list)

