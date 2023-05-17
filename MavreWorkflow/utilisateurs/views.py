from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.api import error
from django.db.models.query_utils import Q
from django.http.response import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import UsagerProfil
from django.contrib.auth import logout
from django.views.generic import View
from django.core.paginator import Paginator

# Create your views here.

# -- définition des vues de l'application -- #

def acceuilConnexion(request):
    # -- Docstring de la vue -- #
    """
        -- Cette vue intitulée 'acceuilConnexion' a pour but principal de
        -- Retourner la page principale du site
    """

    #-- retourne le template (connexion_page.html) -- #
    return render(request, 'connexion_page.html')
def loginUtilisateur(request) :
    # -- docstring de la vue --#
    """
        -- Cette vue répresente le point d'entrer de l'application utilisateur
    """
    # -- vérification de la connexion utilisateur -- #
    if request.user.is_authenticated:
        # -- gestion des erreurs -- #
        try: 
            # -- récupération de l'identifiant de l'utilisateur  -- #
            identifiantUtilisateur = request.user.id 

            # récupération des informations utilisateur -- #
            username = get_object_or_404(User, pk= identifiantUtilisateur)
            profil = get_object_or_404(UsagerProfil,account=identifiantUtilisateur)

            # -- mise en place du contexte -- #
            contexte = {"username": username, "profil": profil}

            # -- retourne le template -- #
            return render(request, 'connexion_page.html',contexte)
        except:
            #-- retourne une erreur 404 --#
            raise Http404
    else : 
        raise Http404