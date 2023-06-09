from django.urls import path
from .import views

# -- 
urlpatterns = [
     path('assure/ajouter/', views.ajouter_assure, name='ajouter_assure'),
]
