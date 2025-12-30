def test_list_users(client):
    # Currently uses InMemoryUserRepository which has 2 users by default
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert data[0]["name"] == "Alice"


def test_get_user_success(client):
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_get_user_not_found(client):
    response = client.get("/api/users/999")
    # Current implementation returns null for nonexistent users with 200 OK
    assert response.status_code == 200
    assert response.json() is None
