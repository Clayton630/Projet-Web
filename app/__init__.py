"""Initialisation de l’application Flask et de ses extensions."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Instancie l’application, configure les extensions et enregistre les blueprints."""
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main  # noqa: WPS433  (import inside factory)
    from . import models

    app.register_blueprint(main)
    login_manager.login_view = "main.login"

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app
