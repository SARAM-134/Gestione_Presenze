# 🚀 Quick Start Guide - Setup Immediato

## ⏱️ Setup Veloce (15 minuti)

### Step 1: Setup Iniziale (Tutti insieme - 5 min)

```bash
# 1. Creare directory progetto
mkdir attendance_project
cd attendance_project

# 2. Creare virtual environment
python -m venv venv

# 3. Attivare virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Creare requirements.txt
echo "Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0" > requirements.txt

# 5. Installare dependencies
pip install -r requirements.txt

# 6. Inizializzare Git
git init
git add .
git commit -m "Initial setup"
```

### Step 2: Creare Progetto Django (Persona 1 - 5 min)

```bash
# Creare progetto
django-admin startproject config .

# Creare app core
python manage.py startapp core

# Struttura creata:
# attendance_project/
# ├── manage.py
# ├── config/
# │   ├── settings.py
# │   ├── urls.py
# └── core/
#     ├── models.py
#     ├── views.py
#     └── ...
```

### Step 3: Configurazione Base (Persona 1 - 5 min)

**config/settings.py** - Aggiungere:

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
    'core',
]

AUTH_USER_MODEL = 'core.Utente'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

---

## 📋 Checklist Distribuzione Lavoro

### ✅ PERSONA 1 - Backend Foundation
**File da creare/modificare:**
- [ ] `core/models.py` (copiare da technical_implementation.md)
- [ ] `core/admin.py` (copiare da technical_implementation.md)
- [ ] Eseguire migrations:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
- [ ] Testare Django admin: `python manage.py runserver`

### ✅ PERSONA 2 - API & Auth
**File da creare:**
- [ ] `core/serializers.py` (copiare da technical_implementation.md)
- [ ] `core/permissions.py` (copiare da technical_implementation.md)
- [ ] `core/views.py` - Solo PartecipanteViewSet
- [ ] `core/urls.py` (versione base con auth)
- [ ] Testare con Postman login endpoint

### ✅ PERSONA 3 - Admin Features
**File da creare/modificare:**
- [ ] `core/views.py` - Aggiungere AdminViewSet e AffluenzaViewSet
- [ ] `core/urls.py` - Aggiungere router completo
- [ ] `config/urls.py` - Include core.urls
- [ ] `populate_db.py` - Script popolazione database
- [ ] Testare tutti gli endpoints

---

## 🔥 Comandi Essenziali per Testing

### Test 1: Verificare Server Funzionante
```bash
python manage.py runserver
# Aprire: http://localhost:8000/admin/
```

### Test 2: Creare Dati di Test via Django Shell
```bash
python manage.py shell
```

```python
from core.models import Utente, Partecipante, Admin
from datetime import date
from decimal import Decimal

# Creare admin
admin_user = Utente.objects.create_user(
    username='admin',
    password='admin123',
    nome='Admin',
    cognome='Test',
    ruolo='admin'
)
Admin.objects.create(utente=admin_user)

# Creare partecipante
part_user = Utente.objects.create_user(
    username='mario.rossi',
    password='pass123',
    nome='Mario',
    cognome='Rossi',
    ruolo='partecipante'
)
part = Partecipante.objects.create(utente=part_user)

print("✅ Utenti creati!")
```

### Test 3: API Testing con cURL

**1. Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"mario.rossi","password":"pass123"}'
```

**2. Vedere presenze (con token):**
```bash
curl -X GET http://localhost:8000/api/partecipante/presenze/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**3. Admin crea affluenza:**
```bash
curl -X POST http://localhost:8000/api/affluenza/ \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "partecipante": 1,
    "data": "2026-01-28",
    "ore_totali": "8.00",
    "assenze": "0.00"
  }'
```

---

## 🐛 Troubleshooting Veloce

### Problema: ImportError o ModuleNotFoundError
```bash
# Verificare virtual environment attivo
which python  # Dovrebbe mostrare path con venv

# Reinstallare requirements
pip install -r requirements.txt
```

### Problema: Migrations error
```bash
# Cancellare migrations e database
rm -rf core/migrations/
rm db.sqlite3

# Ricreare tutto
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
```

### Problema: CORS errors (se testate da frontend)
```bash
pip install django-cors-headers
```

