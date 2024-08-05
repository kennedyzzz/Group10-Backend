from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    from .models import db, ma
    db.init_app(app)
    ma.init_app(app)

    from .views import main
    app.register_blueprint(main)

    return app

app = create_app()
