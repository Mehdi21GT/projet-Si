from django.shortcuts import render , get_object_or_404, redirect
from .models import Conges ,personnel, service , SoldeConge , TypeConge ,OffreEmploi, Candidature, Entretien, Absence, Recrutement
from .forms import CongeForm , DemandeCongeForm ,OffreEmploiForm, CandidatureForm, EntretienForm
from django.db.models import Q ,Count, Avg
from datetime import date


def home(request):
     return render(request, 'home.html')

# Views
def liste_conges(request):
    conges = Conges.objects.all()
    types_conge = TypeConge.objects.all()

    type_conge_id = request.GET.get('type_conge')
    if type_conge_id:
        conges = conges.filter(type_conge_id=type_conge_id)

    context = {
        'conges': conges,
        'types_conge': types_conge,
    }
    return render(request, 'conges/liste_conges.html', context)

def ajouter_conge(request):
    if request.method == "POST":
        form = CongeForm(request.POST)
        if form.is_valid():
            conge = form.save(commit=False)

            # Vérifier si un solde de congé existe
            try:
                solde = SoldeConge.objects.get(employe=conge.employe, type_conge=conge.type_conge)
            except SoldeConge.DoesNotExist:
                messages.error(request, "Aucun solde de congé trouvé pour cet employé et ce type de congé.")
                return render(request, "conges/ajouter_conge.html", {"form": form})

            # Calculer les jours pris et valider
            jours_pris = (conge.date_fin - conge.date_debut).days + 1
            if solde.jours_disponibles < jours_pris:
                messages.error(request, "Le solde de congé est insuffisant.")
                return render(request, "conges/ajouter_conge.html", {"form": form})

            solde.jours_disponibles -= jours_pris
            solde.save()
            conge.jours_utilises = jours_pris
            conge.save()

            messages.success(request, "Le congé a été ajouté avec succès.")
            return redirect("liste_conges")
    else:
        form = CongeForm()

    return render(request, "conges/ajouter_conge.html", {"form": form})

def modifier_conge(request, conge_id):
    conge = get_object_or_404(Conges, id=conge_id)

    if request.method == 'POST':
        form = CongeForm(request.POST, instance=conge)
        if form.is_valid():
            form.save()
            messages.success(request, "Le congé a été modifié avec succès.")
            return redirect('liste_conges')
    else:
        form = CongeForm(instance=conge)

    return render(request, 'conges/modifier_conge.html', {'form': form, 'conge': conge})

def demander_conge(request):
    if request.method == "POST":
        form = DemandeCongeForm(request.POST)
        if form.is_valid():
            try:
                conge = form.save(commit=False)
                conge.employe = request.user.personnel  # Associe l'utilisateur connecté
                conge.save()
                messages.success(request, "Votre demande de congé a été soumise avec succès.")
                return redirect("liste_conges")
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = DemandeCongeForm()

    return render(request, "conges/demander_conge.html", {"form": form})
    

def liste_personnel(request):  # Changer le nom pour éviter le conflit
    # ✅ Récupérer tous les employés avec leur service
    personnel_list = personnel.objects.select_related('serviceEmp').all()

    return render(request, 'personnel.html', {'personnel': personnel_list})

def employe(request):
    return render(request, 'employe.html')

def ajouter_employe(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        dateN = request.POST['dateN']
        numT = request.POST['numT']
        email = request.POST['email']
        posteOccupe = request.POST['posteOccupe']
        dateEmbauche = request.POST['dateEmbauche']
        adresse = request.POST['adresse']
        serviceEmp_nom = request.POST['serviceEmp']

        serviceEmp, created = service.objects.get_or_create(nom=serviceEmp_nom)
        personnel.objects.create(
            nom=nom,
            prenom=prenom,
            dateN=dateN,
            numT=numT,
            email=email,
            posteOccupe=posteOccupe,
            dateEmbauche=dateEmbauche,
            adresse=adresse,
            serviceEmp=serviceEmp
        )
        return redirect('personnel')
    return render(request, 'ajouteremploye.html')

# Gestion des offres d'emploi
def liste_offres(request):
    offres = OffreEmploi.objects.all()
    return render(request, 'offre/liste_offres.html', {'offres': offres})

def ajouter_offre(request):
    if request.method == 'POST':
        form = OffreEmploiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_offres')
    else:
        form = OffreEmploiForm()
    return render(request, 'offre/ajouter_offre.html', {'form': form})

def modifier_offre(request, offre_id):
    offre = get_object_or_404(OffreEmploi, id=offre_id)
    if request.method == 'POST':
        form = OffreEmploiForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('liste_offres')
    else:
        form = OffreEmploiForm(instance=offre)
    return render(request, 'offre/modifier_offre.html', {'form': form})

def supprimer_offre(request, offre_id):
    offre = get_object_or_404(OffreEmploi, id=offre_id)
    if request.method == 'POST':
        offre.delete()
        return redirect('liste_offres')
    return render(request, 'offre/supprimer_offre.html', {'offre': offre})

# Suivi des candidatures
def liste_candidatures(request):
    candidatures = Candidature.objects.all()
    return render(request, 'candidatures/liste_candidatures.html', {'candidatures': candidatures})

def ajouter_candidature(request):
    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_candidatures')
    else:
        form = CandidatureForm()
    return render(request, 'candidatures/ajouter_candidatures.html', {'form': form})

# Gestion des entretiens
def planifier_entretien(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)
    if request.method == 'POST':
        form = EntretienForm(request.POST)
        if form.is_valid():
            entretien = form.save(commit=False)
            entretien.candidature = candidature
            entretien.save()
            return redirect('liste_candidatures')
    else:
        form = EntretienForm()
    return render(request, 'entretien/planifier_entretien.html', {'form': form, 'candidature': candidature})

def gestion_rec(request):
    return render(request, 'gestion_rec.html')

def dashboard(request):
    # Analyse des employés
    total_employes = personnel.objects.count()
    employes_par_type_contrat = personnel.objects.values('type_contrat').annotate(count=Count('id'))
    repartition_sexe = personnel.objects.values('sexe').annotate(count=Count('id'))

    # Top performeurs
    top_performeurs = personnel.objects.order_by('-score_evaluation')[:5]

    # Analyse des absences
    absences = Absence.objects.values('date_absence').annotate(count=Count('id')).order_by('-count')[:12]


    context = {
        'total_employes': total_employes,
        'employes_par_type_contrat': employes_par_type_contrat,
        'repartition_sexe': repartition_sexe,
        'top_performeurs': top_performeurs,
        'absences': absences,
    }

    return render(request, 'dashboard.html', context)