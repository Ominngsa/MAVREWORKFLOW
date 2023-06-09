from django.contrib import messages
from django.contrib.auth.models import User,Group 
from django.contrib.messages.api import error
from django.db.models.query_utils import Q
from django.http.response import Http404, JsonResponse
from django.shortcuts import * 
from .models import UsagerProfil, CampagnieAssurance, Commandes, CommandesMedicaments, Livraisons, Medicament,Assure,AyantDroit,DomaineDetude, Visualiser, Souche,Group
from django.contrib.auth import logout
from django.views.generic import *
from django.core.paginator import  *
from django.contrib.auth.decorators import *  
from utilisateurs.forms import *


# Create your views here.

# -- définition des vues de l'application -- #
# Utilisation des fonctions d'authentification
# def my_view(request):
#     # Création des groupes et des permissions (si nécessaire)
#     create_groups_and_permissions()

#     # Authentification d'un assure
#     assure = authenticate_assure(matricule_salarie='12345')
#     if assure:
#         # Vérification des permissions
#         if has_permission(user=request.user, permission_codename='change_commande'):
#             # L'utilisateur a la permission de modifier les commandes
#             # Faites quelque chose ici
#             pass
#         else:
#             # L'utilisateur n'a pas la permission de modifier les commandes
#             # Faites autre chose ici
#             pass
#     else:
#         # L'assuré n'existe pas
#         # Faites quelque chose ici
#         pass
# @login_required
# def liste_commandes(request):
#     commandes = Commandes.objects.all()
#     return render(request,'liste_commandes.html', {'commandes' : commandes})

# @login_required
# @permission_required('utilisateurs.add_commande', raise_exception=True)
# def ajouter_commande(request) : 
#     if request.method == 'POST':
#         # -- Traiter les données du formulaire d'ajout de commande
#         # ...
#         return redirect('liste_commandes')
#     else:
#         return render(request,'ajouter_commande.html')
    
def ajouter_assure(request):
    if request.method == 'POST':
        form = AssureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_assures')
    else:
        form = AssureForm()
    return render(request, 'ajouter_assure.html', {'form': form})
def acceuilUtilisateur(request) :
    # -- docstring de la vue -- #
    """
        -- Cette vue répresente le point d'entrer après que l'utilisateur se soit connecté
        -- pour la partie web
    """
    # -- vérification de la connexion utilisateur -- #
    if request.user.is_authenticated:
        # -- gestion des erreurs -- #
        try : 
            # -- récupération fr l'identifiant de l'utilisateur -- #
            identifiantUsager = request.user.id

            # -- récuérations des informations utilisateur -- #
            username = get_object_or_404(User, pk = identifiantUsager)
            profil = get_object_or_404(UsagerProfil, account = identifiantUsager)

            # -- récupération des dix dernières commandes par ordre décroissante -- #
            listeCommandes = Commandes.objects.order_by('ASC')[:10]

            # -- récupération des dix dernières livraisons -- #
            listeLivraisons = Livraisons.objeccts.order_by('ASC')[:10]

            # -- mise en place du contexte -- # 
            contexte = {" username " : username , "profil" : profil, "listesCommandes" : listeCommandes , "listeLivraisons" : listeLivraisons}

            # -- retourne le template -- # 
            return render(request,'LeFichierATrouver' , contexte)
        except :
            # -- retourne une erreur 404 -- #
            raise Http404
    else : 
        # -- retourne une erreur 404 -- #
        raise Http404
def deconnexion(request) : 
    # -- docstring de la vue -- #
    """
        -- Cette vue représente le chemin de déconnexion de l'utilisateur
    """

    # -- vérification de la connexion Usager -- #
    if request.user.is_authenticated:
        # -- suppression de la session -- #
        logout(request)

        # -- retourne vers la page d'accueil internaute -- #
        return redirect('/')
    else :
        # -- retourne une erreur 404 -- #
        raise Http404

