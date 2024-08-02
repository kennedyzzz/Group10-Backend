import requests
from unittest.mock import patch

BASE_URL = "http://localhost:3000"


def mock_mpesa_payment(payment_data):

    return {
        "status": "success",
        "message": "Payment processed successfully",
        "transaction_id": payment_data.get("transaction_id"),
    }


@patch("requests.post", side_effect=mock_mpesa_payment)
def test_payment_mpesa_mocked(mock_post):
    url = f"{BASE_URL}/payment"
    data = {
        "order_id": 2,
        "payment_method": "mpesa",
        "amount": 150,
        "mpesa_number": "0712345678",
        "transaction_id": "MPESA123456",
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("message") == "Payment processed successfully"
    assert response_json.get("transaction_id") == "MPESA123456"
