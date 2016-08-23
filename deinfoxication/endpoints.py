"""Application endpoints."""
from flask_restless import APIManager

import deinfoxication.views
from deinfoxication.feed.models import Feed
from deinfoxication.feed.schemas import FeedSchema, validation_for


def register_endpoints(app, db):
    """Register application endpoints."""
    app.register_blueprint(deinfoxication.views.default_blueprint)

    # Create other API endpoints using Flask-Restless.
    manager = APIManager(app, flask_sqlalchemy_db=db)
    with app.app_context():
        manager.create_api(Feed, methods=['GET', 'POST', 'PUT', 'DELETE'], **validation_for(Feed, FeedSchema))
