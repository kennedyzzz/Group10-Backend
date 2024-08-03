from flask import Flask, request, render_template, redirect, url_for, flash
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

consumer_key = 'yty83hjgw0EEGrxoV9j3AAQxVJL2hmjcvYMPxsjXH2ghL8AF'
consumer_secret = 'asJhwuTM0XXBWyTJwCWgPWITuucxPoDkNiQWfeTQGgjGraLyl5KO6Ay93sxrSwIm'
shortcode = '174379' 
lipa_na_mpesa_online_passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
callback_url = 'https://your_callback_url.com/callback'

def get_access_token():
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return response.json()['access_token']

def lipa_na_mpesa_online(phone_number, amount):
    access_token = get_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': f'Bearer {access_token}'}

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = shortcode + lipa_na_mpesa_online_passkey + timestamp
    encoded_string = base64.b64encode(data_to_encode.encode())
    password = encoded_string.decode('utf-8')

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": "Test123",
        "TransactionDesc": "Payment for goods"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        amount = request.form['amount']
        if phone_number and amount:
            response = lipa_na_mpesa_online(phone_number, amount)
            flash('Payment request sent. Please check your phone to complete the transaction.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Please enter a valid phone number and amount.', 'danger')
    return render_template('index.html')

@app.route('/callback', methods=['POST'])
def mpesa_callback():
    mpesa_response = request.get_json()
    print(mpesa_response)
    
    return {"ResultCode": 0, "ResultDesc": "Accepted"}, 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
