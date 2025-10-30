from urllib.parse import quote


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister(client):
    activity = "Chess Club"
    encoded = quote(activity, safe="")
    email = "tester@example.com"

    # Ensure not present initially
    assert email not in client.get("/activities").json()[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{encoded}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Participant should appear
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]

    # Unregister
    resp2 = client.post(f"/activities/{encoded}/unregister", params={"email": email})
    assert resp2.status_code == 200
    assert "Unregistered" in resp2.json().get("message", "")

    data2 = client.get("/activities").json()
    assert email not in data2[activity]["participants"]


def test_signup_existing_returns_400(client):
    # michael@mergington.edu is already in Chess Club from the seed data
    activity = "Chess Club"
    encoded = quote(activity, safe="")
    resp = client.post(f"/activities/{encoded}/signup", params={"email": "michael@mergington.edu"})
    assert resp.status_code == 400
