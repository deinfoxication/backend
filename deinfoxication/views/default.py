"""Default views."""
from flask import jsonify

from deinfoxication.views import default_blueprint


@default_blueprint.route('/')
def index():
    """Index of the API."""
    return jsonify({'it': 'works'})
