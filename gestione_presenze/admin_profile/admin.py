from django.contrib import admin
from .models import Admin as AdminModel


@admin.register(AdminModel)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['utente', 'area_riservata_accesso']
