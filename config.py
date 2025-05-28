"""Configuration principale de l’application Flask."""

class Config:
    """Paramètres globaux (adapter pour la production)."""

    # Chaîne de connexion à la base de données MySQL.
    # Format : mysql+pymysql://utilisateur:motdepasse@adresse:port/nomdelabase
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/retoursdb"

    # Désactive la détection automatique de modification des objets (économie de ressources).
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clé secrète Flask utilisée pour sécuriser les sessions, cookies, etc.
    # !!! À personnaliser en production (doit être très longue, unique et secrète)
    SECRET_KEY = "un-truc-ultra-secret-et-unique"
