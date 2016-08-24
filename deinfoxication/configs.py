"""Configs file, it should not have logic."""
from prettyconf import config

DEBUG = config('DEBUG', cast=config.boolean)
SERVER_NAME = config('SERVER_NAME')
SENTRY_DSN = config('SENTRY_DSN', default=None)

SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS')

BROKER_URL = config('BROKER_URL')
