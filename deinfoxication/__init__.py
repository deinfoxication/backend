"""Main application module."""
import glob
import importlib
import itertools
import os
from functools import lru_cache

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from sqlalchemy import MetaData
from sqlalchemy.orm.mapper import configure_mappers

convention = {
  'ix': 'ix_%(column_0_label)s',
  'uq': 'uq_%(table_name)s_%(column_0_name)s',
  'ck': 'ck_%(table_name)s_%(constraint_name)s',
  'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
  'pk': 'pk_%(table_name)s'
}

db = SQLAlchemy(metadata=MetaData(naming_convention=convention))


@lru_cache()
def _preload_models():
    """Preload models so, alembic can create the migrations properly."""
    base = os.path.dirname(__file__)
    models_files = glob.iglob(os.path.join(base, '**', 'models.py'), recursive=True)
    models_packages = glob.iglob(os.path.join(base, '**', 'models', '__init__.py'), recursive=True)
    for filename in itertools.chain(models_files, models_packages):
        package_name = filename.replace(base, __name__).replace(os.path.sep + '__init__.py', '').\
            replace(os.path.sep, '.').replace('.py', '')
        importlib.import_module(package_name)

    # Configure mappers trigger backrefs creation.
    # http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref
    configure_mappers()


def create_app():
    """Create deinfoxication app."""
    app = Flask(__name__)
    db.init_app(app)
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'configs.py'))
    import deinfoxication.views  # noqa
    app.register_blueprint(deinfoxication.views.default_blueprint)
    app.sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])

    _preload_models()

    return app
