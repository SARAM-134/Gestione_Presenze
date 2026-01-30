from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AffluenzaViewSet

router = DefaultRouter()
router.register(r'', AffluenzaViewSet, basename='affluenza')

urlpatterns = [
    path('', include(router.urls)),
]
