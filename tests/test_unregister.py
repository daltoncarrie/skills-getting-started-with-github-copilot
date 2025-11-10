"""
Tests for the unregister functionality of the Activities API.
"""

import pytest


def test_unregister_from_activity_success(client, reset_activities):
    """Test successful unregistration from an activity."""
    # First, sign up a student
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    test_email = "unregister_test@mergington.edu"
    
    # Sign up first
    client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
    
    # Verify signup worked
    response = client.get("/activities") 
    activities = response.json()
    assert test_email in activities[activity_name]["participants"]
    original_count = len(activities[activity_name]["participants"])
    
    # Now unregister
    response = client.delete(f"/activities/{activity_name}/unregister", 
                           params={"email": test_email})
    
    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert "Unregistered" in response_data["message"]
    assert test_email in response_data["message"]
    assert activity_name in response_data["message"]
    
    # Verify the participant was removed
    response = client.get("/activities")
    updated_activities = response.json()
    updated_participants = updated_activities[activity_name]["participants"]
    
    assert len(updated_participants) == original_count - 1
    assert test_email not in updated_participants


def test_unregister_nonexistent_activity(client):
    """Test unregister from a non-existent activity."""
    response = client.delete("/activities/NonExistentActivity/unregister",
                           params={"email": "test@mergington.edu"})
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_registered_student(client):
    """Test unregister a student who is not registered."""
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    
    # Try to unregister a student who was never registered
    response = client.delete(f"/activities/{activity_name}/unregister",
                           params={"email": "notregistered@mergington.edu"})
    
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()


def test_unregister_existing_participant(client, reset_activities):
    """Test unregistering an existing participant."""
    # Get activities and find one with existing participants
    response = client.get("/activities")
    activities = response.json()
    
    activity_name = None
    existing_email = None
    for name, data in activities.items():
        if data["participants"]:
            activity_name = name
            existing_email = data["participants"][0]
            break
    
    if activity_name and existing_email:
        original_count = len(activities[activity_name]["participants"])
        
        # Unregister the existing participant
        response = client.delete(f"/activities/{activity_name}/unregister",
                               params={"email": existing_email})
        
        assert response.status_code == 200
        
        # Verify removal
        response = client.get("/activities")
        updated_activities = response.json()
        updated_participants = updated_activities[activity_name]["participants"]
        
        assert len(updated_participants) == original_count - 1
        assert existing_email not in updated_participants


def test_unregister_with_url_encoding(client, reset_activities):
    """Test unregister with URL-encoded activity names."""
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
        test_email = "urlunregister@mergington.edu"
        
        # First sign up
        client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
        
        # Then unregister with URL encoding handled by client
        response = client.delete(f"/activities/{activity_name}/unregister",
                               params={"email": test_email})
        
        assert response.status_code == 200
        
        # Verify removal
        response = client.get("/activities")
        updated_activities = response.json()
        assert test_email not in updated_activities[activity_name]["participants"]


def test_signup_unregister_cycle(client, reset_activities):
    """Test multiple signup/unregister cycles for the same student."""
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    test_email = "cycle_test@mergington.edu"
    original_count = len(activities[activity_name]["participants"])
    
    # Cycle 1: Sign up -> Unregister
    client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
    client.delete(f"/activities/{activity_name}/unregister", params={"email": test_email})
    
    # Cycle 2: Sign up -> Unregister  
    client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
    client.delete(f"/activities/{activity_name}/unregister", params={"email": test_email})
    
    # Verify final state
    response = client.get("/activities")
    final_activities = response.json()
    final_count = len(final_activities[activity_name]["participants"])
    
    assert final_count == original_count
    assert test_email not in final_activities[activity_name]["participants"]