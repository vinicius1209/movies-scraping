from flask import Blueprint

movie_bp = Blueprint('movie_bp', __name__, url_prefix='/movies', template_folder='templates', static_folder='static')

from . import routes