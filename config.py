"""Configuration principale de l’application Flask."""

class Config:
    """Paramètres globaux (adapter pour la production)."""

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/retoursdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "un-truc-ultra-secret-et-unique"