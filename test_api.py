import requests

BASE_URL = "http://localhost:3000/" 


def validate_response(response, expected_status, expected_keys=None):
    assert response.status_code == expected_status
    if expected_keys:
        response_json = response.json()
        for key in expected_keys:
            assert key in response_json

def test_signup():
    url = f"{BASE_URL}/signup"
    data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com"
    }
    response = requests.post(url, json=data)
    validate_response(response, 201, ["message"])

def test_login():
    url = f"{BASE_URL}/login"
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = requests.post(url, json=data)
    validate_response(response, 200, ["token"])

def test_home():
    url = f"{BASE_URL}/home"
    response = requests.get(url)
    validate_response(response, 200, ["welcome_message"])

def test_catalog_create():
    url = f"{BASE_URL}/catalog"
    data = {
        "name": "New Category"
    }
    response = requests.post(url, json=data)
    validate_response(response, 201, ["id", "name"])

def test_catalog_read():
    url = f"{BASE_URL}/catalog"
    response = requests.get(url)
    validate_response(response, 200, ["categories"])

def test_catalog_update():
    url = f"{BASE_URL}/catalog/1"  
    data = {
        "name": "Updated Category Name"
    }
    response = requests.put(url, json=data)
    validate_response(response, 200, ["id", "name"])

def test_catalog_delete():
    url = f"{BASE_URL}/catalog/1"  
    response = requests.delete(url)
    validate_response(response, 200, ["message"])

def test_cart_add():
    url = f"{BASE_URL}/cart/add"
    data = {
        "product_id": 1,
        "quantity": 2
    }
    response = requests.post(url, json=data)
    validate_response(response, 200, ["message"])

def test_cart_view():
    url = f"{BASE_URL}/cart"
    response = requests.get(url)
    validate_response(response, 200, ["items"])

def test_wishlist_add():
    url = f"{BASE_URL}/wishlist/add"
    data = {
        "product_id": 1
    }
    response = requests.post(url, json=data)
    validate_response(response, 200, ["message"])

def test_wishlist_view():
    url = f"{BASE_URL}/wishlist"
    response = requests.get(url)
    validate_response(response, 200, ["items"])

def test_contact():
    url = f"{BASE_URL}/contact"
    data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "message": "This is a test message"
    }
    response = requests.post(url, json=data)
    validate_response(response, 200, ["message"])

def test_payment_credit_card():
    url = f"{BASE_URL}/payment"
    data = {
        "order_id": 1,
        "payment_method": "credit_card",
        "amount": 100
    }
    response = requests.post(url, json=data)
    validate_response(response, 200, ["message"])

def test_payment_mpesa():
    url = f"{BASE_URL}/payment"
    data = {
        "order_id": 2,
        "payment_method": "mpesa",
        "amount": 150,
        "mpesa_number": "0712345678",
        "transaction_id": "MPESA123456"
    }
    response = requests.post(url, json=data)
    validate_response(response, 200, ["message"])

def test_review_add():
    url = f"{BASE_URL}/review"
    data = {
        "product_id": 1,
        "rating": 5,
        "review": "Great product!"
    }
    response = requests.post(url, json=data)
    validate_response(response, 201, ["message"])

def test_review_view():
    url = f"{BASE_URL}/review/1"  
    response = requests.get(url)
    validate_response(response, 200, ["reviews"])

