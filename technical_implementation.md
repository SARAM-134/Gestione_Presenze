# Guida Tecnica Implementazione - Attendance System

## 📁 Struttura File Django Completa

```
attendance_project/
├── manage.py
├── requirements.txt
├── README.md
├── attendance_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── core/
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── serializers.py
    ├── permissions.py
    ├── urls.py
    ├── admin.py
    └── migrations/
```

---

## 📦 Requirements.txt

```txt
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
python-dotenv==1.0.0
```

---

## 🔧 PERSONA 1 - Models Implementation

### core/models.py

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Utente(AbstractUser):
    """
    Modello base utente - estende AbstractUser di Django
    """
    RUOLO_CHOICES = [
        ('admin', 'Admin'),
        ('partecipante', 'Partecipante'),
    ]
    
    ruolo = models.CharField(
        max_length=20,
        choices=RUOLO_CHOICES,
        default='partecipante'
    )
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"
    
    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.ruolo})"


class Partecipante(models.Model):
    """
    Profilo partecipante - OneToOne con Utente
    """
    utente = models.OneToOneField(
        Utente,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='partecipante_profile'
    )
    profilo = models.TextField(blank=True, null=True, help_text="Bio o informazioni aggiuntive")
    attivo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Partecipante"
        verbose_name_plural = "Partecipanti"
    
    def __str__(self):
        return f"Partecipante: {self.utente.nome} {self.utente.cognome}"
    
    def calcola_percentuale_presenza(self):
        """
        Calcola la percentuale di presenza basata sui record affluenza
        """
        affluenze = self.affluenza_set.all()
        if not affluenze:
            return 0.0
        
        totale_ore = sum(a.ore_totali for a in affluenze)
        totale_assenze = sum(a.assenze for a in affluenze)
        
        if totale_ore == 0:
            return 0.0
        
        ore_presenti = totale_ore - totale_assenze
        percentuale = (ore_presenti / totale_ore) * 100
        return round(percentuale, 2)


class Admin(models.Model):
    """
    Profilo admin - OneToOne con Utente
    """
    utente = models.OneToOneField(
        Utente,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='admin_profile'
    )
    area_riservata_accesso = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"
    
    def __str__(self):
        return f"Admin: {self.utente.nome} {self.utente.cognome}"


class Affluenza(models.Model):
    """
    Record presenze/assenze per ogni partecipante
    """
    partecipante = models.ForeignKey(
        Partecipante,
        on_delete=models.CASCADE,
        related_name='affluenza_set'
    )
    data = models.DateField()
    ore_totali = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Ore totali del giorno"
    )
    assenze = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Ore di assenza"
    )
    note = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        Admin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='affluenze_create'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Affluenza"
        verbose_name_plural = "Affluenze"
        ordering = ['-data']
        unique_together = ['partecipante', 'data']  # Un record per giorno
    
    def __str__(self):
        return f"{self.partecipante.utente.cognome} - {self.data}"
    
    def clean(self):
        """Validazione custom"""
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        # Non permettere date future
        if self.data > timezone.now().date():
            raise ValidationError("Non puoi inserire presenze future")
        
        # Assenze non possono superare ore totali
        if self.assenze > self.ore_totali:
            raise ValidationError("Le assenze non possono superare le ore totali")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def ore_presenti(self):
        """Calcola ore di presenza effettiva"""
        return self.ore_totali - self.assenze
    
    def percentuale_presenza(self):
        """Percentuale presenza per questo record"""
        if self.ore_totali == 0:
            return 0.0
        return round((self.ore_presenti() / self.ore_totali) * 100, 2)
