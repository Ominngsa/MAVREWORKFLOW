/* --
  -- Nom du fichier : fonctions.js
  -- Nom du redacteur : Franck Souverain MAZIKOU
  -- Date de redaction : 31/08/2021
-- */

/* Modification de la largeur de l'element mySidenav à 250px */
function openNav() {

    document.getElementById("mySidenav").style.width = "250px";

}
/* -- -- */

/* Modification de la largeur de l'element mySidenav à 0px */
function closeNav() {

    document.getElementById("mySidenav").style.width = "0";

}
/* -- -- */

/* -- Affichage du formulaire des petits ecrans -- */
function openFormulairePetitsEcran() {

    document.getElementById("formulaire-petits-ecrans").style.display = "flex";

}
/* -- -- */

/* -- Affichage de l'année en cours -- */
function getAnneeEnCours() {
    /* -- Création d'une instance date -- */
    var newDate = new Date();

    /* -- affichage de l'année en cours -- */
    document.write(newDate.getFullYear());
}
/* -- -- */

/* -- Pour les onglets -- */
function affichageOnglet(nameOnglet) {
    /* -- Déclaration des variables -- */
    var i, tabcontent;

    /* -- Recuperation des elements dont la classe est bloc-contenu-onglet -- */
    tabcontent = document.getElementsByClassName("bloc-contenu-onglet");

    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    /* -- Affichage -- */
    document.getElementById(nameOnglet).style.display = "block";
}
/* -- -- */

/* -- Mise en place de la fonction de telechargement d'un document -- */
function telechargerUnDocument(urlDuDocument, nomDuDocument) {
    fetch(urlDuDocument).then(async(res) => {
        const dfile = await res.blob();
        var blocUrl =
            window.URL && window.URL.createObjectURL ?
            window.URL.createObjectURL(dfile) :
            window.webkitURL.createObjectURL(dfile);

        var templLink = document.createElement("a")
        templLink.style.display = "none";
        templLink.href = blocUrl;
        templLink.setAttribute("download", nomDuDocument + "_by_kakou");

        if (typeof templLink.download === "undefined") {
            templLink.setAttribute("target", "_blank");
        }

        document.body.appendChild(templLink);
        templLink.click();

        setTimeout(function() {
            document.body.removeChild(templLink);
            window.URL.revokeObjectURL(blocUrl);
        }, 200);

        /* -- affichage du message de succès -- */
        document.getElementById('notification').className = "alert-succes";
        document.getElementById('notification').innerText = "Téléchargement du document effectuer avec succès";

        /* -- appel de la fonction pour afficher la notification -- */
        afficherNotification();
    });
}
/* -- -- */

/* -- pour les notifications -- */
function afficherNotification() {
    // -- déclaration de constante -- //
    const toast = document.querySelector('#notification');

    // -- affichage de la notification -- //
    toast.classList.add("show");
    setTimeout(() => {
        toast.classList.remove("show");
    }, 2000);
}
/* -- -- */