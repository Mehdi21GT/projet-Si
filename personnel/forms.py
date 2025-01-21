from django import forms
from .models import Conges , OffreEmploi, Candidature, Entretien

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conges
        fields = ["employe", "type_conge", "date_debut", "date_fin"]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class DemandeCongeForm(forms.ModelForm):
    class Meta:
        model = Conges
        fields = ['type_conge', 'date_debut', 'date_fin']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class OffreEmploiForm(forms.ModelForm):
    class Meta:
        model = OffreEmploi
        fields = '__all__'

class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['offre', 'nom_candidat', 'email_candidat', 'cv']

class EntretienForm(forms.ModelForm):
    class Meta:
        model = Entretien
        fields = '__all__'