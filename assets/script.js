document.addEventListener('DOMContentLoaded', () => {
    // On cible votre formulaire avec son identifiant exact
    const formulaire = document.getElementById('regForm');

    if (formulaire) {
        formulaire.addEventListener('submit', async (event) => {
            event.preventDefault(); // Bloque le rechargement de la page et l'envoi vers 127.0.0

            // Vérification de la correspondance des mots de passe avant l'envoi
            const motdepasse = document.getElementById('motdepasse').value;
            const confirmation = document.getElementById('confirmation').value;

            if (motdepasse !== confirmation) {
                alert("Erreur : Les mots de passe ne correspondent pas.");
                return;
            }

            // On rassemble TOUTES les données de votre formulaire
            const donneesFormulaire = {
                prenom: document.getElementById('prenom').value,
                nom: document.getElementById('nom').value,
                email: document.getElementById('email').value,
                entreprise: document.getElementById('entreprise').value,
                poste: document.getElementById('poste').value,
                taille: document.getElementById('taille').value,
                motdepasse: motdepasse // Optionnel : à crypter idéalement côté backend
            };

            try {
                // Envoi à votre API de production sur Azure App Service
                const reponse = await fetch('https://api.api-sql-formulaire-b5dsdjf0cxd0bhby.westus3-01.azurewebsites.net/soumettre-formulaire', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(donneesFormulaire)
                });

                const resultat = await reponse.json();

                if (reponse.ok) {
                    alert("Succès : " + resultat.message);
                    formulaire.reset(); // Vide le formulaire
                } else {
                    alert("Erreur du serveur : " + resultat.message);
                }

            } catch (erreur) {
                console.error("Erreur réseau :", erreur);
                alert("Impossible de joindre le serveur d'API Azure.");
            }
        });
    }
});
