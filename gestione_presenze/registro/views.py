from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from .models import Registro
from .serializers import RegistroSerializer, RegistroUpdateSerializer
from .permissions import IsAdmin, IsOwnerOrAdmin


class RegistroViewSet(viewsets.ModelViewSet):
    """
    ViewSet per gestire i record di registro (presenze/assenze)
    Solo lettura e modifica - creazione ed eliminazione disabilitate
    """
    queryset = Registro.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Usa serializer diversi per update vs read
        """
        if self.action in ['update', 'partial_update']:
            return RegistroUpdateSerializer
        return RegistroSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Disabilita la creazione di nuovi record tramite API
        """
        return Response(
            {'error': 'La creazione di nuovi record non è permessa tramite API. Usa Django Admin.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Disabilita l'eliminazione di record tramite API
        """
        return Response(
            {'error': 'L\'eliminazione di record non è permessa tramite API. Usa Django Admin.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
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
        if self.action in ['update', 'partial_update']:
            # Solo admin può modificare
            return [IsAdmin()]
        else:
            # Lettura: owner o admin
            return [IsOwnerOrAdmin()]
    
    @action(detail=False, methods=['put'], permission_classes=[IsAdmin])
    def update_registro(self, request):
        """
        Endpoint per aggiornare un registro senza specificare l'ID
        Usa partecipante e data per trovare il record
        Solo per admin
        """
        partecipante_id = request.data.get('partecipante')
        data = request.data.get('data')
        
        if not partecipante_id or not data:
            return Response(
                {'error': 'Devi fornire sia partecipante che data'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Trova il registro basandosi su partecipante e data
            registro = Registro.objects.get(
                partecipante_id=partecipante_id,
                data=data
            )
        except Registro.DoesNotExist:
            return Response(
                {'error': f'Nessun registro trovato per partecipante {partecipante_id} in data {data}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Usa il serializer per validare e aggiornare
        serializer = RegistroUpdateSerializer(registro, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            # Ritorna il registro aggiornato con tutti i campi
            response_serializer = RegistroSerializer(registro)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
