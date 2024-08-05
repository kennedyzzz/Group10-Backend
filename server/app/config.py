import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '90a09368e4cd6ebb31edcb00562d0785')
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')
    if not os.path.exists(INSTANCE_PATH):
        os.makedirs(INSTANCE_PATH)
    
    DATABASE_PATH = os.getenv('DATABASE_PATH', os.path.join(BASE_DIR, 'zuri_trends.db'))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads/')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    CONSUMER_KEY = os.getenv('CONSUMER_KEY', 'yty83hjgw0EEGrxoV9j3AAQxVJL2hmjcvYMPxsjXH2ghL8AF')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET', 'asJhwuTM0XXBWyTJwCWgPWITuucxPoDkNiQWfeTQGgjGraLyl5KO6Ay93sxrSwIm')
    SHORTCODE = os.getenv('SHORTCODE', '174379')
    LIPA_NA_MPESA_ONLINE_PASSKEY = os.getenv('LIPA_NA_MPESA_ONLINE_PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')
    CALLBACK_URL = os.getenv('CALLBACK_URL', 'https://mydomain.com/path')
    FIXED_PHONE_NUMBER = os.getenv('FIXED_PHONE_NUMBER', '0115743312')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
