#  Projet Meridian - Formulaire d'Inscription Sécurisé avec CI/CD, Cloud & Observabilité

##  Présentation du Projet
Ce projet consiste en la mise en place d'une infrastructure informatique moderne, sécurisée et entièrement automatisée (DevOps). Il permet à un utilisateur de créer un compte via un formulaire web en ligne, de transférer et stocker ces données de manière sécurisée dans le Cloud Microsoft Azure via une API Python, d'en suivre les performances en temps réel avec un outil d'observabilité de pointe, et de visualiser les résultats à l'aide d'un logiciel équipé d'un affichage de type **DataGrid**.

---

## Architecture du Système & Flux de Données

Pour des raisons strictes de sécurité, le projet respecte une architecture n-tiers afin de masquer et d'isoler totalement la base de données du public :
1. **Frontend (Le Site Web)** ➔ L'utilisateur remplit ses informations sur `https://cgramitservice.me`. Le script JavaScript intercepte la soumission, compile les champs dans un paquet au format texte standardisé (JSON) et l'envoie de manière asynchrone via HTTPS.
2. **Backend (L'API Passerelle)** ➔ Le serveur Python Flask reçoit le paquet JSON, applique le filtre de sécurité CORS pour rejeter les requêtes non autorisées, valide les données, puis ouvre une connexion cryptée vers la base de données.
3. **Database (Le Stockage)** ➔ Le serveur SQL Server insère les données de manière permanente dans la table dédiée.
4. **DataGrid Client (L'Administration)** ➔ L'administrateur, connecté à distance via un outil de gestion SQL, utilise un composant graphique **DataGrid** pour voir les nouveaux inscrits apparaître en temps réel grâce à une commande `SELECT`.
5. **Observabilité (La Surveillance)** ➔ L'agent New Relic capture les logs et chronomètre les transactions SQL en arrière-plan pour envoyer les rapports de performance au tableau de bord.

---

##  Technologies, Logiciels et Services Utilisés

###  Frontend & Zone DNS
*   **HTML5 / CSS3 / JavaScript (ES6)** : Conception de l'interface utilisateur graphique adaptative (Formulaire Meridian) et développement de la logique d'envoi asynchrone (`fetch()`).
*   **Azure Static Web Apps** : Service Cloud de Microsoft utilisé pour l'hébergement gratuit et optimisé du contenu web statique (`index.html` et dossiers d'assets).
*   **Namecheap** : Fournisseur du nom de domaine personnalisé. Utilisation du panneau DNS pour lier le sous-domaine `https://cgramitservice.me` au serveur Microsoft.

### ⚙️ Backend & API Python
*   **Python 3.14** : Langage de programmation principal exécuté côté serveur.
*   **Flask & Flask-CORS** : Framework micro-web gérant les routes HTTP. L'extension `flask-cors` lève les blocages de sécurité des navigateurs en limitant explicitement l'accès au seul domaine Namecheap autorisé.
*   **Gunicorn (Green Unicorn)** : Serveur HTTP WSGI de production pour Linux, configuré pour exécuter des processus en parallèle (Workers), gérant le multi-threading afin d'assurer la stabilité de l'API face aux connexions simultanées.
*   **Azure App Service (Plan Linux Free F1)** : Serveur d'hébergement cloud isolé configuré dans la région **East US 2** sous l'infrastructure gratuite des crédits *Azure for Students*.

### 🗄️ Base de Données & Outil SQL
*   **Azure SQL Database** : Base de données relationnelle hébergée dans le Cloud Azure.
*   **pyodbc** : Bibliothèque de connexion Python exploitant le pilote système natif `ODBC Driver 18 for SQL Server`.
*   **Database Explorer / Client SQL** : Logiciel d'administration lourd équipé d'un composant de type **DataGrid** pour administrer la base de données et visualiser l'état de la table en temps réel.

### 📦 DevOps & Observabilité
*   **GitHub Actions** : Plateforme d'intégration et de déploiement continus (CI/CD). Gestion de deux pipelines distincts (`.yml`) automatisant la publication du code à chaque `git push`.
*   **New Relic (GitHub Student Developer Pack)** : Plateforme d'observabilité de pointe configurée pour analyser l'intégrité de l'application, surveiller la vitesse des requêtes SQL (`INSERT INTO`) et centraliser la télémétrie des logs.

---

## 🗃️ Structure Finale du Répertoire du Projet

```text
MYFIRSTDEVOPSPROJECT_FORMNRWORKFLOW/
│
├── .github/
│   └── workflows/
│       ├── azure-static-web-apps-lively-glacier.yml   # Pipeline de déploiement automatique du Frontend
│       └── deploy-backend.yml                         # Pipeline de déploiement automatique du Backend Python
│
├── assets/
│   └── script.js                                      # Script JavaScript d'interception et d'envoi JSON
│
├── backend/                                           # Isolation logique de la couche Backend
│   ├── main.py                                        # API Flask (Routage et requêtes d'insertion SQL)
│   ├── newrelic.ini                                   # Fichier de configuration de l'agent New Relic
│   └── requirements.txt                               # Dépendances Python requises (Flask, pyodbc, gunicorn...)
│
├── index.html                                         # Formulaire d'inscription Meridian (À la racine)
└── .gitignore                                         # Fichiers exclus du suivi Git (Fichiers temporaires *.swp, etc.)
```

---

## 📝 Historique des Travaux & Étapes Réalisées

### Étape 1 : Développement du Formulaire et Logique JavaScript
*   Création de la structure du formulaire Meridian intégrant la validation des champs (Prénom, Nom, Email professionnel, Entreprise, Fonction, Taille de l'entreprise, Mot de passe et sa Confirmation).
*   Écriture de la logique d'interception dans `assets/script.js` bloquant le comportement HTML par défaut (`event.preventDefault()`) et expédiant l'objet JSON vers l'adresse finale du serveur de production Azure App Service.

### Étape 2 : Déploiement et Structuration d'Azure SQL
*   Initialisation du serveur cloud logique `christianitserver` et de la base de données `free-sql-db-9199039`.
*   Création et structuration de la table hôte via le panneau d'administration à l'aide de la requête SQL suivante :
    ```sql
    CREATE TABLE Clients (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        Prenom NVARCHAR(100) NOT NULL,
        Nom NVARCHAR(100) NOT NULL,
        Email NVARCHAR(255) NOT NULL UNIQUE,
        Entreprise NVARCHAR(150) NOT NULL,
        Fonction NVARCHAR(150) NOT NULL,
        TailleEntreprise NVARCHAR(50) NOT NULL,
        MotDePasse NVARCHAR(255) NOT NULL,
        DateInscription DATETIME DEFAULT GETDATE()
    );
    ```

### Étape 3 : Programmation et Sécurisation du Backend Python
*   Écriture de l'API Flask dans `backend/main.py` avec mise en place du filtre de sécurité `CORS` pointant vers `https://cgramitservice.me`.
*   Sécurisation absolue du projet : aucune clé secrète ni mot de passe de base de données n'est écrit en clair dans le code source. Le script utilise l'instruction générique `os.getenv()` pour lire ces secrets directement depuis la mémoire sécurisée du serveur.

### Étape 4 : Déploiement de l'Azure App Service Linux & Configuration New Relic
*   Création de la Web App Linux sous **Python 3.14** dans le groupe de ressources commun `static_web_deploy` situé dans la région **East US 2** afin de contourner les restrictions de quota des comptes étudiants.
*   Sélection du forfait **Free F1** (0 USD/mois) pour sécuriser le budget étudiant.
*   Configuration de la commande de démarrage (*Startup Command*) pour injecter l'agent de monitoring devant le serveur de production Gunicorn :
    ```bash
    NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn main:app --bind 0.0.0.0:8000
    ```
*   Injection sécurisée des variables d'environnement secrètes sur le portail Azure : `AZURE_SQL_CONNECTION_STRING` (complétée avec le Driver ODBC 18 et le mot de passe administrateur `gram-65878`) et `NEW_RELIC_LICENSE_KEY`.

### Étape 5 : Automatisation de la Chaîne CI/CD sur GitHub
*   Téléchargement du profil de publication d'Azure App Service (`.publishsettings`) et configuration dans les secrets du dépôt GitHub sous le nom exact de `AZURE_APP_SERVICE_PUBLISH_PROFILE`.
*   Création du fichier de workflow `.github/workflows/deploy-backend.yml` chargé d'isoler le dossier `backend/`, d'installer les dépendances listées dans `requirements.txt` (avec correction de la casse pour `flask-cors`), de zipper l'application et de la pousser de manière automatisée sur Azure à chaque push.

---

## 🏁 Procédure de Recette Fonctionnelle
Pour valider le fonctionnement complet du projet :
1.  Pousser les derniers fichiers vers le dépôt distant :
    ```bash
    git add .
    git commit -m "Publication de la version finale Meridian"
    git push origin main
    ```
2.  Vérifier que les deux pipelines passent au **vert** dans l'onglet **Actions** de GitHub.
3.  Accéder au site `https://cgramitservice.me` et soumettre une inscription via le formulaire.
4.  Exécuter un `SELECT * FROM Clients;` dans votre outil SQL pour voir la ligne s'ajouter instantanément dans votre interface de type **DataGrid**.
5.  Ouvrir la console cloud **New Relic**, aller dans le menu `APM & Services` pour analyser en direct les graphiques de performances et la vitesse de traitement de vos requêtes SQL.
