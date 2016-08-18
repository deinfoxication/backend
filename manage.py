#!/usr/bin/env python
"""Manage file."""
import os
import subprocess

import click
from IPython.terminal.embed import embed
from prettyconf import config

from deinfoxication import create_app


@click.group()
def manager():
    """Click group for manager commands."""
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
    args.extend(['deinfoxication', os.path.join('migrations', 'versions'), 'tests'])
    if subprocess.call(args) != 0:
        exit(1)


@manager.command()
def tests():
    """Run py.test."""
    print('Running tests...')
    if subprocess.call(['py.test', 'tests/']) != 0:
        exit(1)


@manager.command()
def flake8():
    """Run flake8."""
    print('Running flake8...')
    if subprocess.call(['flake8']) != 0:
        exit(1)


@manager.command()
@click.pass_context
def build(ctx):
    """Run all pre-commit commands."""
    for task in (isort, flake8, tests):
        ctx.invoke(task)


@manager.command()
def shell():
    """Open a interactive shell with the current global variables."""
    embed()


    for task in (flake8, tests, isort):
        ctx.invoke(task)


if __name__ == '__main__':
    manager()
