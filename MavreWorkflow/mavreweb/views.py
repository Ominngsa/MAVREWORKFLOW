from django.shortcuts import render
# -- importations des modules -- #
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login
from utilisateurs.models import UsagerProfil,Assure,AyantDroit, CampagnieAssurance, Commandes , CommandesMedicaments , CommandesUsager , DomaineDetude, Livraisons, Livreur,Medicament,Societe,Souche
from django.views.generic import View
from django.core.paginator import Paginator
# Create your views here.

def acceuil(request):
    # -- docstring de la vue -- #
    """
    
    """
    # -- retourne le template (index.html) -- #
    return render(request, 'index.html')
def webuser(request):
    # -- docstring de la vue -- #
    """
        -- Cette vue intiluée 'webuser' a pour but principal de 
        -- Récupérer une liste de dix (10) commandes reçus et livrés
        -- Et des domaines d'études pour les retourner au templates
        -- normalement c'est le fichier dashboard
    """

    # -- récupération de dix livraisons aléotairement -- #
    listeLivraisons = Livraisons.objects.order_by('?')[:10]

    # -- récupération de dix commandes aléatorement -- #
    listeCommandes = Commandes.objects.order_by('?')[:10]

    # -- récupération des domaines d'études -- #
    listeDomaineEtude = DomaineDetude.objects.order_by('nomDomaineEtude')

    # -- retourne le template (dashboard.html) -- #
    return render(request, 'dashboard.html', {'listeLivraisons' : listeLivraisons, 'listeCommandes': listeCommandes, 'listeDomaineEtude': listeDomaineEtude})

def aPropos(request):
    # -- docstring de la vue -- #
    """
        -- Cette vue intituliée 'aPropos' a pour but principal de
        -- Retourner simplément l'utiliteur le template d'in
        -- Formations (aPropos.html) 
    """

    # -- retourne le template (aPropos.html) -- #
    return render(request, 'aPropos.html')

def politiqueConfidentialité(request):
    # -- docstring de la vue -- #
    """
        -- Cette vue intitulée 'politiqueConfidentialité' a pour but principal de
        -- Retourner simplement à l'utilisateur le template possedant la politique de
        -- Confidentialité (politiqueConfidentialite.html) de la plateforme
    
    """
    
    # -- retourne le template (politiqueConfidentialité.html) -- #
    return render(request, 'politiqueConfidentialite.html')

