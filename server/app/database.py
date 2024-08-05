from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)


    from server.app.views import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)


    with app.app_context():
        db.create_all()

    return app