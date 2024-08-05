import sys
import os
from flask.cli import FlaskGroup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))

from app import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)

if __name__ == "__main__":
    cli()
