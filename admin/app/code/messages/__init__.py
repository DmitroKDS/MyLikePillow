from flask import Blueprint

bp = Blueprint('messages', __name__)

from . import routes