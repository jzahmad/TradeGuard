from tests.conftest import auth_header, login_user, register_user


def test_register_success(client):
    response = register_user(client, username="newtrader", password="password123")

    assert response.status_code == 201
    body = response.get_json()
    assert body["user"]["username"] == "newtrader"
    assert body["user"]["role"] == "TRADER"
    assert "password" not in body["user"]


def test_register_missing_fields(client):
    response = client.post("/api/auth/register", json={"username": "onlyusername"})

    assert response.status_code == 400
    assert "fields" in response.get_json()


def test_register_duplicate_username(client):
    register_user(client, username="dupe", email="first@example.com")
    response = register_user(client, username="dupe", email="second@example.com")

    assert response.status_code == 409
    assert "Username" in response.get_json()["error"]


def test_register_duplicate_email(client):
    register_user(client, username="user_a", email="shared@example.com")
    response = register_user(client, username="user_b", email="shared@example.com")

    assert response.status_code == 409
    assert "Email" in response.get_json()["error"]


def test_login_success(client):
    register_user(client, username="loginuser", password="password123")
    response = client.post(
        "/api/auth/login",
        json={"username": "loginuser", "password": "password123"},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert "access_token" in body
    assert body["user"]["username"] == "loginuser"


def test_login_wrong_password(client):
    register_user(client, username="wrongpw", password="password123")
    response = client.post(
        "/api/auth/login",
        json={"username": "wrongpw", "password": "not-the-password"},
    )

    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "ghost", "password": "password123"},
    )

    assert response.status_code == 401


def test_me_requires_auth(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401


def test_me_with_valid_token(client):
    register_user(client, username="meuser", password="password123")
    token = login_user(client, username="meuser", password="password123")

    response = client.get("/api/auth/me", headers=auth_header(token))

    assert response.status_code == 200
    assert response.get_json()["username"] == "meuser"
