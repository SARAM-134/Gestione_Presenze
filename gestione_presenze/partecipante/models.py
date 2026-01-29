from django.db import models
from utente.models import Utente


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
        Calcola la percentuale di presenza basata sui record affluenza
        """
        affluenze = self.affluenza_set.all()
        if not affluenze:
            return 0.0
        
        totale_ore = sum(a.ore_totali for a in affluenze)
        totale_assenze = sum(a.assenze for a in affluenze)
        
        if totale_ore == 0:
            return 0.0
        
        ore_presenti = totale_ore - totale_assenze
        percentuale = (ore_presenti / totale_ore) * 100
        return round(percentuale, 2)
