from flask.blueprints import Blueprint

default_blueprint = Blueprint('default', __name__)

import deinfoxication.views.default  # flake8: noqa
