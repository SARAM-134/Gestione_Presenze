from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utente


@admin.register(Utente)
class UtenteAdmin(UserAdmin):
    list_display = ['username', 'nome', 'cognome', 'email', 'ruolo', 'is_active']
    list_filter = ['ruolo', 'is_active']
    search_fields = ['username', 'nome', 'cognome', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni Aggiuntive', {'fields': ('nome', 'cognome', 'ruolo')}),
    )
