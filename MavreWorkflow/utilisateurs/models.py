from django.contrib.auth.models import User,Group,Permission
from django.db import models
from django.urls import reverse

# Create your models here.
class DomaineDetude(models.Model):
    #--  --#
    """
        -- Cette classe répresente la table des domaines d'études
        -- De l'application utilisateur
    """
    # I'm still doubting about this class
class UsagerProfil :
    #--  --#
    """
        -- Cette classe UsagerProfil represente la table des profils utilisateurs
        -- L'application utilisateur
    """

    account = models.OneToOneField(User, on_delete=models.CASCADE)

    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    permission = models.OneToOneField(Permission, on_delete=models.CASCADE)

    # -- mise en place des attributs de la classe modèle Utilisateur profil -- #
    domaineEtudeUtilisateur = models.ForeignKey(DomaineDetude, null=True, on_delete=models.SET_NULL)
    dateCreationProfil = models.DateTimeField(auto_now=True, null=False)

    # -- mise en place de la méthode __str__ -- #
    def __str__(self):
        return f"Nom utilisateur : {self.account.username}"

class Commandes : 
    # -- docstring de la classe modèle Commandes -- #
    """
        -- Cette classe Commandes représente la table des commandes des assurés
        -- De l'application utilisateur 
    """

    # -- mise en place des attributs de la classe modèle Commandes -- #
    libelle_commande = models.TextField(null = True, max_length= 100)
    date_commande = models.DamteTimeField(auto_now=True, null=False)
    dateReception_commande = models.DateFieldTimeFiels(auto_now=True, null=False)

    # -- mise en place de la méthode __str__ -- #
    def __str__(self):
        return f"date_commande : {self.date_commande}"
class CommandesUsager(models.Model):
    # -- docstring de la classe CommandesUsager -- #
    """
        -- Cette classe CommandesUsager représente la tabble CommandesUsager --
        -- De l'application utilisateur 
    """

    numero_commande = models.ForeignKey(Commandes, on_delete=models.CASCADE)

    id_usager = models.ForeignKey(UsagerProfil, on_delete=models.CASCADE)

    qte_commandes_par_pair = models.TextField(max_length=50, null=True,)

class Medicament : 
    # -- docstring de la classe modèle Medicaments -- #
    """
        -- Cette classe Medicament représente la table des médicaments de la pharmacie
        -- De l'application utilisateur
    """

    # -- mise en place des attrinuts de la classe modèle Medicament -- #
    libelle_medicament = models.CharField(max_length=150, null=False)
    quantite_medicament = models.BigIntegerField(null=False)
    prix_medicament = models.BigIntegerField(null=False)
    Image_medicament = models.ImageField(null=False)

    # -- mise en place de la place de la méthode __str__ -- #
    def __str__(self):
        return f"image_medicament : {self.image_medicament}"
    
    # -- mise en place de la méthode get_absolute_url
    def get_absolute_url(self):
        return reverse("afficher_medicament", args=[str(self.id)])
    
class CommandesMedicaments : 
    # -- docstring de la classe modèle CommandesMédicaments -- #
    """
        -- Cette classe représente la tables CommandesMédicaments et
        -- est née de la relation de la classe Commandes et Médicaments
        
    """ 
    numero_commandes = models.ForeignKey(Commandes, on_delete=models.CASCADE)
    numero_medicaments = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    qte_commander = models.BigIntegerField(null=False)

    # -- mise en place de la méthode __str__ -- #
    def __str__(self):
        return f"qte_commander : {self.qte_commander}"

class Souche : 
    # -- docstring de la classe modèle Souche -- #
    """
        -- Cette classe représente la table Souche 
        -- Il s'agit du papier qui rends possible la commande
        -- D'un assuré
    """ 
    #
    id_usager = models.ForeignKey(UsagerProfil, on_delete= models.CASCADE)
    #date_envoie = models.DateTimeField(auto_now=True, null = False)
    image_souche = models.ImageField(null=False)

    # -- mise en place de la méthode __str__ -- #
    def __str__(self):
        return f"image_souche : {self.image_souche}"
