from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Admin
from .serializers import AdminProfileSerializer


class AdminProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet per gestire i profili Admin
    """
    queryset = Admin.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtra i risultati in base all'utente
        """
        user = self.request.user
        
        # Se è admin, può vedere tutti i profili admin
        if user.ruolo == 'admin':
            return Admin.objects.all()
        
        # Altrimenti nessun accesso
        return Admin.objects.none()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Endpoint per ottenere il proprio profilo admin
        """
        try:
            admin_profile = Admin.objects.get(utente=request.user)
            serializer = self.get_serializer(admin_profile)
            return Response(serializer.data)
        except Admin.DoesNotExist:
            return Response(
                {'error': 'Profilo admin non trovato'},
                status=404
            )
