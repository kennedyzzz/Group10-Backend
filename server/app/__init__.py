from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from server.app.config import Config

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zuri_trends.db'
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from server.app.views import views
    app.register_blueprint(views)

    with app.app_context():
        db.create_all()

    return app
