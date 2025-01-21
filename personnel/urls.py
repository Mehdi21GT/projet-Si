from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('personnel/', views.liste_personnel, name='personnel'),  
    path('employe/', views.employe, name='employe'),
    path('ajouteremploye/', views.ajouter_employe, name='ajouter_employe'),
    path('conges/liste/', views.liste_conges, name='liste_conges'),
    path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),
    path('conges/modifier/', views.modifier_conge, name='modifier_conge'),
    path('conges/demander/', views.demander_conge, name='demander_conge'),
    path('offres/', views.liste_offres, name='liste_offres'),
    path('gestion_rec/', views.gestion_rec, name='gestion_rec'),
    path('offres/ajouter/', views.ajouter_offre, name='ajouter_offre'),
    path('offres/modifier/<int:offre_id>/', views.modifier_offre, name='modifier_offre'),
    path('offres/supprimer/<int:offre_id>/', views.supprimer_offre, name='supprimer_offre'),
    path('candidatures/', views.liste_candidatures, name='liste_candidatures'),
    path('candidatures/ajouter/', views.ajouter_candidature, name='ajouter_candidature'),
    path('entretiens/planifier/<int:candidature_id>/', views.planifier_entretien, name='planifier_entretien'),
    path('dashboard/', views.dashboard, name='dashboard')

]