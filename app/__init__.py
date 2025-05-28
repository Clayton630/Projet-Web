"""Initialisation de l’application Flask et de ses extensions."""

# On importe les modules nécessaires :
from flask import Flask                    # Le cœur du framework web Flask
from flask_sqlalchemy import SQLAlchemy    # Pour gérer la base de données SQL facilement (ORM)
from flask_login import LoginManager       # Pour gérer l’authentification (sessions, utilisateurs connectés)

# On crée une instance SQLAlchemy, sans l’associer tout de suite à l’application
db = SQLAlchemy()

# On crée un gestionnaire d’authentification (login manager), idem
login_manager = LoginManager()


def create_app():
    """
    Fonction « factory » qui instancie l’application Flask,
    configure toutes les extensions (SQLAlchemy, LoginManager),
    et enregistre les blueprints (modules de routes).
    Elle retourne l’objet application Flask prêt à être lancé.
    """

    # On crée l’application Flask principale (le site)
    app = Flask(__name__)

    # On charge la configuration à partir du fichier config.py, classe Config
    app.config.from_object("config.Config")

    # On initialise les extensions avec l’application :
    db.init_app(app)                # Connecte la base de données à l’app Flask
    login_manager.init_app(app)     # Active le gestionnaire de connexion

    # On importe le blueprint des routes principales (après l’app pour éviter les références circulaires)
    from .routes import main  # noqa: WPS433 (cette notation permet d’ignorer un warning du linter sur l'import interne)
    from . import models      # Importe les modèles SQLAlchemy (User, Etablissement, etc.)

    # On enregistre le blueprint sur l’application (toutes les routes de `main` deviennent actives)
    app.register_blueprint(main)

    # On définit la page de login par défaut (si l’utilisateur n’est pas connecté, Flask-Login le redirige ici)
    login_manager.login_view = "main.login"

    # On indique à Flask-Login comment charger un utilisateur à partir de son identifiant stocké en session
    @login_manager.user_loader
    def load_user(user_id):
        # On cherche l’utilisateur dans la base via son id (doit retourner un objet User ou None)
        return models.User.query.get(int(user_id))

    # On retourne l’app Flask prête à être lancée (par un serveur ou flask run)
    return app
