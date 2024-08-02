import requests

BASE_URL = "http://localhost:3000/"  

def test_signup():
    url = f"{BASE_URL}/signup"
    data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201
    assert response.json().get("message") == "User created successfully"

    def test_login():
     url = f"{BASE_URL}/login"
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert "token" in response.json()

def test_home():
    url = f"{BASE_URL}/home"
    response = requests.get(url)
    assert response.status_code == 200
    assert "welcome_message" in response.json()

