from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import re
from markupsafe import Markup

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)
    app.config.from_object(Config)
    db.init_app(app)
    app.jinja_env.filters['linkify'] = linkify

    return app


def linkify(text):
    if not text:
        return ""
    url_pattern = r'(https?://[^\s]+)'
    return Markup(re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text))