import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///zuri_trends.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    CONSUMER_KEY = 'your_consumer_key'
    CONSUMER_SECRET = 'your_consumer_secret'
    SHORTCODE = '174379'
    LIPA_NA_MPESA_ONLINE_PASSKEY = 'your_passkey'
    CALLBACK_URL = 'https://your_callback_url.com/callback'
    FIXED_PHONE_NUMBER = '0115743312'
