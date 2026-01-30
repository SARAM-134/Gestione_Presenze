from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartecipanteViewSet

router = DefaultRouter()
router.register(r'', PartecipanteViewSet, basename='partecipante')

urlpatterns = [
    path('', include(router.urls)),
]
