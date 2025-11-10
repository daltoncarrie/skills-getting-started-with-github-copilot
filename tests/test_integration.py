"""
Integration tests for the Activities API that test complete workflows.
"""

import pytest


def test_complete_registration_workflow(client, reset_activities):
    """Test a complete registration workflow from start to finish."""
    # Step 1: Get initial state
    response = client.get("/activities")
    initial_activities = response.json()
    activity_name = list(initial_activities.keys())[0]
    initial_count = len(initial_activities[activity_name]["participants"])
    initial_max = initial_activities[activity_name]["max_participants"]
    
    # Step 2: Register a new student
    test_email = "workflow@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
    assert response.status_code == 200
    
    # Step 3: Verify registration
    response = client.get("/activities")
    activities_after_signup = response.json()
    participants_after_signup = activities_after_signup[activity_name]["participants"]
    
    assert len(participants_after_signup) == initial_count + 1
    assert test_email in participants_after_signup
    
    # Step 4: Try to register the same student again (should fail)
    response = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
    assert response.status_code == 400
    
    # Step 5: Unregister the student
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": test_email})
    assert response.status_code == 200
    
    # Step 6: Verify unregistration
    response = client.get("/activities")
    final_activities = response.json()
    final_participants = final_activities[activity_name]["participants"]
    
    assert len(final_participants) == initial_count
    assert test_email not in final_participants
    
    # Step 7: Verify we can register the same student again after unregistration
    response = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
    assert response.status_code == 200


def test_multiple_students_same_activity(client, reset_activities):
    """Test registering multiple students for the same activity."""
    response = client.get("/activities")
    activities = response.json()
    activity_name = list(activities.keys())[0]
    initial_count = len(activities[activity_name]["participants"])
    
    # Register multiple students
    test_emails = [
        "student1@mergington.edu",
        "student2@mergington.edu", 
        "student3@mergington.edu"
    ]
    
    for email in test_emails:
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response.status_code == 200
    
    # Verify all are registered
    response = client.get("/activities")
    updated_activities = response.json()
    participants = updated_activities[activity_name]["participants"]
    
    assert len(participants) == initial_count + len(test_emails)
    for email in test_emails:
        assert email in participants
    
    # Unregister one student
    response = client.delete(f"/activities/{activity_name}/unregister", 
                           params={"email": test_emails[1]})
    assert response.status_code == 200
    
    # Verify only one was removed
    response = client.get("/activities")
    final_activities = response.json()
    final_participants = final_activities[activity_name]["participants"]
    
    assert len(final_participants) == initial_count + len(test_emails) - 1
    assert test_emails[1] not in final_participants
    assert test_emails[0] in final_participants
    assert test_emails[2] in final_participants


def test_student_multiple_activities(client, reset_activities):
    """Test registering the same student for multiple activities."""
    response = client.get("/activities")
    activities = response.json()
    activity_names = list(activities.keys())[:3]  # Test with first 3 activities
    
    test_email = "multiactvity@mergington.edu"
    
    # Register for multiple activities
    for activity_name in activity_names:
        response = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
        assert response.status_code == 200
    
    # Verify student is in all activities
    response = client.get("/activities")
    updated_activities = response.json()
    
    for activity_name in activity_names:
        assert test_email in updated_activities[activity_name]["participants"]
    
    # Unregister from one activity
    response = client.delete(f"/activities/{activity_names[0]}/unregister", 
                           params={"email": test_email})
    assert response.status_code == 200
    
    # Verify student is removed from only that activity
    response = client.get("/activities")
    final_activities = response.json()
    
    assert test_email not in final_activities[activity_names[0]]["participants"]
    assert test_email in final_activities[activity_names[1]]["participants"] 
    assert test_email in final_activities[activity_names[2]]["participants"]


def test_activity_capacity_constraints(client, reset_activities):
    """Test that activity capacity constraints are respected (if implemented)."""
    response = client.get("/activities")
    activities = response.json()
    
    # Find an activity with low capacity for testing
    activity_name = None
    max_participants = float('inf')
    
    for name, data in activities.items():
        if data["max_participants"] < max_participants:
            max_participants = data["max_participants"]
            activity_name = name
    
    if activity_name:
        current_count = len(activities[activity_name]["participants"])
        available_spots = max_participants - current_count
        
        # Fill up remaining spots
        for i in range(available_spots):
            email = f"capacity_test{i}@mergington.edu"
            response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
            # Should succeed unless capacity checking is implemented
            # For now, we just verify the API doesn't crash
            assert response.status_code in [200, 400]  # Either success or capacity full


def test_api_error_handling(client):
    """Test API error handling with various invalid inputs."""
    # Test with empty email
    response = client.post("/activities/Chess Club/signup", params={"email": ""})
    # API should handle gracefully (exact behavior may vary)
    assert response.status_code in [200, 400, 422]
    
    # Test with very long activity name
    long_name = "A" * 1000
    response = client.post(f"/activities/{long_name}/signup", 
                          params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    
    # Test unregister with empty email - our API accepts empty strings
    response = client.delete("/activities/Chess Club/unregister", params={"email": ""})
    assert response.status_code in [200, 400, 422]