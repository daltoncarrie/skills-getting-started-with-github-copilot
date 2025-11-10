"""
Test configuration and fixtures for the Mergington High School API tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_activity_data():
    """Sample activity data for testing."""
    return {
        "description": "Test activity for unit testing",
        "schedule": "Test schedule",
        "max_participants": 5,
        "participants": ["test1@mergington.edu", "test2@mergington.edu"]
    }


@pytest.fixture
def reset_activities():
    """Reset activities to original state after each test."""
    # Store original activities
    from src.app import activities
    original_activities = activities.copy()
    
    yield
    
    # Restore original activities
    activities.clear()
    activities.update(original_activities)