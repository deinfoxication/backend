import os

from flask import Flask


def create_app():
    """Create deinfoxication app."""
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'configs.py'))
    import deinfoxication.views  # flake8: noqa
    app.register_blueprint(deinfoxication.views.default_blueprint)
    return app
