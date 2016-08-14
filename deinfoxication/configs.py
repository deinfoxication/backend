"""Configs file, it should not have logic."""
from prettyconf import config

DEBUG = config('DEBUG', cast=config.boolean)
