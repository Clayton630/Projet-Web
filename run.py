"""Point d’entrée : démarre l’application Flask en mode debug sur le port 5001, pour éviter les conflits avec AirPlay sur mac"""

# Importe la fonction qui crée l’application Flask depuis le package `app`
from app import create_app

# Appelle la factory pour obtenir une instance Flask déjà configurée
app = create_app()

# Si ce fichier est lancé directement (et non importé), on lance le serveur Flask
if __name__ == "__main__":
    # Lance l’application :
    # - debug=True : rechargement automatique à chaque changement de code + affichage des erreurs détaillées
    # - port=5001  : lance sur le port 5001 (utile sur Mac, car AirPlay peut bloquer le port 5000 par défaut)
    app.run(debug=True, port=5001)
