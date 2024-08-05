from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import os

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('server.app.config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zuri_trends.db'

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    app.register_blueprint(views)

    return app