def creerUnCompte(request):
    # -- docstring de la vue -- #
    """
        -- Cette vue intitulée 'creerUnCompte' a pour but principal de recuperer les
        -- Identifiants nécessaires à la création utilisateur, vérifier le
        -- Username s'il existe déjà dans la base de données puis lui retourner un 
        -- Message dans le fichier (sign-up.html)
    """

    # -- définition des sous fonctions -- #
    def verificationName(username) : 
        # -- docstring de la sous fonction -- #
        """
            -- Cette sous fonction a pour but de vérifier le nom d'un utilisateur
            -- S'il existe déja dans la bd, puis renvoie True pour vrai
            -- Ou False pour non
        """

        try:
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
            # -- aucun utilisateur trouvé -- #
            return False
        
    # -- vérification de la requête HTTP -- #
    if request.method == "POST" and 'nomFamille' in request.POST and 'prenomUtilisateur' in request.POST and 'nomUtilissateur' in request.POST and 'adresseMail' in request.POST and 'password' in request.POST:
        # -- vérification du nom -- #
        if verificationName(request.POST.get('nomUtilisateur')):
            # -- renvoi une erreur en message -- #
            messages.error(request, "Le nom d'utilisateur saisi ci-dessous existe déja ! Connectez-vous plûtot.")

            # -- retourne vers la page creerUncompte -- #
            return render(request, 'sign-up.html', {'nomUtilisateurContexteEnCasErreur' : request.POST.get('nomUtilisateur'), 'NomFamileContexteEnCasErreur': request.POST.get('nomFamille'), 'PrenomUtilisateurContexteEnCasErreur': request.POST.get('prenomUtilisateur'), 'adresseMailContexteEnCasErreur': request.POST.get('adresseMail'), 'passwordContexteEnCasErreur' : request.POST.get('password')})
        elif len(request.POST.get('password')) < 8:
            # -- renvoi une erreur en message -- #
            messages.error(request, "Le mot de passe doit obligatoirement contenir 8 caractères !")

            # -- retourne vers la page creerUnCompte -- #
            return render(request, 'sign-up.html', {'nomUtilisateurContexteEnCasErreur' : request.POST.get('nomUtilisateur'), 'NomFamilleContexteEnCasErreur': request.POST.get('nomFamille'), 'PrenomUtilisateurContexteEnCasErreur' : request.POST.get('prenomUtilisateur'), 'adresseMailContexteEnCasErreur': request.POST.get('adresseMail'), 'passwordContexteEnCasErreur' : request.POST.get('password')})
        elif request.POST.get('nomUtilisateur').lower() in request.POST.get('password').lower():
            # -- renvoi une erreur en message -- #
            messages.error(request, "Le mot de passe ne doit pas contenir le nom d'utilisateur")

            # -- retourne vers la page creerUnCompte -- #
            return render(request, 'sign-up.html', {'nomUtilisateurContextEnCasErreur' : request.POST.get('nomUtilisateur'), 'NomFamilleContexteEnCasErreur' : request.POST.get('nomFamille'),'PrenomUtilisateurContexteEnCasErreur': request.POST.get('prenomUtilisateur'), 'adresseMailContexteEnCasErreur': request.POST.get('adresseMail'), 'passwordContexteEnCasErreur' : request.POST.get('password')})
        else:
            # -- gestion d'exceptions -- #
            try:
                # -- création d'un utilisateur -- #
                usager = User.objects.create_user(username= request.POST.get('nomUtilisateur'), password=request.POST.get('password'), email=request.POST.get('adresseMail'), first_name= request.POST.get('prenomUtilisateur'), last_name = request.POST.get('nomFamille'))

                # -- sauvergarde l'utilisateur -- #
                usager.save()

                # -- création d'un profil utilisateur -- #
                profilUtilisateur = UsagerProfil(account = usager)

                 # -- sauvegarde du profil utilisateur -- #
                profilUtilisateur.save()

                # -- renvoie un message de succès -- #
                messages.success(request, "Votre compte a été créer avec succès !!")

                # -- retourne vers la page creerUncompte -- #
                return redirect('sign-in.html')
            except :
                # -- renvoi une erreur en message -- #
                messages.error(request, "Désolé une erreur est survenue ! Veuillez recommencer")

                # -- retourne vers la page creerUnCompte -- #
                return render(request, 'sign-up.html', {'nomUtilisateurContexteEnCasErreur' : request.POST.get('nomUtilisateur'), 'NomFamilleContexteEnCasErreur' : request.POST.get('nomFamille'), 'PrenomUtilisateurContexteEnCasErreur' : request.POST.get('prenomUtilisateur'), 'adresseMailContexteEnCasErreur' : request.POST.get('adresseMail'), 'passwordContexteEnCasErreur' : request.POST.get('password')})
        
# -- retourne le template
    return render(request,'sign-up.html')
            

class Connexion(View):
    # -- docstring de la vue -- #
    """
        -- Cette vue intitulé 'Connexion' a pour but de principal de recuperer
        -- L'username et le password d'un utilisateur, de les comparer à un
        -- Tuple présent dans la base de données, puis retourner un status
        -- Tout en utilisant la méthode de transition de données Ajax  
    """

    # -- mise en place des sous fonctions -- #
    def get(self, request):
        # -- docstring de la sous fonction -- #
        """
            -- Cette sous fonction a pour but de recuperer les identifiants 
            -- Passés par la methode GET avec ajax
        """

        # -- vérification de la methode -- #
        if request.method == "GET" and 'nomUtilisateur' in request.GET and 'password' in request.GET:
            # -- authentification de l'utilisateur -- #
            user = authenticate(request, username = request.GET.get('nomUtilisateur'), password = request.GET.get('password'))

            # -- vérification de l'utilisateur -- #
            if user is not None:
                # -- authentifie l'utilisateur -- #
                login(request, user)
                
                # -- redirection vers utilisateur -- #
                return JsonResponse({'message' : True}, status = 200)
            else:
                # -- retourne un false -- #
                return JsonResponse({'message' : False}, status = 200)
        
        # -- retourne une erreur -- #
        raise Http404
    
def formLogin(request) :
    # -- docstring de la vue -- #
    """
    
    """
    return render(request,'sign-in.html')