from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Chaîne de connexion fournie par Microsoft Azure
AZURE_CONN_STRING = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:votre-serveur-azure.database.windows.net,1433;"
    "Database=nom_de_votre_bdd;"
    "Uid=votre_utilisateur;"
    "Pwd=votre_mot_de_passe;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

@app.route('/soumettre-formulaire', methods=['POST'])
def soumettre_formulaire():
    data = request.get_json()
    nom = data.get('nom')
    email = data.get('email')

    try:
        # 1. Connexion directe à la base de données SQL dans le Cloud Azure
        conn = pyodbc.connect(AZURE_CONN_STRING)
        cursor = conn.cursor()

        # 2. Requête SQL pour insérer les données du formulaire
        query = "INSERT INTO Clients (Nom, Email) VALUES (?, ?)"
        cursor.execute(query, (nom, email))
        
        # 3. Validation et fermeture
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "message": "Données enregistrées dans Azure (et bientôt synchronisées en local) !"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
