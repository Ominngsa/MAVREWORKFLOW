from django import forms
from utilisateurs.models import Assure, AyantDroit, CampagnieAssurance , Commandes , CommandesMedicaments , CommandesUsager , Livraisons , Livreur , Medicament

class AssureForm(forms.ModelForm):
    class Meta:
        model = Assure 
        fields = ['nom' , 'prenom' , 'date de naissance' , 'Adresse' , 'Téléphone']

class AyantDroitForm(forms.ModelForm) :
    class Meta:
        model = AyantDroit
        fields = ['nom' , 'prenom' , 'date de naissance' , 'Adresse' , 'Téléphone']
class CampagnieAssurance(forms.ModelForm) :
    class Meta:
        model = CampagnieAssurance
        fields = ['Nom' , 'Pourcentage']