Aggiungere in settings.py:
```python
INSTALLED_APPS = [
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOW_ALL_ORIGINS = True  # Solo per sviluppo!
```

---

## 📊 Endpoint API Completi

### Authentication
```
POST   /api/auth/login/          - Login (username, password)
POST   /api/auth/refresh/        - Refresh token
```

### Partecipante (require auth + ruolo partecipante)
```
GET    /api/partecipante/presenze/        - Proprie presenze
GET    /api/partecipante/stats/           - Proprie statistiche
PUT    /api/partecipante/profilo/         - Aggiorna profilo
```

### Admin (require auth + ruolo admin)
```
GET    /api/admin/partecipanti/                        - Lista partecipanti
GET    /api/admin/partecipante-presenze/?partecipante_id=X  - Presenze partecipante

POST   /api/affluenza/                     - Crea affluenza
GET    /api/affluenza/                     - Lista affluenze
GET    /api/affluenza/{id}/                - Dettaglio affluenza
PUT    /api/affluenza/{id}/                - Aggiorna affluenza
DELETE /api/affluenza/{id}/                - Elimina affluenza
```

---

## 🎯 Demo Finale - Scenario di Test

### Preparazione Dati:
1. 2 Admin accounts
2. 5 Partecipanti
3. 20-30 record affluenza ultimi 20 giorni

### Demo Flow:

**1. Login come Admin**
```json
POST /api/auth/login/
{
    "username": "admin",
    "password": "admin123"
}
```

**2. Vedere lista partecipanti**
```
GET /api/admin/partecipanti/
```

**3. Creare affluenza per Mario Rossi**
```json
POST /api/affluenza/
{
    "partecipante": 2,
    "data": "2026-01-28",
    "ore_totali": "8.00",
    "assenze": "1.00",
    "note": "Ritardo mattutino"
}
```

**4. Login come Partecipante Mario**
```json
POST /api/auth/login/
{
    "username": "mario.rossi",
    "password": "pass123"
}
```

**5. Vedere proprie presenze e stats**
```
GET /api/partecipante/presenze/
GET /api/partecipante/stats/
```

---

## 📱 Postman Collection Template

Creare collection "Attendance API" con:

```
Attendance API/
├── Auth/
│   ├── Login Admin
│   ├── Login Partecipante
│   └── Refresh Token
├── Partecipante/
│   ├── Get Presenze
│   ├── Get Stats
│   └── Update Profilo
└── Admin/
    ├── List Partecipanti
    ├── Get Partecipante Presenze
    ├── Create Affluenza
    ├── Update Affluenza
    └── Delete Affluenza
```

**Environment Variables:**
- `base_url`: http://localhost:8000
- `admin_token`: (da popolare dopo login)
- `user_token`: (da popolare dopo login)

---

## ⏰ Timeline Realistica

### Giorno 1 - Mattina (9:00-13:00)
- **9:00-9:30**: Setup tutti insieme, Git init
- **9:30-11:00**: 
  - P1: Models + migrations
  - P2: Serializers + permissions
  - P3: URLs structure planning
- **11:00-13:00**: 
  - P1: Admin config + testing
  - P2: Auth endpoints + testing
  - P3: Admin views (inizio)

### Giorno 1 - Pomeriggio (14:00-18:00)
- **14:00-16:00**:
  - P1: Supporto + documentation
  - P2: Partecipante viewset
  - P3: Admin viewset complete
- **16:00-18:00**:
  - Tutti: Prima integration, fix bugs
  - Testing endpoints base

### Giorno 2 - Mattina (9:00-13:00)
- **9:00-11:00**:
  - P1: Script popolazione DB
  - P2: Stats calculations
  - P3: Business logic validations
- **11:00-13:00**:
  - Tutti: Integration testing completo

### Giorno 2 - Pomeriggio (14:00-17:00)
- **14:00-15:30**: Final testing, bug fixes
- **15:30-17:00**: Preparazione demo, documentazione

---

## ✨ Tips per Successo

1. **Comunicare ogni 30 min** su cosa state facendo
2. **Commit frequenti** con messaggi chiari
3. **Testare subito** ogni endpoint creato
4. **Non aggiungere features** se base non funziona
5. **Chiedere aiuto** subito se bloccati

**Buon lavoro! 💪 Keep it simple, make it work! 🚀**
