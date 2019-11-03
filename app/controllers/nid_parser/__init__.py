from flask import Blueprint

nid_parser = Blueprint('nid_parser', __name__)
from .routes import *
