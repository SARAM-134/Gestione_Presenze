from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permission per verificare che l'utente sia Admin
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.ruolo == 'admin'
        )

class IsPartecipante(permissions.BasePermission):
    """
    Permission per verificare che l'utente sia Partecipante
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.ruolo == 'partecipante'
        )

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission che permette accesso al proprietario o admin
    """
    def has_object_permission(self, request, view, obj):
        # Admin ha sempre accesso
        if request.user.ruolo == 'admin':
            return True
        
        # Partecipante può accedere solo ai propri dati
        if hasattr(obj, 'partecipante'):
            return obj.partecipante.utente == request.user
        
        return False
