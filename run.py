from werkzeug.middleware.proxy_fix import ProxyFix
from app import create_app
from app.common import attach_gunicorn_logger, attach_sentry_wsgi
from app.config import App

app = create_app()

if (__name__ != '__main__') and (App.enable_gunicorn_logger == 'True'):
    attach_gunicorn_logger(app)


def run():
    app.run(App.debug, App.host, App.port)


wsgi = ProxyFix(app.wsgi_app)
if App.init_sentry == 'True':
    wsgi = attach_sentry_wsgi(wsgi)
if __name__ == '__main__':
    run()
