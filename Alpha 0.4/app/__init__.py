from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    login_manager.init_app(app)
    
    from .routes import main
    from . import models
    
    app.register_blueprint(main)

    # Définir la route de redirection après une connexion
    login_manager.login_view = 'main.login'

    # Définir la méthode user_loader pour flask-login
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))
    
    return app