def modificationCompte(request) : 
    # -- docstring de la vue -- #
    """
        -- Cette vue permet de modifier le compte d'un Usager
    """
    def getInformationUsager(identifiantUsager):
        # -- docstring de la vue -- #
        """
            -- Cette méthode permet de récupérer les identifiants
            -- D'un utilisatuer
        """

        # -- récupération des informations utilisateur -- #
        username = get_object_or_404(User, pk = identifiantUsager)
        profil = get_object_or_404(UsagerProfil, account = identifiantUsager)

        # -- mise en place du contexte -- # 
        context =  {" username " : username , "profil" : profil}

        # -- retourne le contexte -- #
        return context

    def verificationName(username, nomUsagerCourant):
        # -- docstring de la vue -- #
        """
            -- Cette méthode a pour but de vérifier le nom d'un utilisateur
        """

        try:
            # -- vérificztion de username -- #
            if username.lower() == nomUsagerCourant.lower():
                # -- retourne Faux (False) -- #
                return False
            else :
                # -- tentative de récupération d'un utilisateur du même nom -- #
                usager = User.objects.get(username = username)

                # -- vérification du nom -- #
                if usager.username.lower() == username.lower():
                # -- retourne vrai (True) -- #
                    return True
                else :
                    # -- retourne Faux (False) -- #
                    return False
        except : 
            # -- retourne Faux (False) -- #
            return False
    
        # -- vérification de la connexion usager -- #
    if request.user.is_authenticated and request.method == "POST" and 'nomUsager' in request.POST and 'domaineEtude' in request.POST and 'numeroTelephone' in request.POST and 'password' in request.POST :
        # -- docstring du numéro de téléphone -- #
        if verificationName(request.POST.get('nomUsager'), request.user.username) :
            # -- renvoie une erreur en message -- #
            messages.error(request, "Le nom d'usager saisi ci-dessous existe déjà pour un usager")

            # -- mise en place du contexte -- #
            contexte = getInformationUsager(request.user.id)

            # -- mise à jour du contexte -- #
            contexte.update({'nomUsagerEnCasErreur' : request.POST.get('nomUsager'),'numeroEnCasErreur' : request.POST.get('numeroTelephone'), 'PasswordEnCasErreur' : request.POST.get('password')})

            # -- retourne le template de modification d'Usager (modifier_compte_usager.html)
            # -- IL FAUT LA TROUVER -- #
            return render(request, ' #lefichier# ' , contexte)
        elif len(request.POST.get('password')) : 
            # -- renvoie une erreur en message -- #
            messages.error(request, "Le mot de passe doit contenir huit caractères !")

            # -- mise en place du contexte -- #
            contexte = getInformationUsager(request.user.id)

            # -- mise à jour du contexte -- #
            contexte.update({'nomUsagerEnCasErreur' : request.POST.get('nomUsager'),'numeroEnCasErreur' : request.POST.get('numeroTelephone'), 'PasswordEnCasErreur' : request.POST.get('password')})

            # -- retourne le template (modifier_compte_usager.html) -- #
            return render(request, ' #lefichier# ', contexte)
        else :
            # -- gestion des erreurs -- #
            try :
                # -- mise en place de la liste de données -- #
                liste_donnees = [request.POST.get('nomUsager'), request.POST.get('numeroTelephone'), request.POST.get('password')]

                # -- récupération des informations utilisateurs -- #
                usager = get_object_or_404(User, pk = request.user.id)
                profil = get_object_or_404(UsagerProfil, account=request.user)

                # -- gestion des exceptions -- #
                try :
                    # -- mise en place du contexte -- #
                    contexte = getInformationUsager(request.user.id)

                    # -- mise à jour du contexte -- #
                    contexte.update({'nomUsagerEnCasErreur' : request.POST.get('nomUsager'),'numeroEnCasErreur' : request.POST.get('numeroTelephone'), 'PasswordEnCasErreur' : request.POST.get('password')})

                    # -- retourne le template (modifier_compte_usager.html)
                    return render(request, '#trouver le fichier', contexte)
                except :
                    # -- ne rien faire -- #
                    pass

                # -- modification de l'utilisateur -- #
                usager.username = liste_donnees[0]
                usager.set_password(liste_donnees[3])
                usager.email = liste_donnees[2]

                # -- modification du profil -- # 
                # profil.domaineEtudeUsager = get_object_or_404(DomaineEtude, nomDomaineEtude = liste_donnees[1])

                # -- sauvegarde de l'usager et du profil
                usager.save()
                #profil.save()

                # -- renvoie un message de succès -- #
                messages.success(request, "Votre compte a éte modifié avec succès !!")

                # -- retourne le template (connexion_usager.html) -- #
                return render(request, ' #trouverLeFichier#  ', getInformationUsager(request.user.id))
            except :
                # -- rencoi une erreur en message -- #
                messages.error(request, "Une erreur s'est produite ! Votre compte n'a pas été modifier.")

                # -- mise en place du contexte -- #
                contexte = getInformationUsager(request.user.id)

                # -- mise à jour du contexte -- #
                contexte.update({'nomUsagerEnCasErreur' : request.POST.get('nomUsager'),'numeroEnCasErreur' : request.POST.get('numeroTelephone'), 'PasswordEnCasErreur' : request.POST.get('password')})

                # --retourne le template (modifier_compte_usager.html)
                return render(request , contexte )
    elif request.user.is_authenticated:

        # -- retourne le template (modifier_compte_usager.html) -- #
        return render(request, ' #TrouverLeFichier# ', getInformationUsager(request.user.id))
    else:
        # -- retourne une erreur 404 -- #
        raise Http404
