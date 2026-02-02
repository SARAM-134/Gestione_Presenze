from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Partecipante
from .serializers import PartecipanteSerializer, PartecipanteStatsSerializer


class PartecipanteViewSet(viewsets.ModelViewSet):
    """
    ViewSet per gestire i profili Partecipante
    """
    queryset = Partecipante.objects.all()
    serializer_class = PartecipanteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtra i risultati in base all'utente
        """
        user = self.request.user
        
        # Admin può vedere tutti i partecipanti
        if user.ruolo == 'admin':
            return Partecipante.objects.all()
        
        # Partecipante può vedere solo se stesso
        if user.ruolo == 'partecipante':
            return Partecipante.objects.filter(utente=user)
        
        return Partecipante.objects.none()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Endpoint per ottenere il proprio profilo partecipante
        """
        try:
            partecipante = Partecipante.objects.get(utente=request.user)
            serializer = self.get_serializer(partecipante)
            return Response(serializer.data)
        except Partecipante.DoesNotExist:
            return Response(
                {'error': 'Profilo partecipante non trovato'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        Endpoint per ottenere statistiche di un partecipante
        Include anche i dati personali del partecipante
        """
        partecipante = self.get_object()
        
        # Calcola statistiche
        registri = partecipante.registro_set.all()
        totale_giorni = registri.count()
        totale_ore = sum(r.ore_totali for r in registri)
        totale_assenze = sum(r.assenze for r in registri)
        ore_presenti = totale_ore - totale_assenze
        
        percentuale_presenza = 0.0
        if totale_ore > 0:
            percentuale_presenza = (ore_presenti / totale_ore) * 100
        
        stats_data = {
            # Dati personali
            'nome': partecipante.utente.nome,
            'cognome': partecipante.utente.cognome,
            'email': partecipante.utente.email,
            # Statistiche
            'totale_giorni': totale_giorni,
            'totale_ore': totale_ore,
            'totale_assenze': totale_assenze,
            'ore_presenti': ore_presenti,
            'percentuale_presenza': round(percentuale_presenza, 2)
        }
        
        serializer = PartecipanteStatsSerializer(stats_data)
        return Response(serializer.data)
