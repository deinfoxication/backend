"""Main application module."""
import os

from flask import Flask
from raven.contrib.flask import Sentry


def create_app():
    """Create deinfoxication app."""
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'configs.py'))
    import deinfoxication.views  # noqa
    app.register_blueprint(deinfoxication.views.default_blueprint)
    app.sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])
    return app
