from rest_framework import serializers
from .models import AdminProfile
from utente.serializers import UtenteSerializer

class AdminProfileSerializer(serializers.ModelSerializer):
    utente = UtenteSerializer(read_only=True)
    
    class Meta:
        model = AdminProfile
        fields = ['utente', 'area_riservata_accesso', 'note']
