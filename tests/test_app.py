"""
Tests for the High School Management System API

Uses the AAA (Arrange-Act-Assert) testing pattern:
- Arrange: Set up test data and preconditions
- Act: Execute the code being tested
- Assert: Verify the results
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture to reset activities to initial state before each test.
    Ensures test isolation by preventing state leakage between tests.
    """
    # Arrange: Define the initial activities state
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team and intramural games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and compete in matches",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 10,
            "participants": ["sarah@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["jackson@mergington.edu", "ava@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater production and performance arts",
            "schedule": "Thursdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["lily@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Build and program robots for competition",
            "schedule": "Tuesdays, 4:30 PM - 6:00 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu", "lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["grace@mergington.edu"]
        }
    }
    
    # Reset the activities dictionary
    activities.clear()
    activities.update(initial_activities)
    
    yield  # Run the test
    
    # Cleanup (reset again after test)
    activities.clear()
    activities.update(initial_activities)


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


class TestGetActivities:
    """Tests for the GET /activities endpoint"""
    
    def test_get_all_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all available activities
        
        AAA Pattern:
        - Arrange: Client is ready (from fixture)
        - Act: Make GET request to /activities
        - Assert: Verify status code is 200 and all 9 activities are returned
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert "Basketball Team" in data
        assert "Tennis Club" in data
        assert "Art Studio" in data
        assert "Drama Club" in data
        assert "Robotics Club" in data
        assert "Debate Team" in data
    
    def test_get_activities_includes_activity_details(self, client):
        """
        Test that each activity has required fields
        
        AAA Pattern:
        - Arrange: Client is ready
        - Act: Make GET request to /activities
        - Assert: Verify each activity has description, schedule, max_participants, and participants
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
    
    def test_get_activities_returns_current_participants(self, client):
        """
        Test that activities show correct current participant lists
        
        AAA Pattern:
        - Arrange: Client is ready
        - Act: Make GET request to /activities
        - Assert: Verify specific activities have expected participants
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
        assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_student_succeeds(self, client):
        """
        Test successful signup of a new student to an activity
        
        AAA Pattern:
        - Arrange: Prepare new student email and activity name
        - Act: Make POST request to signup endpoint
        - Assert: Verify status code is 200 and success message is returned
        """
        # Arrange
        activity_name = "Chess Club"
        new_student = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert new_student in response.json()["message"]
        assert activity_name in response.json()["message"]
    
    def test_signup_student_appears_in_participants_list(self, client):
        """
        Test that a signed-up student appears in the activity's participants list
        
        AAA Pattern:
        - Arrange: Prepare student email
        - Act: Signup student, then fetch activities
        - Assert: Verify student is now in participants list
        """
        # Arrange
        activity_name = "Programming Class"
        new_student = "newcoder@mergington.edu"
        
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )
        activities_response = client.get("/activities")
        
        # Assert
        assert signup_response.status_code == 200
        assert activities_response.status_code == 200
        participants = activities_response.json()[activity_name]["participants"]
        assert new_student in participants
        assert len(participants) == 3  # 2 original + 1 new
    
    def test_signup_to_nonexistent_activity_returns_404(self, client):
        """
        Test that signup to a non-existent activity returns 404
        
        AAA Pattern:
        - Arrange: Prepare student email and non-existent activity name
        - Act: Make POST request to signup endpoint with invalid activity
        - Assert: Verify status code is 404 and error detail is provided
        """
        # Arrange
        fake_activity = "Nonexistent Club"
        student_email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_already_signed_up_student_returns_400(self, client):
        """
        Test that a student already signed up gets a 400 error
        
        AAA Pattern:
        - Arrange: Get an existing participant from an activity
        - Act: Attempt to signup the same student again
        - Assert: Verify status code is 400 and appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        existing_student = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_student}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"
    
    def test_signup_multiple_students_to_same_activity(self, client):
        """
        Test that multiple different students can signup to the same activity
        
        AAA Pattern:
        - Arrange: Prepare multiple student emails
        - Act: Signup each student to the same activity
        - Assert: Verify all students are successfully added
        """
        # Arrange
        activity_name = "Tennis Club"
        students = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
        
        # Act
        responses = [
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": student}
            )
            for student in students
        ]
        
        # Assert
        for response in responses:
            assert response.status_code == 200
        
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert "sarah@mergington.edu" in participants  # Original
        assert all(student in participants for student in students)
        assert len(participants) == 4  # 1 original + 3 new


class TestUnregisterFromActivity:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_existing_participant_succeeds(self, client):
        """
        Test successful unregistration of an existing participant
        
        AAA Pattern:
        - Arrange: Get an existing participant from an activity
        - Act: Make DELETE request to unregister endpoint
        - Assert: Verify status code is 200 and success message
        """
        # Arrange
        activity_name = "Chess Club"
        participant = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": participant}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert participant in response.json()["message"]
        assert activity_name in response.json()["message"]
    
    def test_unregister_removes_participant_from_list(self, client):
        """
        Test that unregistration removes the student from the participants list
        
        AAA Pattern:
        - Arrange: Get an activity with existing participant
        - Act: Unregister the participant, then fetch activities
        - Assert: Verify participant is no longer in the list
        """
        # Arrange
        activity_name = "Programming Class"
        participant = "emma@mergington.edu"
        
        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": participant}
        )
        activities_response = client.get("/activities")
        
        # Assert
        assert unregister_response.status_code == 200
        participants = activities_response.json()[activity_name]["participants"]
        assert participant not in participants
        assert len(participants) == 1  # Only sophia remains
    
    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """
        Test that unregistering from a non-existent activity returns 404
        
        AAA Pattern:
        - Arrange: Prepare student email and non-existent activity name
        - Act: Make DELETE request for invalid activity
        - Assert: Verify status code is 404
        """
        # Arrange
        fake_activity = "Ghost Club"
        student_email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{fake_activity}/unregister",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_non_participant_returns_400(self, client):
        """
        Test that unregistering a non-participant returns 400
        
        AAA Pattern:
        - Arrange: Get a student not in an activity
        - Act: Attempt to unregister non-participant
        - Assert: Verify status code is 400 with appropriate error
        """
        # Arrange
        activity_name = "Chess Club"
        non_participant = "random@mergington.edu"  # Not in Chess Club
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": non_participant}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student not signed up for this activity"
    
    def test_unregister_multiple_participants_one_by_one(self, client):
        """
        Test unregistering multiple students from same activity sequentially
        
        AAA Pattern:
        - Arrange: Get an activity with multiple participants
        - Act: Unregister each participant one by one
        - Assert: Verify all are removed and count decreases
        """
        # Arrange
        activity_name = "Chess Club"
        participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # Act & Assert
        for i, participant in enumerate(participants):
            response = client.delete(
                f"/activities/{activity_name}/unregister",
                params={"email": participant}
            )
            assert response.status_code == 200
            
            # Verify participant count decreases
            activities_response = client.get("/activities")
            remaining = activities_response.json()[activity_name]["participants"]
            assert len(remaining) == len(participants) - i - 1
            assert participant not in remaining


class TestIntegrationScenarios:
    """Integration tests combining multiple endpoints"""
    
    def test_signup_then_unregister_workflow(self, client):
        """
        Test complete workflow: signup a student, verify they're added, then unregister
        
        AAA Pattern:
        - Arrange: Prepare test data
        - Act: Signup, verify in list, then unregister
        - Assert: Verify student appears and then disappears
        """
        # Arrange
        activity_name = "Art Studio"
        student = "newcomer@mergington.edu"
        
        # Act: Signup
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student}
        )
        assert signup_response.status_code == 200
        
        # Act: Verify in list
        activities_response = client.get("/activities")
        participants_after_signup = activities_response.json()[activity_name]["participants"]
        assert student in participants_after_signup
        original_count = len(participants_after_signup)
        
        # Act: Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student}
        )
        assert unregister_response.status_code == 200
        
        # Assert: Verify removed from list
        activities_response = client.get("/activities")
        participants_after_unregister = activities_response.json()[activity_name]["participants"]
        assert student not in participants_after_unregister
        assert len(participants_after_unregister) == original_count - 1
    
    def test_signup_multiple_activities_same_student(self, client):
        """
        Test that a student can signup for multiple activities
        
        AAA Pattern:
        - Arrange: Select multiple activities and student
        - Act: Signup student to each activity
        - Assert: Verify student appears in all activities
        """
        # Arrange
        student = "versatile@mergington.edu"
        activities_to_join = ["Chess Club", "Programming Class", "Robotics Club"]
        
        # Act: Signup to multiple activities
        for activity in activities_to_join:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": student}
            )
            assert response.status_code == 200
        
        # Assert: Verify in all activities
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        
        for activity in activities_to_join:
            assert student in data[activity]["participants"]