def suppressionCompte(request) : 
    # -- docstring de la vue -- #
    """
        -- Cette vue a pour but de supprimer un compte d'un utilisateur
    """ 

    # -- définition des sous fonctions -- #
    def getInformationsUsager(identifiantUsager):
        # -- docstrinf de la sous fonction -- #
        """
            -- Cette sous fonction a pour but de récupérer les identifiants
            -- D'un usager
        """ 

        # -- récupération des informations usagers -- #
        usager = get_object_or_404(User, pk= identifiantUsager) 
        profil = get_object_or_404(UsagerProfil, account = identifiantUsager)

        # -- mise en place du contexte -- #
        context = {"usager" : usager , "profil": profil}      

        # -- retourne le contexte -- #
        return context
    # -- vérification de la connexion de l'usager -- #   
    if request.user.is_autenticated : 
        # -- récupération des informations avant suppression -- #
        contexte = getInformationsUsager(request.user.id)

        # -- gestion des erreurs -- #
        try : 
            # -- récupération de l'usager courant et de son profil -- #
            usager = get_object_or_404(User, pk = request.user.id)
            profil = get_object_or_404(UsagerProfil, account = request.user.id)

            # supression de l'utilisateur et de son profil --  #
            usager.delete()
            profil.delete()

            # -- renvoi un message de succès -- #
            messages.success(request, "Votre compte a été supprimer avec succès !!")

            # -- retourne le template (modifierCompteUtilisateur.html) -- #
            return render(request, '#TrouverLeFichier#', contexte)
        except :
            # -- renvoie une erreur en message -- #
            messages.error(request, "Désolé un problème est survenue ! Votre compte n'a pas été supprimer !")

            # -- retourne le template(modifierCompte) --  #
            return render(request, '#TrouverLeFichier#', contexte)
        else:
            # -- retourne une erreur 404 -- #
            raise Http404
def commandesRecus(request) :
    # -- docstring de la vue -- #
    """
        -- Cette vue permet de rediriger l'utilisateurs vers le tableau avec les commandes reçus
    """        
    # -- vérification de la connexion utilisateur -- #
    if request.user.is_authenticated:
        # -- récupération de  l'udentifiant de l'utilisateur -- #
        identifiantUsager = request.user.id

        # -- récupération des informations usager -- #
        usager = get_object_or_404(User, pk= identifiantUsager)
        profil = get_object_or_404(UsagerProfil, account= identifiantUsager)

        # -- récupération des commandes validés -- #
        listeCommandesRecus = Commandes.objects.order_by('-date_commande').filter(idUsager = profil)

        # -- mise en place du contexte -- #
        context = {"usager" : usager , "profil" : profil , 'listeCommandesRecus' : listeCommandesRecus}

        # -- retourne le template (commandesRecus.html) -- #
        return render(request, 'commandesRecus.html', context)
    else : 
        # -- retourne une erreur 404 -- #
        raise Http404
def rechercheFormUsager(request) :
    # -- docstring de la vue -- #
    """
        -- Cette vue permet de rédiriger le vendeur vers le template
        -- Pour rechercher
    """

    # -- vérification de la connexion utilisateur -- #
    if request.user.is_authenticated and request.method == "GET" and 'recherche' in request.GET :
        # -- recuperation de la valeur -- #
        recherche = request.GET.get('recherche')

        # -- récupération de l'identifiant de l'utilisateur -- #
        identifiantUsager = request.user.id

        # -- récupération de l'identifiant de l'usager -- #
        usager = get_object_or_404(User, pk= identifiantUsager)
        profil = get_object_or_404(UsagerProfil, account = identifiantUsager)

        # -- faire une rechercher sur le mot clé -- #
        listeAssuresRecherche = Assure.objects.order_by('-nom_assure').filter(Q(nomAssure_icontains=recherche) | Q(prenomAssure_icontains=recherche))[:4]
        listeAyantDroitRecherhce = AyantDroit.objects.order_by('-nom_ayantDroit').filter(Q(nomAyantDroit_icontains=recherche) | Q(domaineEtudeAyantDroit_nomDomaineEtude_icontains = recherche))[:4]

        # -- récupération de dix assurés et dix ayantDroits -- #
        listeAssures = Assure.objects.order_by('?')[:10]
        listeAyantDroit = AyantDroit.objects.order_by('?')[:10]

        # -- récupération des domaines d'études -- #
        listeDomaineEtude = DomaineDetude.objects.order_by('nomDomaineEtude')

        context = {"usager" : usager , "profil": profil , 'listeAssures' : listeAssures, 'listeAyantDroit' : listeAyantDroit, 'dictElementTwo' : {'listeAssureRecherche' : listeAssuresRecherche, 'listeAyantDroitRecherche' : listeAyantDroitRecherhce}, 'listeDomaineEtude' : listeDomaineEtude}

        # -- retourne le template -- #
        return render(request, 'TrouverLeFichier',context)
    else:
        # -- retourne une erreur 404 -- #
        raise Http404
