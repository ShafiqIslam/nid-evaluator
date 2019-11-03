from flask import Flask
from .middlewares import after_request_middleware, before_request_middleware, teardown_appcontext_middleware
from .middlewares import response
from .controllers import register_modules
from app.config import DB, App


def create_app():
    # initialize flask application
    application = Flask(__name__)

    # load_config()
    # register all blueprints
    application = register_modules(application)

    # register custom response class
    application.response_class = response.JSONResponse

    # register before request middleware
    before_request_middleware(app=application)

    # register after request middleware
    after_request_middleware(app=application)

    # register after app context teardown middleware
    teardown_appcontext_middleware(app=application)

    # register custom error handler
    response.json_error_handler(app=application)

    # initialize the database
    if App.init_db == 'True':
        from .common.database import init_db
        init_db(application)

    return application
