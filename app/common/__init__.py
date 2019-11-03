from flask import request
import logging
from app.config import App

Request = request


def init_sentry():
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    sentry_sdk.init(
        dsn=App.sentry_dsn,
        integrations=[FlaskIntegration(), SqlalchemyIntegration(), RedisIntegration()]
    )


def attach_sentry_wsgi(app):
    from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
    return SentryWsgiMiddleware(app)


def attach_gunicorn_logger(app):
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