def rechercheUsager(request, motCle):
    # -- docstring de la vue -- #
    """

    """

    # -- vérification de la connexion usager -- #
    if request.user.is_authenticated : 
        # -- récupération de l'identifiant de l'usager -- #
        identifiantUsager = request.user.id

        # -- récupération des informations usager -- #
        usager = get_object_or_404(User, pk= identifiantUsager)
        profil = get_object_or_404(UsagerProfil, account= identifiantUsager)

        # -- vérification du mot clé -- #
        if motCle == "assures" : 
            # -- faire une recherche sur le mot clé assure (avec la classe modèle Assures) -- #
            listeElement = Assure.objects.order_by('-nom_assure')

            # -- création de la pagination -- #
            paginationAssure = Paginator(listeElement, 3)
            nombrePage = request.GET.get('page')
            objectPage = paginationAssure.get_page(nombrePage)
        elif motCle == "ayantdroit":
            # -- faire une recherche sur le mot clé ayantdroit (avec la classe modèle AyantDroit)
            listeElement = AyantDroit.objects.order_by('-nom_ayantDroit')

            # -- création de la pagination -- #
            paginationAyantDroit = Paginator(listeElement,3)
            nombrePage = request.GET.get('page')
            objectPage = paginationAyantDroit.get_page(nombrePage)
        else : 
            # -- faire une recherche sur le mot clé (avec la classe modèle) -- #
            listeElement = UsagerProfil.objects.order_by('-nom_usager')
            """
                maybe rechercher les vendeurs
            """

            # -- récupération de dix assurés et ayantDroit aléatoirement -- #
            listeAssures = Assure.objects.order_by('?')[:10]
            listeAyantDroit = AyantDroit.objects.order_by('?')[:10]

            # -- récupération des domaines d'études -- #
            listeDomaineEtude = DomaineDetude.objects.order_by('nomDomaineEtude')

            context = {"usager" : usager, "profil" : profil, "listeAssures" : listeAssures, "listeAyantDroit" : listeAyantDroit, 'listeElement' : objectPage, 'listeDomaineEtude': listeDomaineEtude}

            # -- retourne le template -- #
            return render(request, 'TrouverLeFichier', context)
    else : 
        # -- retourne une erreur 404 -- #
        raise Http404
