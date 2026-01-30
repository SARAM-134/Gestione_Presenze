# 📘 Guida Completa - Sistema Gestione Presenze

**Versione**: 2.0 (Aggiornata 30/01/2026)  
**Stato**: Progetto Completato e Funzionante ✅

---

## 📋 Indice

1. [Panoramica Progetto](#panoramica-progetto)
2. [Struttura Attuale](#struttura-attuale)
3. [Architettura Database](#architettura-database)
4. [Setup e Installazione](#setup-e-installazione)
5. [Struttura Codice](#struttura-codice)
6. [API Endpoints](#api-endpoints)
7. [Testing](#testing)
8. [Credenziali di Accesso](#credenziali-di-accesso)

---

## 📋 Panoramica Progetto

### Obiettivo
Sistema backend Django per gestione presenze/assenze con autenticazione JWT e due ruoli utente (Admin e Partecipante).

### Stack Tecnologico
- **Backend**: Python 3.14, Django 6.0.1
- **API**: Django REST Framework 3.16.1
- **Autenticazione**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite
- **Virtual Environment**: venv

### Funzionalità Principali
- ✅ Autenticazione JWT per Admin e Partecipanti
- ✅ Admin: gestione completa presenze/assenze
- ✅ Partecipanti: visualizzazione proprie presenze e statistiche
- ✅ Calcolo automatico percentuali presenza
- ✅ Validazioni business logic (no date future, ore coerenti)

---

## 🏗️ Struttura Attuale

### Directory Tree
```
Gestione_Presenze/
├── venv/                          # Virtual environment
├── gestione_presenze/             # Progetto Django
│   ├── manage.py
│   ├── populate_db.py             # Script popolazione database
│   ├── db.sqlite3                 # Database SQLite
│   │
│   ├── gestione_presenze/         # Configurazione progetto
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── partecipante/              # App Partecipante + Utente
│   │   ├── models.py              # Utente + Partecipante
│   │   ├── serializers.py         # Tutti i serializers utente
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── admin_profile/             # App Admin
│   │   ├── models.py              # Admin
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   └── registro/                  # App Registro (ex affluenza)
│       ├── models.py              # Registro
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── permissions.py
│       ├── admin.py
│       └── migrations/
│
├── attendance_project_plan.md     # Piano originale
├── quick_start_guide.md           # Guida setup veloce
├── technical_implementation.md    # Dettagli tecnici
└── README.md
```

### App Django

#### 1. **partecipante** (App principale utenti)
Contiene:
- Modello `Utente` (AbstractUser) - base per autenticazione
- Modello `Partecipante` - profilo partecipante
- Serializers per entrambi i modelli
- ViewSet per operazioni partecipante

#### 2. **admin_profile**
Contiene:
- Modello `Admin` - profilo amministratore
- Serializers admin
- ViewSet per operazioni admin

#### 3. **registro** (ex affluenza)
Contiene:
- Modello `Registro` - record presenze/assenze
- Serializers registro
- ViewSet CRUD completo
- Permissions custom (IsAdmin, IsOwnerOrAdmin)

---

## 🗄️ Architettura Database

### Schema Relazionale

```
┌─────────────────────────────────┐
│         Utente                  │
│  (partecipante.models.Utente)   │
├─────────────────────────────────┤
│ id (PK)                         │
│ username (Unique)               │
│ email                           │
│ password (Hashed)               │
│ nome                            │
│ cognome                         │
│ ruolo ('admin'/'partecipante')  │
│ created_at                      │
│ updated_at                      │
└─────────────────────────────────┘
         │                │
         │                │
         ▼                ▼
┌──────────────┐   ┌──────────────┐
│ Partecipante │   │    Admin     │
├──────────────┤   ├──────────────┤
│ utente (FK)  │   │ utente (FK)  │
│ profilo      │   └──────────────┘
│ attivo       │
└──────────────┘
         │
         │ (1:N)
         ▼
┌─────────────────────────────────┐
│          Registro               │
├─────────────────────────────────┤
│ id (PK)                         │
│ partecipante_id (FK)            │
│ data (Date)                     │
│ ore_totali (Decimal)            │
│ assenze (Decimal)               │
│ note (Text)                     │
│ created_by (FK → Admin)         │
│ created_at                      │
└─────────────────────────────────┘
```

### Modelli Dettagliati

#### Utente (partecipante/models.py)
```python
class Utente(AbstractUser):
    ruolo = CharField(choices=['admin', 'partecipante'])
    nome = CharField(max_length=100)
    cognome = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

#### Partecipante (partecipante/models.py)
```python
class Partecipante(Model):
    utente = OneToOneField(Utente, primary_key=True)
    profilo = TextField(blank=True, null=True)
    attivo = BooleanField(default=True)
    
    def calcola_percentuale_presenza() → float
```

#### Admin (admin_profile/models.py)
```python
class Admin(Model):
    utente = OneToOneField(Utente, primary_key=True)
```

#### Registro (registro/models.py)
```python
class Registro(Model):
    partecipante = ForeignKey(Partecipante)
    data = DateField()
    ore_totali = DecimalField(max_digits=4, decimal_places=2)
    assenze = DecimalField(max_digits=4, decimal_places=2)
    note = TextField(blank=True, null=True)
    created_by = ForeignKey(Admin, null=True)
    created_at = DateTimeField(auto_now_add=True)
    
    # Constraint: unique_together = ['partecipante', 'data']
    
    def ore_presenti() → Decimal
    def percentuale_presenza() → float
```

---

## 🚀 Setup e Installazione

### Prerequisiti
- Python 3.14+
- pip
- virtualenv

### Installazione Rapida

```bash
# 1. Clona/Naviga nella directory progetto
cd Gestione_Presenze/Gestione_Presenze/gestione_presenze

# 2. Attiva virtual environment
source ../venv/bin/activate  # Mac/Linux
# ../venv/Scripts/activate   # Windows

# 3. Verifica dipendenze (già installate)
pip list | grep -E "Django|djangorestframework"

# 4. Verifica database e migrazioni
python manage.py check

# 5. Popola database con dati di test
python populate_db.py

# 6. Avvia server
python manage.py runserver
```

### Configurazione (settings.py)

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'admin_profile',
    'registro',
    'partecipante',
]

AUTH_USER_MODEL = 'partecipante.Utente'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

---

## 💻 Struttura Codice

### URL Configuration

**gestione_presenze/urls.py** (Main)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/partecipante/', include('partecipante.urls')),
    path('api/admin/', include('admin_profile.urls')),
    path('api/registro/', include('registro.urls')),
]
```

### Permissions (registro/permissions.py)

```python
class IsAdmin(BasePermission):
    """Verifica che l'utente sia Admin"""
    def has_permission(self, request, view):
        return request.user.ruolo == 'admin'

class IsPartecipante(BasePermission):
    """Verifica che l'utente sia Partecipante"""
    def has_permission(self, request, view):
        return request.user.ruolo == 'partecipante'

class IsOwnerOrAdmin(BasePermission):
    """Admin o proprietario dei dati"""
    def has_object_permission(self, request, view, obj):
        if request.user.ruolo == 'admin':
            return True
        return obj.partecipante.utente == request.user
```

### Business Logic

#### Validazioni Registro
- ❌ Non permettere date future
- ❌ Assenze non possono superare ore totali
- ✅ Un solo record per partecipante per giorno (unique_together)

#### Calcoli Automatici
```python
# Ore presenti per singolo record
ore_presenti = ore_totali - assenze

# Percentuale presenza partecipante
totale_ore = sum(registro.ore_totali for all records)
totale_assenze = sum(registro.assenze for all records)
percentuale = ((totale_ore - totale_assenze) / totale_ore) * 100
```

---

## 🌐 API Endpoints

### Autenticazione

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "admin1",
    "password": "admin123"
}

Response 200:
{
    "access": "eyJ0eXAiOiJKV1QiLC...",
    "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

#### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLC..."
}

Response 200:
{
    "access": "eyJ0eXAiOiJKV1QiLC..."
}
```

---

### Partecipante Endpoints

**Autenticazione richiesta**: JWT Token  
**Permessi**: Ruolo `partecipante`

#### Visualizza Profilo
```http
GET /api/partecipante/me/
Authorization: Bearer {access_token}

Response 200:
{
    "utente": {
        "id": 3,
        "username": "part1",
        "nome": "Mario",
        "cognome": "Rossi",
        "ruolo": "partecipante"
    },
    "profilo": "Profilo partecipante",
    "attivo": true,
    "percentuale_presenza": 89.38
}
```

#### Visualizza Proprie Presenze
```http
GET /api/partecipante/{id}/
Authorization: Bearer {access_token}

Response 200:
[
    {
        "id": 1,
        "data": "2026-01-30",
        "ore_totali": "8.00",
        "assenze": "2.00",
        "ore_presenti": 6.00,
        "percentuale_presenza": 75.00,
        "note": ""
    },
    ...
]
```

#### Statistiche Personali
```http
GET /api/partecipante/{id}/stats/
Authorization: Bearer {access_token}

Response 200:
{
    "totale_giorni": 10,
    "totale_ore": "80.00",
    "totale_assenze": "8.50",
    "ore_presenti": "71.50",
    "percentuale_presenza": 89.38
}
```

---

### Admin Endpoints

**Autenticazione richiesta**: JWT Token  
**Permessi**: Ruolo `admin`

#### Lista Tutti i Partecipanti
```http
GET /api/admin/profile/
Authorization: Bearer {admin_token}

Response 200:
[
    {
        "utente": {...},
        "profilo": "...",
        "attivo": true,
        "percentuale_presenza": 89.38
    },
    ...
]
```

#### Profilo Admin Corrente
```http
GET /api/admin/profile/me/
Authorization: Bearer {admin_token}

Response 200:
{
    "utente": {
        "id": 1,
        "username": "admin1",
        "nome": "Admin",
        "cognome": "Uno",
        "ruolo": "admin"
    }
}
```

---

### Registro Endpoints (CRUD Completo)

**Permessi**: 
- **GET**: Admin o Partecipante (solo propri dati)
- **POST/PUT/DELETE**: Solo Admin

#### Lista Registri
```http
GET /api/registro/
Authorization: Bearer {token}

# Query params opzionali:
# ?partecipante=1
# ?data_inizio=2026-01-01
# ?data_fine=2026-01-31

Response 200:
[
    {
        "id": 1,
        "partecipante": 2,
        "partecipante_nome": "Mario",
        "partecipante_cognome": "Rossi",
        "data": "2026-01-30",
        "ore_totali": "8.00",
        "assenze": "1.00",
        "ore_presenti": 7.00,
        "percentuale_presenza": 87.50,
        "note": "Ritardo mattutino",
        "created_at": "2026-01-30T10:00:00Z"
    },
    ...
]
```

#### Crea Registro (Solo Admin)
```http
POST /api/registro/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
    "partecipante": 2,
    "data": "2026-01-30",
    "ore_totali": "8.00",
    "assenze": "1.00"
}

Response 201:
{
    "id": 41,
    "partecipante": 2,
    "data": "2026-01-30",
    "ore_totali": "8.00",
    "assenze": "1.00",
    ...
}
```

#### Aggiorna Registro (Solo Admin)
```http
PUT /api/registro/1/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
    "partecipante": 2,
    "data": "2026-01-30",
    "ore_totali": "8.00",
    "assenze": "2.00"
}

Response 200: {...}
```

#### Elimina Registro (Solo Admin)
```http
DELETE /api/registro/1/
Authorization: Bearer {admin_token}

Response 204: No Content
```

#### Statistiche Aggregate (Solo Admin)
```http
GET /api/registro/summary/
Authorization: Bearer {admin_token}

Response 200:
{
    "totale_record": 40,
    "totale_ore": "320.00",
    "totale_assenze": "32.00",
    "ore_presenti": "288.00",
    "percentuale_presenza_media": 90.00
}
```

---

## 🧪 Testing

### Test con cURL

#### 1. Login Admin
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin1", "password": "admin123"}'
```

#### 2. Login Partecipante
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "part1", "password": "part123"}'
```

#### 3. Vedere Registri (con token)
```bash
curl -X GET http://localhost:8000/api/registro/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4. Creare Registro (Admin)
```bash
curl -X POST http://localhost:8000/api/registro/ \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "partecipante": 3,
    "data": "2026-01-30",
    "ore_totali": "8.00",
    "assenze": "0.00"
  }'
```

### Test con Postman

**Collection Structure:**
```
Gestione Presenze API/
├── Auth/
│   ├── Login Admin
│   ├── Login Partecipante
│   └── Refresh Token
├── Partecipante/
│   ├── Get Profile
│   ├── Get Stats
│   └── Get Presenze
└── Admin/
    ├── List Partecipanti
    ├── Get Registro
    ├── Create Registro
    ├── Update Registro
    └── Delete Registro
```

**Environment Variables:**
- `base_url`: `http://localhost:8000`
- `admin_token`: (da popolare dopo login)
- `user_token`: (da popolare dopo login)

---

## 🔑 Credenziali di Accesso

### Admin
```
Username: admin1
Password: admin123
Email: admin1@example.com

Username: admin2
Password: admin123
Email: admin2@example.com
```

### Partecipanti
```
Username: part1
Password: part123
Email: part1@example.com

Username: part2
Password: part123
Email: part2@example.com

Username: part3
Password: part123
Email: part3@example.com

Username: part4
Password: part123
Email: part4@example.com
```

---

## 📊 Dati di Test

Il database viene popolato con:
- **2 Admin**
- **4 Partecipanti**
- **40 Record Registro** (10 giorni × 4 partecipanti)

### Ripopolare Database
```bash
# Pulire e ripopolare
python populate_db.py
# Rispondere 's' quando chiede se pulire il database
```

---

## 🐛 Troubleshooting

### Server non si avvia
```bash
# Verifica virtual environment attivo
which python  # Dovrebbe mostrare path con venv

# Verifica dipendenze
pip list | grep Django
```

### Errore "table does not exist"
```bash
# Riapplica migrazioni
python manage.py migrate
```

### Token JWT non funziona
```bash
# Verifica che il token sia nel formato corretto
# Header: Authorization: Bearer {token}
# NON: Authorization: JWT {token}
```

### Errore 403 Forbidden
- Verifica che l'utente abbia il ruolo corretto
- Admin endpoints richiedono `ruolo='admin'`
- Partecipante endpoints richiedono `ruolo='partecipante'`

---

## 📝 Note Importanti

### Modifiche Recenti (30/01/2026)
1. ✅ **Rinominato** `affluenza` → `registro`
2. ✅ **Spostato** modello `Utente` da app `utente` a app `partecipante`
3. ✅ **Eliminata** app `utente` completamente
4. ✅ **Aggiornato** `AUTH_USER_MODEL = 'partecipante.Utente'`

### Struttura App
- **partecipante**: Contiene sia `Utente` che `Partecipante`
- **admin_profile**: Contiene solo `Admin`
- **registro**: Contiene solo `Registro` (ex Affluenza)

### Convenzioni Naming
- Modelli: PascalCase (es. `Registro`, `Partecipante`)
- URL endpoints: lowercase con trattini (es. `api/registro/`)
- File: snake_case (es. `models.py`, `serializers.py`)

---

## 🎯 Prossimi Passi (Opzionali)

- [ ] Aggiungere paginazione ai risultati API
- [ ] Implementare filtri avanzati per data
- [ ] Export dati in CSV/Excel
- [ ] Dashboard statistiche admin
- [ ] Email notifiche per assenze
- [ ] Frontend con React/Vue
- [ ] Deploy su server di produzione

---

## 📚 Risorse

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [SQLite Browser](https://sqlitebrowser.org/)

---

**Progetto Completato e Funzionante! 🎉**

Per domande o supporto, consultare la documentazione o i file di walkthrough nella directory `brain/`.