```

### core/admin.py

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utente, Partecipante, Admin, Affluenza

@admin.register(Utente)
class UtenteAdmin(UserAdmin):
    list_display = ['username', 'nome', 'cognome', 'email', 'ruolo', 'is_active']
    list_filter = ['ruolo', 'is_active']
    search_fields = ['username', 'nome', 'cognome', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni Aggiuntive', {'fields': ('nome', 'cognome', 'ruolo')}),
    )

@admin.register(Partecipante)
class PartecipanteAdmin(admin.ModelAdmin):
    list_display = ['utente', 'attivo', 'get_percentuale_presenza']
    list_filter = ['attivo']
    search_fields = ['utente__nome', 'utente__cognome']
    
    def get_percentuale_presenza(self, obj):
        return f"{obj.calcola_percentuale_presenza()}%"
    get_percentuale_presenza.short_description = 'Presenza %'

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['utente', 'area_riservata_accesso']

@admin.register(Affluenza)
class AffluenzaAdmin(admin.ModelAdmin):
    list_display = ['partecipante', 'data', 'ore_totali', 'assenze', 'ore_presenti', 'created_by']
    list_filter = ['data', 'created_by']
    search_fields = ['partecipante__utente__nome', 'partecipante__utente__cognome']
    date_hierarchy = 'data'
    
    def ore_presenti(self, obj):
        return obj.ore_presenti()
    ore_presenti.short_description = 'Ore Presenti'
```

---

## 🔐 PERSONA 2 - Authentication & Serializers

### core/serializers.py

```python
from rest_framework import serializers
from .models import Utente, Partecipante, Admin, Affluenza

class UtenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = ['id', 'username', 'email', 'nome', 'cognome', 'ruolo']
        read_only_fields = ['id']

class PartecipanteSerializer(serializers.ModelSerializer):
    utente = UtenteSerializer(read_only=True)
    percentuale_presenza = serializers.SerializerMethodField()
    
    class Meta:
        model = Partecipante
        fields = ['utente', 'profilo', 'attivo', 'percentuale_presenza']
    
    def get_percentuale_presenza(self, obj):
        return obj.calcola_percentuale_presenza()

class AffluenzaSerializer(serializers.ModelSerializer):
    partecipante_nome = serializers.CharField(
        source='partecipante.utente.nome',
        read_only=True
    )
    partecipante_cognome = serializers.CharField(
        source='partecipante.utente.cognome',
        read_only=True
    )
    ore_presenti = serializers.SerializerMethodField()
    percentuale_presenza = serializers.SerializerMethodField()
    
    class Meta:
        model = Affluenza
        fields = [
            'id', 'partecipante', 'partecipante_nome', 'partecipante_cognome',
            'data', 'ore_totali', 'assenze', 'ore_presenti', 
            'percentuale_presenza', 'note', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_ore_presenti(self, obj):
        return float(obj.ore_presenti())
    
    def get_percentuale_presenza(self, obj):
        return obj.percentuale_presenza()

class PartecipanteStatsSerializer(serializers.Serializer):
    """Serializer per statistiche partecipante"""
    totale_giorni = serializers.IntegerField()
    totale_ore = serializers.DecimalField(max_digits=10, decimal_places=2)
    totale_assenze = serializers.DecimalField(max_digits=10, decimal_places=2)
    ore_presenti = serializers.DecimalField(max_digits=10, decimal_places=2)
    percentuale_presenza = serializers.DecimalField(max_digits=5, decimal_places=2)
```

### core/permissions.py

```python
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
```

### core/views.py (Parte Persona 2)

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Partecipante, Affluenza
from .serializers import (
    PartecipanteSerializer, 
    AffluenzaSerializer,
    PartecipanteStatsSerializer
)
from .permissions import IsPartecipante
from decimal import Decimal

class PartecipanteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet per Partecipante - Solo lettura
    """
    permission_classes = [IsAuthenticated, IsPartecipante]
    serializer_class = PartecipanteSerializer
    
    def get_queryset(self):
        # Partecipante vede solo sé stesso
        return Partecipante.objects.filter(utente=self.request.user)
    
    @action(detail=False, methods=['get'])
    def presenze(self, request):
        """
        GET /api/partecipante/presenze/
        Visualizza tutte le presenze del partecipante loggato
        """
        partecipante = get_object_or_404(
            Partecipante, 
            utente=request.user
        )
        affluenze = Affluenza.objects.filter(
            partecipante=partecipante
        ).order_by('-data')
        
        serializer = AffluenzaSerializer(affluenze, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        GET /api/partecipante/stats/
        Statistiche del partecipante loggato
        """
        partecipante = get_object_or_404(
            Partecipante, 
            utente=request.user
        )
        affluenze = Affluenza.objects.filter(partecipante=partecipante)
        
        totale_ore = sum(a.ore_totali for a in affluenze)
        totale_assenze = sum(a.assenze for a in affluenze)
        ore_presenti = totale_ore - totale_assenze
        
        percentuale = 0.0
        if totale_ore > 0:
            percentuale = (ore_presenti / totale_ore) * 100
        
        stats = {
            'totale_giorni': affluenze.count(),
            'totale_ore': totale_ore,
            'totale_assenze': totale_assenze,
            'ore_presenti': ore_presenti,
            'percentuale_presenza': round(percentuale, 2)
        }
        
        serializer = PartecipanteStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def profilo(self, request):
        """
        PUT/PATCH /api/partecipante/profilo/
        Aggiorna il profilo del partecipante (funzionalità opzionale)
        """
        partecipante = get_object_or_404(
            Partecipante,
            utente=request.user
        )
        
        if 'profilo' in request.data:
            partecipante.profilo = request.data['profilo']
            partecipante.save()
        
        serializer = PartecipanteSerializer(partecipante)
        return Response(serializer.data)
```

---

## 👑 PERSONA 3 - Admin Features

### core/views.py (Parte Persona 3)

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Partecipante, Affluenza, Admin
from .serializers import PartecipanteSerializer, AffluenzaSerializer
from .permissions import IsAdmin

class AdminViewSet(viewsets.ViewSet):
    """
    ViewSet per operazioni Admin
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def list(self, request):
        """
        GET /api/admin/partecipanti/
        Lista tutti i partecipanti
        """
        partecipanti = Partecipante.objects.all()
        serializer = PartecipanteSerializer(partecipanti, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def partecipante_presenze(self, request):
        """
        GET /api/admin/partecipante-presenze/?partecipante_id=X
        Presenze di un partecipante specifico
        """
        partecipante_id = request.query_params.get('partecipante_id')
        
        if not partecipante_id:
            return Response(
                {'error': 'partecipante_id richiesto'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        partecipante = get_object_or_404(Partecipante, pk=partecipante_id)
        affluenze = Affluenza.objects.filter(
            partecipante=partecipante
        ).order_by('-data')
        
        serializer = AffluenzaSerializer(affluenze, many=True)
        return Response(serializer.data)


class AffluenzaViewSet(viewsets.ModelViewSet):
    """
    ViewSet per gestione affluenze (CRUD completo per Admin)
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AffluenzaSerializer
    queryset = Affluenza.objects.all().order_by('-data')
    
    def perform_create(self, serializer):
        """
        POST /api/affluenza/
        Crea nuovo record affluenza
        """
        # Collega l'admin che ha creato il record
        try:
            admin = Admin.objects.get(utente=self.request.user)
            serializer.save(created_by=admin)
        except Admin.DoesNotExist:
            serializer.save()
    
    def perform_update(self, serializer):
        """
        PUT/PATCH /api/affluenza/<id>/
        Modifica record affluenza esistente
        """
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        """
        DELETE /api/affluenza/<id>/
        Elimina record affluenza
        """
        instance = self.get_object()
        instance.delete()
        return Response(
            {'message': 'Record eliminato con successo'},
            status=status.HTTP_204_NO_CONTENT
        )
```

---

## 🌐 URL Configuration

### core/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PartecipanteViewSet, AdminViewSet, AffluenzaViewSet

router = DefaultRouter()
router.register(r'partecipante', PartecipanteViewSet, basename='partecipante')
router.register(r'admin', AdminViewSet, basename='admin')
router.register(r'affluenza', AffluenzaViewSet, basename='affluenza')

urlpatterns = [
    # Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Routes
    path('', include(router.urls)),
]
```

### attendance_project/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]
```

---

## ⚙️ Settings Configuration

### attendance_project/settings.py (Aggiunte necessarie)

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    
    # Local
    'core',
]

