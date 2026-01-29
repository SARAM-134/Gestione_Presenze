from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from partecipante.models import Partecipante
from admin_profile.models import Admin


class Affluenza(models.Model):
    """
    Record presenze/assenze per ogni partecipante
    """
    partecipante = models.ForeignKey(
        Partecipante,
        on_delete=models.CASCADE,
        related_name='affluenza_set'
    )
    data = models.DateField()
    ore_totali = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Ore totali del giorno"
    )
    assenze = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Ore di assenza"
    )
    note = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        Admin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='affluenze_create'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Affluenza"
        verbose_name_plural = "Affluenze"
        ordering = ['-data']
        unique_together = ['partecipante', 'data']  # Un record per giorno
    
    def __str__(self):
        return f"{self.partecipante.utente.cognome} - {self.data}"
    
    def clean(self):
        """Validazione custom"""
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        # Non permettere date future
        if self.data > timezone.now().date():
            raise ValidationError("Non puoi inserire presenze future")
        
        # Assenze non possono superare ore totali
        if self.assenze > self.ore_totali:
            raise ValidationError("Le assenze non possono superare le ore totali")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def ore_presenti(self):
        """Calcola ore di presenza effettiva"""
        return self.ore_totali - self.assenze
    
    def percentuale_presenza(self):
        """Percentuale presenza per questo record"""
        if self.ore_totali == 0:
            return 0.0
        return round((self.ore_presenti() / self.ore_totali) * 100, 2)
