import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('server.app.config.Config')
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
