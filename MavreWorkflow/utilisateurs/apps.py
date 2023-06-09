from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission,Group
from django.contrib.contenttypes.models import ContentType
from utilisateurs.models import Commandes 
class UtilisateursConfig(AppConfig):
    name = 'utilisateurs'

    # def ready(self):
    #     post_migrate.connect(self.on_post_migrate, sender=self)

    # def on_post_migrate(self, **kwargs):
    #     # Création des groupes 
    #     preparateurs_group = Group.objects.get_or_create(name='preparateurs')
    #     vendeurs_group = Group.objects.get_or_create(name='vendeurs')
    #     assures_group = Group.objects.get_or_create(name='assures')
    #     utilisateurs_lambda_group = Group.objects.get_or_create(name='utilisateurs_lambda')

    #     # -- Attribution des permissions aux groupes -- #
    #     content_type_commande, created = ContentType.objects.get_or_create(app_label='utilisateurs', model='Commandes')

    #     permission_add_commande = Permission.objects.get(content_type=content_type_commande, codename='add_commande')
    #     permission_change_commande = Permission.objects.get(content_type=content_type_commande, codename='change_commande')
    #     permission_delete_commande = Permission.objects.get(content_type=content_type_commande, codename='delete_commande')

    #     preparateurs_group.Permissions.add(permission_add_commande, permission_change_commande, permission_delete_commande)