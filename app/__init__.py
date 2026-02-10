from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)
    app.config.from_object(Config)
    db.init_app(app)

    return app