class Livraisons : 
    # -- docstring de la classe modèle Livraisons -- #
    """
        -- Cette classe représente la table Livraisons
    """

    # mise en place des attributs de la classe modèle Livraisons
    libelle_livraison = models.TextField(max_length=100, null=True)
    date_livraison = models.DateField(auto_now_add=True, null=False)

    # -- définition de la méthode __str__ -- #
    def __str__(self):
        return f"date_livraisons : {self.date_livraison}"

class Vendeur(models.Model):
    # -- docstring de la classe modèle Vendeur -- #
    """
        -- Cette classe représente la table Vendeur
    """
    id_usager = models.ForeignKey(UsagerProfil, on_delete= models.CASCADE)

    # -- mise en place des attributs de la classe modèle Vendeur -- #
    nom_Vendeur = models.TextField(max_length=150, null=False)
    prenom_Vendeur = models.TextField(max_length=150, null=False)
    adresse_Vendeur = models.TextField(max_length=150, null=False)
    datenaiss_Vendeur = models.DateField(null=True)
    telephone_Vendeur = models.IntegerField(null=False)

    # -- mise en place de la méthode __str__ --  #
    def __str__(self):
        return f"Nom vendeur : {self.nom_Vendeur}"
    
class Livreur(models.Model) :
    # -- docstring de la classe Livreur -- #
    """
        -- Cette classe répresente la table livreur
    """

    code_vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE)

    # -- mise en place de la méthode __str__ -- #
    def __str__(self):
        return f"Code vendeur : {self.code_vendeur}"
class CampagnieAssurance :                                              
    # -- docstring de la classe modèle CampagnieAssurance -- #
    """
        -- Cette classe répresente la table Compagnie Assurance
    """

    # -- mise en place des attributs de la classe modèle CompagnieAssurance -- #
    nom_compagnieAssurance = models.TextField(max_length=150, null=False)
    pourcentage = models.DecimalField(null=True)

    def __str__(self) :
        return f"Pourcentage : {self.pourcentage}"
class Societe : 
    # -- docstring de la classe modèle Societe -- #
    """
        -- Cette classe répresente la table Societé
        -- Ce sont les societes qui sont assurés auprès des compagnies d'assurance
    """
    code_campagnieAssurance = models.ForeignKey(CampagnieAssurance, on_delete= models.CASCADE)

    # -- mise en place des attributs de la classe Societe -- #
    nom_societe = models.TextField(max_length=50, null=False)

    # -- mise en place de la méthode __str__ -- #
    def __str__(self) : 
        return f"nom societé : {self.nom_societe}"

class Assure(models.Model) : 
    #-- docstring de la classe modèle Assuré --#
    """
        -- Cette classe répresente la table des assures
        -- L'application utilisateurs 
    """

    id_usager = models.ForeignKey(UsagerProfil, on_delete= models.CASCADE)
    code_societe = models.ForeignKey(Societe , on_delete=models.CASCADE)

    nom_assure = models.TextField(max_length=150, null=False)
    prenom_assure = models.TextField(max_length=150, null=False)
    adresse_assure = models.TextField(max_length=150, null=False)
    datenaiss_assure = models.DateField(null=True)
    telephone_assure = models.IntegerField(null=False)

    # -- mise en place de la méthode __str__ -- #
    def __str__(self) :
        return f"Nom assure : {self.nom_assure}"
class AyantDroit(models.Model) :
    #-- docstring de la classe modèle AyantDroit --#
    """
        -- Cette classe répresente la table ayantdroit
        -- L'application utilisateurs
    """
    id_usager = models.ForeignKey(UsagerProfil, on_delete= models.CASCADE)
    matricule_assuré = models.ForeignKey(Assure, on_delete= models.CASCADE )

    nom_ayantdroit = models.TextField(max_length=150, null=False)
    prenom_ayantdroit = models.TextField(max_length=150, null=False)
    adresse_ayantdroit = models.TextField(max_length=150, null=False)
    datenaiss_ayantdroit = models.DateField(null=True)
    telephone_ayantdroit = models.IntegerField(null=False)

    # -- mise en place de la méthode __str__ -- #
    def __str__(self) :
        return f"Nom ayant droit : {self.nom_ayantdroit}"