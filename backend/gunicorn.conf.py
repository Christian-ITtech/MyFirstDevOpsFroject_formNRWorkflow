import os

# Configuration de production Gunicorn pour Azure App Service
port = os.environ.get("PORT", 8000)
bind = f"0.0.0.0:{port}"

workers = 2 
timeout = 600 
loglevel = "info"

# Point d'entrée mis à jour avec le nouveau nom du fichier (app.py)
wsgi_app = "backend.app:app"