class AjouterAssure(View): 
    # -- docstring de la vue -- #
    """
        -- Cette vue permet de créer un assure 
    """

    # -- mise en place des sous fonctions -- #
    def get(self,request):
        # -- docstring de la sous fonction -- #
        """
            -- Cette sous fonction permet de récupérer les identifiants passés par la méthode GET à travers AJAX

        """

        # -- vérification de la connexion usager -- #
        if request.user.is_authenticated :
            # -- vérification de la méthode -- #
            if request.method == "GET" and 'nom_assure' in request.GET and 'prenom_assure' in request.GET and 'adresse_assure' in request.GET and 'datenaiss_assure' in request.GET and 'telephone_assure' in request.GET :
                # -- recuperation des identifiants de l'assuré -- #
                nom_assure = request.GET.get('nom_assure')
                prenom_assure = request.GET.get('prenom_assure')
                adresse_assure = request.GET.get('adresse_assure')
                datenaiss_assure = request.GET.get('datenaiss_assure')
                telephone_assure = request.GET.get('telephone_assure')

                # -- récupération d'un profil de l'usager -- #
                profil = get_object_or_404(UsagerProfil, account = request.user.id)

                # -- création d'un assuré -- # 
                nouvelAssure = Assure(nom_assure = nom_assure, prenom_assure = prenom_assure, adresse_assure = adresse_assure, datenaiss_assure = datenaiss_assure, telephone_assure = telephone_assure, idUsager = profil)
                nouvelAssure.save()

                # -- retourne True -- #
                return JsonResponse({'messageAssure' : True}, statuts = 200)
            else:
                # -- retourne un False -- #
                return JsonResponse({'messageAssure' : False}, statuts = 200)
        else : 
            # -- retourne une erreur -- #
            raise Http404
    def afficherCommandeUsager(request,numeroCommande) : 
        # -- docstring de la vue -- #
        """
            -- Cette vue a pour but de rediriger l'usager vers le template afficherCommandeUsager
        """

        # -- vérification de la connexion usager -- #
        if request.user.is_authenticated :
            # -- vérification de l'identifiant de l'usager -- #
            identifiantUsager = request.user.id

            # -- récupération des informations usager -- #
            usager = get_object_or_404(User, pk = identifiantUsager)
            profil = get_object_or_404(UsagerProfil, account = identifiantUsager)

            # -- récupération des informations de la commande -- #
            commande = get_object_or_404(Commandes,pk=numeroCommande)

            # -- récupération des informations de la commandesMedicaments -- #
            commandesMedicament = get_object_or_404(CommandesMedicaments, pk=commandesMedicament)

            # -- I THINK JE DOIS ASSOCIER LA TABLE Commandes*IFORGOT*

            # -- création de la pagination -- #
            paginationCommande = Paginator(commande,2)
            nombrePage = request.GET.get('page')
            objectPage = paginationCommande.get_page(nombrePage)

            # -- mise en place du contexte -- #
            context = {"usager" : usager, "profil": profil, 'commandes' : commande, 'commandesMedicaments' : commandesMedicament, 'pagination' : objectPage}

            # -- retourne le template (afficherCommande.html) -- #
            return render(request, 'TrouverLeFichier', context)
        else : 
            # -- retourne une erreur 404 -- #
            raise Http404
class visualisationSouche(View):
    # -- docstring de la vue -- #
    """
        -- Cette vue permet de mentionner la lecture d'un souche
    """
    # -- mise en place des sous fonctions -- #
    def get(self, request) : 
        # -- docstring de la sous fonction -- #
        """
            -- Cette sous fonction a pour but de récupérer les identifiants passés par la méthode GET avec ajax
        """

        # -- définition des sous fonctions -- #
        def verificationVisualisationSouche(identifiantUsager, codeSouche):
            # -- docstring de la sous fonction -- #
            """
                -- Cette sous fonction a pour but de vérifier la visualisation d'une souche
            """

            try:
                # -- tentative de récupération -- #
                visuelSouche = Visualiser.objects.get(idUsager = identifiantUsager, code_souche = codeSouche)
                # -- vérifications des identifiiants -- #
                if visualisationSouche.idUsager == identifiantUsager and visuelSouche.code_souche == codeSouche : 
                    # -- retourne vrai (True) -- #
                    return True
                else : 
                    # -- retourne Faux (False) -- #
                    return False
            except : 
                # -- retourne Faux (False) -- #
                return False
            
        # -- vérification de la connexion usager -- #
        if request.user.is_authenticated:
            # -- vérification de la methode -- #
            if request.method == "GET" and 'code_souche' in request.GET:
                # -- récupération des identifiants -- #
                code_souche = request.GET.get('code_souche')

                # -- récupération du profil de l'utilisateur et de la souche -- #
                profil = get_object_or_404(UsagerProfil, account = request.user.id)
                souche = get_object_or_404(Souche, pk= code_souche)

                # -- vérification d'une visualisation -- #
                if verificationVisualisationSouche(profil, souche):
                    # -- retourne Trouvée -- #
                    return JsonResponse({'message': 'Troouvée'}, statuts = 200)
                else : 
                    # -- création d'une visualisation -- #
                    nouvelleVisualisation = Visualiser(idUsager = profil, code_souche = souche)
                    nouvelleVisualisation.save()

                    # -- retourne True -- #
                    return JsonResponse({'message' : True}, status = 200)
            else :
                # -- retourne un false -- #
                return JsonResponse({'message' : False}, statuts=200)
        else : 
            # -- retourne une erreur -- #
            raise Http404
        

def nouvelleSouche(request,idUsager):
        # -- docstring de la vue -- #
        """
            -- Cette vue a pour but de créer une nouvelle souche
        """
        def verificationIdUsager(identifiantUsager):
            # -- docstring de la fonction -- #
            """
                -- Cette sous fonction 
            """