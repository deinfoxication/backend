"""Views module."""
# isort:skip_file
from flask.blueprints import Blueprint

default_blueprint = Blueprint("default", __name__)

import deinfoxication.views.default  # noqa: F401
