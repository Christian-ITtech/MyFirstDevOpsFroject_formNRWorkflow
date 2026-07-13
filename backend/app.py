import os
import pyodbc
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Autorise toutes les origines Web à envoyer des données de formulaire de manière securisee
CORS(app, resources={r"/*": {"origins": "*"}})


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

    prenom = data.get('prenom')
    nom = data.get('nom')
    email = data.get('email')
    entreprise = data.get('entreprise')
    poste = data.get('poste')
    taille = data.get('taille')
    motdepasse = data.get('motdepasse')

    if not all([prenom, nom, email, entreprise, poste, taille, motdepasse]):
        return jsonify({"status": "error", "message": "Tous les champs requis doivent être remplis."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
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

    except pyodbc.IntegrityError:
        # Violation de contrainte (ex : email déjà utilisé) → message générique, sans détail technique
        return jsonify({
            "status": "error",
            "message": "Un compte existe déjà avec cet email."
        }), 409

    except Exception as e:
        # Toute autre erreur inattendue : on logue le détail côté serveur (visible dans New Relic / Log stream)
        # mais on ne le renvoie JAMAIS tel quel au client
        app.logger.error(f"Erreur lors de la création du compte : {e}")
        return jsonify({
            "status": "error",
            "message": "Une erreur est survenue. Veuillez réessayer plus tard."
        }), 500

# Note : app.run() est retiré car c'est Gunicorn qui gère le démarrage en production sur Azure
