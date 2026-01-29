from django.contrib import admin
from .models import Affluenza


@admin.register(Affluenza)
class AffluenzaAdmin(admin.ModelAdmin):
    list_display = ['partecipante', 'data', 'ore_totali', 'assenze', 'ore_presenti', 'created_by']
    list_filter = ['data', 'created_by']
    search_fields = ['partecipante__utente__nome', 'partecipante__utente__cognome']
    date_hierarchy = 'data'
    
    def ore_presenti(self, obj):
        return obj.ore_presenti()
    ore_presenti.short_description = 'Ore Presenti'
