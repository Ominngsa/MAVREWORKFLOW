

function connexionUtilisateur() {
    /* -- vérification du  contenu -- */
    if (document.getElementById('nomUtilisateur').value.length > 0 && document.getElementById('motDePasse').value.length > 0) {
        /* -- déclaration de la liste d'identifiants -- */
        listeIdentifiants = { 'nomUtilisateur': document.getElementById('nomUtilisateur').value, 'password': document.getElementById('motDePasse').value }

        /* -- mise en place de la methode ajax -- */
        $.ajax({
            method: "GET",
            url: "/connexion",
            data: listeIdentifiants,
            async: true,
            success: function(response) {

                /* -- vérification du message -- */
                if (response.message) {
                    /* -- redirection vers la page d'accueil utilisateur -- */
                    window.location.href = '/utilisateur/'
                } else {
                    /* -- affichage du message d'erreur -- */
                    document.getElementById('blocMessageConnexion').style.display = 'block';
                    document.getElementById('messageConnexion').innerText = "Le nom utilisateur ou le mot de passe saisi est invalide !!";
                }
            },
            error: function(error) {
                /* -- affichage du message d'erreur -- */
                document.getElementById('blocMessageConnexion').style.display = 'block';
                document.getElementById('messageConnexion').innerText = "Une erreur est survenue lors de la connexion !!";
            }
        });
    }
}