import os
import pyodbc
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Activation du CORS pour autoriser votre site en ligne
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "https://form.cgramitservice.me"  # Votre domaine Namecheap
            ]
        }
    },
)


def get_db_connection():
    """Récupère la chaîne de connexion sécurisée depuis Azure."""
    conn_string = os.getenv("AZURE_SQL_CONNECTION_STRING")
    if not conn_string:
        raise RuntimeError(
            "La variable AZURE_SQL_CONNECTION_STRING est manquante."
        )
    return pyodbc.connect(conn_string)


@app.route("/soumettre-formulaire", methods=["POST"])
def soumettre_formulaire():
    data = request.get_json()

    # Récupération de tous les champs
    prenom = data.get("prenom")
    nom = data.get("nom")
    email = data.get("email")
    entreprise = data.get("entreprise")
    poste = data.get("poste")
    taille = data.get("taille")
    motdepasse = data.get("motdepasse")

    # Vérification stricte
    if not all([prenom, nom, email, entreprise, poste, taille, motdepasse]):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Tous les champs requis doivent être remplis.",
                }
            ),
            400,
        )

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Requête SQL propre et alignée
        query = """INSERT INTO Clients (Prenom, Nom, Email, Entreprise, Fonction, TailleEntreprise, MotDePasse) VALUES (?, ?, ?, ?, ?, ?, ?)"""

        cursor.execute(
            query, (prenom, nom, email, entreprise, poste, taille, motdepasse)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Votre compte Meridian a été créé avec succès !",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run()
