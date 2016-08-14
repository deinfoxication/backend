#!/usr/bin/env python
"""Manage file."""
import subprocess

import click
from prettyconf import config

from deinfoxication import create_app


@click.group()
def manager():
    pass


@manager.command()
def runserver(host='0.0.0.0', port=8000, debug=None):
    """Runserver."""
    app = create_app()
    if debug is None:
        debug = config('DEBUG')
    app.run(host, port, debug)


@manager.command()
@click.option('--fix', default=False, is_flag=True)
def isort(fix=False):
    """Check if imports are in the right order."""
    print('Checking files sorting...')
    args = ['isort', '-rc']
    if not fix:
        args.append('-c')
    subprocess.check_call(args)


@manager.command()
def tests():
    """Run py.test."""
    print('Running tests...')
    subprocess.check_call(['py.test', 'tests/'])

if __name__ == '__main__':
    manager()
