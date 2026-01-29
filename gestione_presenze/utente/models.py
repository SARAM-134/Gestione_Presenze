from django.db import models
from django.contrib.auth.models import AbstractUser


class Utente(AbstractUser):
    """
    Modello base utente - estende AbstractUser di Django
    """
    RUOLO_CHOICES = [
        ('admin', 'Admin'),
        ('partecipante', 'Partecipante'),
    ]
    
    ruolo = models.CharField(
        max_length=20,
        choices=RUOLO_CHOICES,
        default='partecipante'
    )
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"
    
    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.ruolo})"
