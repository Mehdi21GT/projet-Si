from django.contrib import admin
from .models import personnel , service ,Conges,TypeConge ,SoldeConge
admin.site.register(personnel)
admin.site.register(service)
admin.site.register(TypeConge)
admin.site.register(SoldeConge)

@admin.register(Conges)
class CongeAdmin(admin.ModelAdmin):
    list_display = ("employe", "type_conge", "date_debut", "date_fin", "jours_utilises")
    search_fields = ("employe__nom", "employe__prenom", "type_conge__type")
    list_filter = ("type_conge", "date_debut", "date_fin")
