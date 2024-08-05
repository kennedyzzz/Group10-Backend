from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import base64
import os
from werkzeug.utils import secure_filename

db = SQLAlchemy()
ma = Marshmallow()
CORS = CORS()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object('app.config.Config')

    db.init_app(app)
    ma.init_app(app)
    CORS(app)

    # API keys and configuration
    global consumer_key, consumer_secret, shortcode, lipa_na_mpesa_online_passkey, callback_url, fixed_phone_number
    consumer_key = app.config['CONSUMER_KEY']
    consumer_secret = app.config['CONSUMER_SECRET']
    shortcode = app.config['SHORTCODE']
    lipa_na_mpesa_online_passkey = app.config['LIPA_NA_MPESA_ONLINE_PASSKEY']
    callback_url = app.config['CALLBACK_URL']
    fixed_phone_number = app.config['FIXED_PHONE_NUMBER']

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    def get_access_token():
        api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        return response.json()['access_token']

    def lipa_na_mpesa_online(amount, phone_number):
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
            "AccountReference": "ZuriTrends",
            "TransactionDesc": "Payment for goods"
        }

        response = requests.post(api_url, json=payload, headers=headers)
        return response.json()

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @app.route('/upload_image', methods=['POST'])
    def upload_image():
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

        return jsonify({'message': 'Invalid file type'}), 400

    from . import views

    return app
