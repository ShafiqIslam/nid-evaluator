from flask import Blueprint

evaluator = Blueprint('evaluator', __name__)
from . import routes
