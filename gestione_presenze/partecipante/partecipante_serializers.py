from rest_framework import serializers
from .models import Partecipante
from utente.serializers import UtenteSerializer

class PartecipanteSerializer(serializers.ModelSerializer):
    utente = UtenteSerializer(read_only=True)
    percentuale_presenza = serializers.SerializerMethodField()
    
    class Meta:
        model = Partecipante
        fields = [
            'utente',
            'data_nascita',
            'comune',
            'numero_telefono',
            'attivo',
            'percentuale_presenza'
        ]
    
    def get_percentuale_presenza(self, obj):
        return obj.calcola_percentuale_presenza()

class PartecipanteStatsSerializer(serializers.Serializer):
    """Serializer per statistiche partecipante"""
    totale_giorni = serializers.IntegerField()
    totale_ore = serializers.DecimalField(max_digits=10, decimal_places=2)
    totale_assenze = serializers.DecimalField(max_digits=10, decimal_places=2)
    ore_presenti = serializers.DecimalField(max_digits=10, decimal_places=2)
    percentuale_presenza = serializers.DecimalField(max_digits=5, decimal_places=2)
