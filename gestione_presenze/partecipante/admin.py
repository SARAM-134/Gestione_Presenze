from django.contrib import admin
from .models import Partecipante


@admin.register(Partecipante)
class PartecipanteAdmin(admin.ModelAdmin):
    list_display = ['utente', 'attivo', 'get_percentuale_presenza']
    list_filter = ['attivo']
    search_fields = ['utente__nome', 'utente__cognome']
    
    def get_percentuale_presenza(self, obj):
        return f"{obj.calcola_percentuale_presenza()}%"
    get_percentuale_presenza.short_description = 'Presenza %'