# Custom User Model
AUTH_USER_MODEL = 'core.Utente'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 🧪 Testing con Postman

### 1. Login (Ottenere Token)
```
POST http://localhost:8000/api/auth/login/
Body (JSON):
{
    "username": "mario.rossi",
    "password": "password123"
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLC...",
    "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

### 2. API Partecipante - Vedere presenze
```
GET http://localhost:8000/api/partecipante/presenze/
Headers:
Authorization: Bearer {access_token}
```

### 3. API Admin - Creare affluenza
```
POST http://localhost:8000/api/affluenza/
Headers:
Authorization: Bearer {access_token}
Body (JSON):
{
    "partecipante": 1,
    "data": "2026-01-28",
    "ore_totali": "8.00",
    "assenze": "2.00",
    "note": "Assenza pomeridiana"
}
```

---

## 🎯 Script Popolazione Database

### populate_db.py (Da creare nella root)

```python
import os
import django
from datetime import date, timedelta
from decimal import Decimal
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_project.settings')
django.setup()

from core.models import Utente, Partecipante, Admin, Affluenza

def populate():
    print("🚀 Inizializzazione database...")
    
    # Creare Admin
    admin1 = Utente.objects.create_user(
        username='admin1',
        email='admin1@example.com',
        password='admin123',
        nome='Marco',
        cognome='Bianchi',
        ruolo='admin'
    )
    Admin.objects.create(utente=admin1)
    print("✅ Admin creato: admin1")
    
    # Creare Partecipanti
    partecipanti_data = [
        ('mario.rossi', 'Mario', 'Rossi'),
        ('laura.verdi', 'Laura', 'Verdi'),
        ('paolo.neri', 'Paolo', 'Neri'),
        ('giulia.blu', 'Giulia', 'Blu'),
        ('luca.gialli', 'Luca', 'Gialli'),
    ]
    
    partecipanti = []
    for username, nome, cognome in partecipanti_data:
        utente = Utente.objects.create_user(
            username=username,
            email=f'{username}@example.com',
            password='pass123',
            nome=nome,
            cognome=cognome,
            ruolo='partecipante'
        )
        part = Partecipante.objects.create(
            utente=utente,
            profilo=f"Profilo di {nome} {cognome}"
        )
        partecipanti.append(part)
        print(f"✅ Partecipante creato: {username}")
    
    # Creare Affluenze (ultimi 20 giorni)
    admin_obj = Admin.objects.first()
    start_date = date.today() - timedelta(days=20)
    
    for i in range(20):
        current_date = start_date + timedelta(days=i)
        
        for part in partecipanti:
            # Varia la presenza: alcuni partecipanti più presenti
            if random.random() < 0.9:  # 90% probabilità di record
                ore_totali = Decimal('8.00')
                # Assenze casuali 0-3 ore
                assenze = Decimal(str(random.choice([0, 0, 0, 1, 2, 3])))
                
                Affluenza.objects.create(
                    partecipante=part,
                    data=current_date,
                    ore_totali=ore_totali,
                    assenze=assenze,
                    created_by=admin_obj
                )
    
    print("✅ Affluenze create per ultimi 20 giorni")
    print("\n🎉 Database popolato con successo!")
    print("\n📊 Riepilogo:")
    print(f"   Admin: {Utente.objects.filter(ruolo='admin').count()}")
    print(f"   Partecipanti: {Partecipante.objects.count()}")
    print(f"   Record Affluenza: {Affluenza.objects.count()}")

if __name__ == '__main__':
    populate()
```

**Eseguire con:**
```bash
python populate_db.py
```

---

## 📝 Comandi Utili

```bash
# Creare progetto
django-admin startproject attendance_project
cd attendance_project
python manage.py startapp core

# Migrazioni
python manage.py makemigrations
python manage.py migrate

# Creare superuser
python manage.py createsuperuser

# Avviare server
python manage.py runserver

# Popolare database
python populate_db.py

# Shell Django (per testing)
python manage.py shell
```

---

**Questa guida fornisce il codice completo pronto all'uso per tutte e 3 le persone! 🚀**
