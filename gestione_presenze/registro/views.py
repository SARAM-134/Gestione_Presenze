from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from .models import Registro
from .serializers import RegistroSerializer, RegistroCreateUpdateSerializer
from .permissions import IsAdmin, IsOwnerOrAdmin


class RegistroViewSet(viewsets.ModelViewSet):
    """
    ViewSet per gestire i record di registro (presenze/assenze)
    """
    queryset = Registro.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Usa serializer diversi per create/update vs read
        """
        if self.action in ['create', 'update', 'partial_update']:
            return RegistroCreateUpdateSerializer
        return RegistroSerializer
    
    def get_queryset(self):
        """
        Filtra i risultati in base all'utente
        """
        user = self.request.user
        
        # Admin può vedere tutti i registri
        if user.ruolo == 'admin':
            queryset = Registro.objects.all()
        # Partecipante può vedere solo i propri
        elif user.ruolo == 'partecipante':
            queryset = Registro.objects.filter(
                partecipante__utente=user
            )
        else:
            queryset = Registro.objects.none()
        
        # Filtri opzionali via query params
        partecipante_id = self.request.query_params.get('partecipante', None)
        data_inizio = self.request.query_params.get('data_inizio', None)
        data_fine = self.request.query_params.get('data_fine', None)
        
        if partecipante_id:
            queryset = queryset.filter(partecipante_id=partecipante_id)
        if data_inizio:
            queryset = queryset.filter(data__gte=data_inizio)
        if data_fine:
            queryset = queryset.filter(data__lte=data_fine)
        
        return queryset
    
    def get_permissions(self):
        """
        Permessi diversi per azioni diverse
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Solo admin può creare/modificare/eliminare
            return [IsAdmin()]
        else:
            # Lettura: owner o admin
            return [IsOwnerOrAdmin()]
    
    def perform_create(self, serializer):
        """
        Salva chi ha creato il record
        """
        # Ottieni il profilo admin dell'utente corrente
        try:
            from admin_profile.models import Admin
            admin_profile = Admin.objects.get(utente=self.request.user)
            serializer.save(created_by=admin_profile)
        except Admin.DoesNotExist:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Endpoint per statistiche generali
        Solo per admin
        """
        if request.user.ruolo != 'admin':
            return Response(
                {'error': 'Solo gli admin possono accedere a questo endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Statistiche aggregate
        stats = Registro.objects.aggregate(
            totale_record=Count('id'),
            totale_ore=Sum('ore_totali'),
            totale_assenze=Sum('assenze')
        )
        
        ore_presenti = (stats['totale_ore'] or 0) - (stats['totale_assenze'] or 0)
        percentuale_media = 0.0
        if stats['totale_ore'] and stats['totale_ore'] > 0:
            percentuale_media = (ore_presenti / stats['totale_ore']) * 100
        
        return Response({
            'totale_record': stats['totale_record'],
            'totale_ore': stats['totale_ore'],
            'totale_assenze': stats['totale_assenze'],
            'ore_presenti': ore_presenti,
            'percentuale_presenza_media': round(percentuale_media, 2)
        })
