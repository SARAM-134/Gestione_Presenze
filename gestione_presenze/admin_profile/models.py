from django.db import models
from utente.models import Utente


class Admin(models.Model):
    """
    Profilo admin - OneToOne con Utente
    """
    utente = models.OneToOneField(
        Utente,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='admin_profile'
    )
    area_riservata_accesso = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"
    
    def __str__(self):
        return f"Admin: {self.utente.nome} {self.utente.cognome}"
