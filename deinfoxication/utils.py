"""Common utilities."""
from functools import lru_cache, wraps

from flask.globals import _app_ctx_stack

from deinfoxication import create_app


@lru_cache(1)
def get_app():
    """Get a cached version of the current app or create a new one and push to the stack."""
    if _app_ctx_stack.top:
        return _app_ctx_stack.top
    return create_app()


def app_context(func):
    """Put the main app in context for the decorated function."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        """Check if the app is already in the stack and if it is not push it."""
        app = get_app()
        if _app_ctx_stack.top:
            return func(*args, **kwargs)

        ctx = app.app_context()
        ctx.push()
        try:
            return func(*args, **kwargs)
        finally:
            ctx.pop()

    return wrapped
