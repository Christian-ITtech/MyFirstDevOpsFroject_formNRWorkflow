import os
import pyodbc
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Activation du CORS pour autoriser uniquement votre site en ligne Namecheap
CORS(app, resources={r"/*": {"origins": ["https://form.cgramitservice.me"]}})

def get_db_connection():
    """Récupère la chaîne de connexion sécurisée depuis les variables Azure."""
    conn_string = os.getenv("AZURE_SQL_CONNECTION_STRING")
    if not conn_string:
        raise RuntimeError("La variable AZURE_SQL_CONNECTION_STRING est introuvable.")
    return pyodbc.connect(conn_string)

@app.route('/soumettre-formulaire', methods=['POST'])
def soumettre_formulaire():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Aucune donnée reçue."}), 400

    # Extraction des clés (alignées à 100% avec les minuscules du fichier script.js)
    prenom = data.get('prenom')
    nom = data.get('nom')
    email = data.get('email')
    entreprise = data.get('entreprise')
    poste = data.get('poste')
    taille = data.get('taille')
    motdepasse = data.get('motdepasse') # CORRECTION : Tout en minuscules !

    # Vérification de sécurité stricte
    if not all([prenom, nom, email, entreprise, poste, taille, motdepasse]):
        return jsonify({"status": "error", "message": "Tous les champs requis doivent être remplis."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Requête d'insertion dans la table Azure SQL
        query = """
            INSERT INTO Clients (Prenom, Nom, Email, Entreprise, Fonction, TailleEntreprise, MotDePasse)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (prenom, nom, email, entreprise, poste, taille, motdepasse))
        conn.commit()
        
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Votre compte Meridian a été créé avec succès !"
        }), 200

    except Exception as e:
        # Renvoie l'erreur SQL ou système exacte pour l'analyser dans la console du navigateur
        return jsonify({"status": "error", "message": str(e)}), 500

# Note : app.run() est retiré car c'est Gunicorn qui gère le démarrage en production sur Azure
