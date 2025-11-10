"""
Tests for the signup functionality of the Activities API.
"""

import pytest


def test_signup_for_activity_success(client, reset_activities):
    """Test successful signup for an activity."""
    # Get available activities first
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    original_count = len(activities[activity_name]["participants"])
    
    # Sign up for the activity
    test_email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
    
    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert test_email in response_data["message"]
    assert activity_name in response_data["message"]
    
    # Verify the participant was added
    response = client.get("/activities")
    updated_activities = response.json()
    updated_participants = updated_activities[activity_name]["participants"]
    
    assert len(updated_participants) == original_count + 1
    assert test_email in updated_participants


def test_signup_nonexistent_activity(client):
    """Test signup for a non-existent activity."""
    response = client.post("/activities/NonExistentActivity/signup", 
                          params={"email": "test@mergington.edu"})
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_registration(client, reset_activities):
    """Test that duplicate registration is prevented."""
    # Get an activity with existing participants
    response = client.get("/activities")
    activities = response.json()
    
    # Find an activity with participants
    activity_name = None
    existing_email = None
    for name, data in activities.items():
        if data["participants"]:
            activity_name = name
            existing_email = data["participants"][0]
            break
    
    if not activity_name:
        # If no activities have participants, add one first
        activity_name = list(activities.keys())[0]
        existing_email = "existing@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})
    
    # Try to sign up the same student again
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})
    
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_with_url_encoding(client, reset_activities):
    """Test signup with URL-encoded activity names."""
    # Get activities
    response = client.get("/activities")
    activities = response.json()
    
    # Find an activity with spaces in the name
    activity_name = None
    for name in activities.keys():
        if " " in name:
            activity_name = name
            break
    
    if activity_name:
        test_email = "urltest@mergington.edu"
        # The client should handle URL encoding automatically
        response = client.post(f"/activities/{activity_name}/signup", 
                              params={"email": test_email})
        
        assert response.status_code == 200
        
        # Verify the participant was added
        response = client.get("/activities")
        updated_activities = response.json()
        assert test_email in updated_activities[activity_name]["participants"]


def test_signup_email_validation(client):
    """Test signup with various email formats."""
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    
    # Valid email formats should work
    valid_emails = [
        "student@mergington.edu",
        "first.last@mergington.edu", 
        "student123@mergington.edu"
    ]
    
    for email in valid_emails:
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        # Should succeed (200) or fail due to duplicate (400), but not due to format
        assert response.status_code in [200, 400]