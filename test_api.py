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
