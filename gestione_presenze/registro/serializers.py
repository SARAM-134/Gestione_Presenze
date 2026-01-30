from rest_framework import serializers
from .models import Registro

class RegistroSerializer(serializers.ModelSerializer):
    partecipante_nome = serializers.CharField(
        source='partecipante.utente.nome',
        read_only=True
    )
    partecipante_cognome = serializers.CharField(
        source='partecipante.utente.cognome',
        read_only=True
    )
    ore_presenti = serializers.SerializerMethodField()
    percentuale_presenza = serializers.SerializerMethodField()
    
    class Meta:
        model = Registro
        fields = [
            'id',
            'partecipante',
            'partecipante_nome',
            'partecipante_cognome',
            'matricola',
            'data',
            'ore_totali',
            'assenze',
            'ore_presenti',
            'percentuale_presenza',
            'registro_admin',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'matricola', 'created_at', 'updated_at']
    
    def get_ore_presenti(self, obj):
        return float(obj.ore_presenti())
    
    def get_percentuale_presenza(self, obj):
        return obj.percentuale_presenza()

class RegistroCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer per creazione/modifica registro da parte admin"""
    
    class Meta:
        model = Registro
        fields = [
            'partecipante',
            'data',
            'ore_totali',
            'assenze'
        ]
    
    def validate(self, data):
        """Validazione dati"""
        if data['assenze'] > data['ore_totali']:
            raise serializers.ValidationError({
                'assenze': 'Le ore di assenza non possono superare le ore totali.'
            })
        return data
