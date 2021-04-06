from django.contrib import admin
from django.urls import path, include
from partage_repas import views
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('creer_repas/', views.creer_repas, name='creer_repas'),
    path('mesrepas/', views.mesrepas, name='mesrepas'),
    path('repas_details/<int:pk>/',views.repas_details,name='repas_details'),
    path('profil_details/<int:pk>/',views.profil_details,name='profil_details'),
    path('laisser_commentaire/<int:pk>', views.laisser_commentaire, name='laisser_commentaire'),
    path('reserver_repas/<int:pk>/', views.reserver_repas, name='reserver_repas'),
    path('supprimer_repas/<int:pk>/', views.supprimer_repas, name='supprimer_repas'),
    path('desinscrire_repas/<int:pk>/', views.desinscrire_repas, name='desinscrire_repas'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('profil/', views.profil, name='profil'),
    path('changer_mdp', views.changer_mdp, name='changer_mdp'),
    path('inscription/', views.inscription, name='inscription'),
    path('listerepas/', views.listerepas, name='listerepas'),
    path('<int:page>', views.listerepas, name='listerepas'),
    path('rechercher/', views.rechercher, name='rechercher'),
    path('', views.accueil, name='')
]
