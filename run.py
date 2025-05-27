"""Point d’entrée : démarre l’application Flask en mode debug sur le port 5001, pour éviter les conflits avec AirPlay sur mac"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
