from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object('server.app.config.Config')


    db.init_app(app)
    ma.init_app(app)

    from .views import views
    app.register_blueprint(views)

    return app
