from . import db

class User(db.Model):
    __tablename__ = 'Utilisateurs'
    id_user = db.Column(db.Integer, primary_key=True)
    mot_de_passe = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    isadmin = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<User {self.nom}>"