from flask import Flask

from app.controllers.evaluator import evaluator


def register_modules(application: Flask):
    application.register_blueprint(evaluator)
    return application
