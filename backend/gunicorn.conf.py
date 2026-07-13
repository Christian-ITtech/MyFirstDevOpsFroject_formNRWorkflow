# Configuration de production Gunicorn pour Azure App Service
import os

bind = "0.0.0.0:8000"
workers = 2  # Limite le nombre de processus pour économiser la mémoire gratuite
timeout = 600  # Monte le délai d'attente à 10 minutes pour éviter le ContainerTimeout
loglevel = "info"
