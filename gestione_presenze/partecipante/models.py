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


class Partecipante(models.Model):
    """
    Profilo partecipante - OneToOne con Utente
    """
    utente = models.OneToOneField(
        Utente,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='partecipante_profile'
    )
    profilo = models.TextField(blank=True, null=True, help_text="Bio o informazioni aggiuntive")
    attivo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Partecipante"
        verbose_name_plural = "Partecipanti"
    
    def __str__(self):
        return f"Partecipante: {self.utente.nome} {self.utente.cognome}"
    
    def calcola_percentuale_presenza(self):
        """
        Calcola la percentuale di presenza basata sui record registro
        """
        registri = self.registro_set.all()
        if not registri:
            return 0.0
        
        totale_ore = sum(r.ore_totali for r in registri)
        totale_assenze = sum(r.assenze for r in registri)
        
        if totale_ore == 0:
            return 0.0
        
        ore_presenti = totale_ore - totale_assenze
        percentuale = (ore_presenti / totale_ore) * 100
        return round(percentuale, 2)
