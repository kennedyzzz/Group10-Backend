import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '90a09368e4cd6ebb31edcb00562d0785')  
    SQLALCHEMY_DATABASE_URI = 'sqlite:///zuri_trends.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    CONSUMER_KEY = 'yty83hjgw0EEGrxoV9j3AAQxVJL2hmjcvYMPxsjXH2ghL8AF'
    CONSUMER_SECRET = 'asJhwuTM0XXBWyTJwCWgPWITuucxPoDkNiQWfeTQGgjGraLyl5KO6Ay93sxrSwIm'
    SHORTCODE = '174379'
    LIPA_NA_MPESA_ONLINE_PASSKEY = 'your_passkey'
    CALLBACK_URL = 'https://your_callback_url.com/callback'
    FIXED_PHONE_NUMBER = '0115743312'
