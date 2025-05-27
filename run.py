"""Point d’entrée : démarre l’application Flask en mode debug sur le port 5001, pour éviter les conflits avec AirPlay sur mac"""

from app import create_app

app = create_app()

# ====== BLOC TEMPORAIRE POUR INITIALISER LA BASE DE DONNÉES SUR RENDER ======
# Ce bloc lance automatiquement la migration (création des tables) au démarrage,
# uniquement le temps d’initialiser la base sur Render (plan gratuit, pas de shell/job possible).
# Dès que tout fonctionne, SUPPRIME ce bloc et repousse le fichier sur GitHub !

from flask_migrate import upgrade

with app.app_context():
    upgrade()
# ====== FIN DU BLOC TEMPORAIRE ======

if __name__ == "__main__":
    app.run(debug=True, port=5001)
