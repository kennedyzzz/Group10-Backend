from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint, url_prefix='/api')

    CORS(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
