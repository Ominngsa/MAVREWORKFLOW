from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from utilisateurs.models import Assure,AyantDroit,CampagnieAssurance,Commandes,CommandesMedicaments,CommandesUsager,Livraisons,Medicament

def create_groups_and_permissions():
    # Création des groupes
    preparateurs_group, _ = Group.objects.get_or_create(name='preparateurs')
    vendeurs_group, _ = Group.objects.get_or_create(name='vendeurs')
    assures_group, _ = Group.objects.get_or_create(name='assures')
    ayantdroit_group, _ = Group.objects.get_or_create(name='ayantDroit')
    utilisateurs_lambda_group, _ = Group.objects.get_or_create(name='utilisateurs_lambda')

    # Attribution des permissions aux groupes
    #  pour le modèle Commandes
    content_type_commande = ContentType.objects.get(app_label='utilisateurs', model='Commandes')

    # Permissions pour ajouter, modifier, supprimer et afficher des commandes
    permission_add_commande = Permission.objects.get(content_type=content_type_commande, codename='add_commande')
    permission_change_commande = Permission.objects.get(content_type=content_type_commande, codename='change_commande')
    permission_delete_commande = Permission.objects.get(content_type=content_type_commande, codename='delete_commande')
    permission_view_commande = Permission.objects.get(context_type=content_type_commande, codename='view_commande')

    preparateurs_group.permissions.add(permission_add_commande, permission_change_commande, permission_delete_commande,permission_view_commande,permission_view_commande)

    vendeurs_group.permissions.add(permission_view_commande)

    assures_group.permissions.add(permission_add_commande,permission_change_commande,permission_delete_commande)

    ayantdroit_group.permissions.add(permission_add_commande,permission_change_commande,permission_delete_commande)

    #  pour le modèle Assure
    content_type_assure = ContentType.objects.get(app_label='utilisateurs', model='Assure')

    # Permissions pour ajouter, modifier,supprimer et afficher des assurés
    permission_add_assure = Permission.objects.get(content_type=content_type_assure, codename='add_commande')
    permission_change_assure = Permission.objects.get(content_type=content_type_assure, codename='change_commande')
    permission_delete_assure = Permission.objects.get(content_type=content_type_assure, codename='delete_commande')
    permission_view_assure = Permission.objects.get(content_type=content_type_assure,codename='view_commande' )

    preparateurs_group.permissions.add(permission_add_commande, permission_change_commande, permission_delete_commande)

def authenticate_assure(matricule_salarie):
    try:
        assure = Assure.objects.get(matricule_salarie=matricule_salarie)
        return assure
    except Assure.DoesNotExist:
        return None

def has_permission(user, permission_codename):
    return user.has_perm(permission_codename)