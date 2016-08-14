import os

from flask import Flask


def create_app():
    """Create deinfoxication app."""
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'configs.py'))
    return app
