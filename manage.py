#!/usr/bin/env python
"""Manage file."""
import os
import subprocess

import click
from flask_click_migrate import MigrateGroup
from IPython.terminal import embed
from prettyconf import config

from deinfoxication import celery as celery_instance, create_app, migrate
from deinfoxication.utils import app_context

app = create_app()
migrate_group = MigrateGroup(migrate_instance=migrate)


@click.group()
def manager():
    """Click group for manager commands."""
    pass


@manager.command()
def runserver(host="0.0.0.0", port=8000, debug=None):
    """Runserver."""
    app = create_app()
    if debug is None:
        debug = config("DEBUG")
    app.run(host, port, debug)


@manager.command()
@click.option("--fix", default=False, is_flag=True)
def isort(fix=False):
    """Check if imports are in the right order."""
    print("Checking files sorting...")
    args = ["isort", "-rc"]
    if not fix:
        args.append("-c")
    args.extend(["deinfoxication", os.path.join("migrations", "versions"), "tests"])
    if subprocess.call(args) != 0:
        exit(1)


@manager.command()
@click.argument("extra_args", nargs=-1)
def tests(extra_args):
    """Run py.test."""
    print("Running tests...")
    args = ["py.test", "tests/"]
    if subprocess.call(args + list(extra_args)) != 0:
        exit(1)


@manager.command()
def flake8():
    """Run flake8."""
    print("Running flake8...")
    if subprocess.call(["flake8"]) != 0:
        exit(1)


@manager.command()
@click.pass_context
def build(ctx):
    """Run all pre-commit commands."""
    for task in (isort, flake8, tests):
        ctx.invoke(task)


@manager.command()
@app_context
def shell():
    """Open a interactive shell with the current global variables."""
    embed.embed()


@manager.command()
@click.argument("extra_args", nargs=-1)
@click.pass_context
def celery(ctx, extra_args):
    """Celery command."""
    ctx.exit(celery_instance.worker_main(list(extra_args)))


if __name__ == "__main__":
    app = create_app()
    manager.add_command(migrate_group)
    with app.app_context():
        manager()
