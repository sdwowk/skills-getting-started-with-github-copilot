from src.app import activities

EXISTING_ACTIVITY = "Chess Club"
EXISTING_PARTICIPANT = "michael@mergington.edu"


def test_root_redirects_to_static_index(client):
    # Arrange
    # (no setup required)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange
    # (no setup required)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert EXISTING_ACTIVITY in body
    activity = body[EXISTING_ACTIVITY]
    assert set(["description", "schedule", "max_participants", "participants"]) <= activity.keys()


def test_signup_for_activity_success(client):
    # Arrange
    new_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{EXISTING_ACTIVITY}/signup", params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert new_email in activities[EXISTING_ACTIVITY]["participants"]


def test_signup_duplicate_participant_fails(client):
    # Arrange
    # (EXISTING_PARTICIPANT is already signed up for EXISTING_ACTIVITY)

    # Act
    response = client.post(
        f"/activities/{EXISTING_ACTIVITY}/signup", params={"email": EXISTING_PARTICIPANT}
    )

    # Assert
    assert response.status_code == 400


def test_signup_activity_not_found(client):
    # Arrange
    bogus_activity = "Nonexistent Club"

    # Act
    response = client.post(
        f"/activities/{bogus_activity}/signup", params={"email": "someone@mergington.edu"}
    )

    # Assert
    assert response.status_code == 404


def test_unregister_participant_success(client):
    # Arrange
    # (EXISTING_PARTICIPANT is already signed up for EXISTING_ACTIVITY)

    # Act
    response = client.delete(
        f"/activities/{EXISTING_ACTIVITY}/unregister", params={"email": EXISTING_PARTICIPANT}
    )

    # Assert
    assert response.status_code == 200
    assert EXISTING_PARTICIPANT not in activities[EXISTING_ACTIVITY]["participants"]


def test_unregister_participant_not_registered_fails(client):
    # Arrange
    unregistered_email = "notsignedup@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{EXISTING_ACTIVITY}/unregister", params={"email": unregistered_email}
    )

    # Assert
    assert response.status_code == 400


def test_unregister_activity_not_found(client):
    # Arrange
    bogus_activity = "Nonexistent Club"

    # Act
    response = client.delete(
        f"/activities/{bogus_activity}/unregister", params={"email": EXISTING_PARTICIPANT}
    )

    # Assert
    assert response.status_code == 404
