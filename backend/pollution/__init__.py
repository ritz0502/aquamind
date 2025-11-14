from flask import Blueprint

pollution = Blueprint("pollution", __name__)

from . import routes
