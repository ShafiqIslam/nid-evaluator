from flask import Flask

from app.controllers.nid_parser import nid_parser


def register_modules(application: Flask):
    application.register_blueprint(nid_parser)
    return application
