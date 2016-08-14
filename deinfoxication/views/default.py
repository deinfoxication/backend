from flask import jsonify

from deinfoxication.views import default_blueprint


@default_blueprint.route('/')
def index():
    return jsonify({'it': 'works'})
