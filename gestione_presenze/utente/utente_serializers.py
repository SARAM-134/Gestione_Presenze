from rest_framework import serializers
from .models import Utente

class UtenteSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = Utente
        fields = [
            'id', 'username', 'email', 'matricola',
            'nome', 'cognome', 'full_name', 'ruolo',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class UtenteCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Utente
        fields = [
            'username', 'password', 'email', 'matricola',
            'nome', 'cognome', 'ruolo'
        ]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        utente = Utente(**validated_data)
        utente.set_password(password)
        utente.save()
        return utente
