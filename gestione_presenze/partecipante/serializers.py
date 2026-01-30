from rest_framework import serializers
from .models import Utente, Partecipante


class UtenteSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = Utente
        fields = [
            'id', 'username', 'email',
            'nome', 'cognome', 'full_name', 'ruolo',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UtenteCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Utente
        fields = [
            'username', 'password', 'email',
            'nome', 'cognome', 'ruolo'
        ]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        utente = Utente(**validated_data)
        utente.set_password(password)
        utente.save()
        return utente


class PartecipanteSerializer(serializers.ModelSerializer):
    utente = UtenteSerializer(read_only=True)
    percentuale_presenza = serializers.SerializerMethodField()
    
    class Meta:
        model = Partecipante
        fields = [
            'utente',
            'profilo',
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
