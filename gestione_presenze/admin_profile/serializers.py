from rest_framework import serializers
from .models import Admin
from utente.serializers import UtenteSerializer

class AdminProfileSerializer(serializers.ModelSerializer):
    utente = UtenteSerializer(read_only=True)
    
    class Meta:
        model = Admin
        fields = ['utente', 'area_riservata_accesso']
