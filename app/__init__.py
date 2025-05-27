from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate    # <-- AJOUTÉ

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()                  # <-- AJOUTÉ

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)        # <-- AJOUTÉ
    login_manager.init_app(app)

    from .routes import main
    from . import models

    app.register_blueprint(main)
    login_manager.login_view = "main.login"

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app
