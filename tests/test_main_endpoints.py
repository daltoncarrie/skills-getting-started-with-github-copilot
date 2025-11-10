"""
Tests for the main API endpoints of the Mergington High School Activities API.
"""

import pytest
from fastapi.testclient import TestClient


def test_root_redirect(client):
    """Test that root path redirects to static index.html."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test retrieving all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Check structure of first activity
    first_activity = list(activities.values())[0]
    required_fields = ["description", "schedule", "max_participants", "participants"]
    for field in required_fields:
        assert field in first_activity
        
    # Verify participants is a list
    assert isinstance(first_activity["participants"], list)


def test_get_activities_structure(client):
    """Test that activities have the correct structure."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert len(activity_name) > 0
        
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
        
        # Check that max_participants is positive
        assert activity_data["max_participants"] > 0
        
        # Check that participants count doesn't exceed max
        assert len(activity_data["participants"]) <= activity_data["max_participants"]