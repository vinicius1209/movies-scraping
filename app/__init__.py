from flask import Flask
from . import config 

# App definitions
app = Flask(__name__)
app.config.from_object(config.Config) 

# Import blueprints
from .movies import movie_bp

app.register_blueprint(movie_bp)

def execute_app():
    return app
