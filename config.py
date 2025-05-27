"""Configuration principale de l’application Flask."""

import os

class Config:
    """Paramètres globaux adaptés pour la production Render."""

    # La chaîne de connexion à la base de données sera lue dans les variables d'environnement
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
