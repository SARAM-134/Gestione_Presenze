from django.contrib import admin
from .models import Utente, Partecipante


@admin.register(Utente)
class UtenteAdmin(admin.ModelAdmin):
    list_display = ['username', 'nome', 'cognome', 'email', 'ruolo', 'is_active']
    list_filter = ['ruolo', 'is_active']
    search_fields = ['username', 'nome', 'cognome', 'email']


@admin.register(Partecipante)
class PartecipanteAdmin(admin.ModelAdmin):
    list_display = ['utente', 'attivo', 'get_percentuale_presenza']
    list_filter = ['attivo']
    search_fields = ['utente__nome', 'utente__cognome']
    
    def get_percentuale_presenza(self, obj):
        return f"{obj.calcola_percentuale_presenza()}%"
    get_percentuale_presenza.short_description = 'Presenza %'

