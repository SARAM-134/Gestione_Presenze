# 🚀 GUIDA RAPIDA - COMPLETARE IL PROGETTO

## 📍 STATO ATTUALE

### ✅ GIÀ FATTO:
- Tutti i **models.py** (Utente, AdminProfile, Partecipante, Affluenza)
- Tutti gli **admin.py** (configurazione Django admin)
- Migrations applicate
- Database SQLite creato
- Tutte le **views.py** esistono

### ❌ MANCA:
- **serializers.py** per tutte le app
- **urls.py** per admin_profile, partecipante, affluenza
- **permissions.py** per affluenza
- **populate_db.py** nella root del progetto

---

## 🎯 COSA FARE ORA - PASSO PER PASSO

### STEP 1: Copiare i file che ti ho creato

Ho creato 7 file pronti da copiare. Devi copiarli nel progetto così:

```bash
# DALLA DIRECTORY DEL TUO PROGETTO:

# 1. utente/serializers.py
cp utente_serializers.py ~/Gestione_Presenze/utente/serializers.py

# 2. admin_profile/serializers.py
cp admin_profile_serializers.py ~/Gestione_Presenze/admin_profile/serializers.py

# 3. admin_profile/urls.py
cp admin_profile_urls.py ~/Gestione_Presenze/admin_profile/urls.py

# 4. partecipante/serializers.py
cp partecipante_serializers.py ~/Gestione_Presenze/partecipante/serializers.py

# 5. partecipante/urls.py
cp partecipante_urls.py ~/Gestione_Presenze/partecipante/urls.py

# 6. affluenza/permissions.py
cp affluenza_permissions.py ~/Gestione_Presenze/affluenza/permissions.py

# 7. affluenza/serializers.py
cp affluenza_serializers.py ~/Gestione_Presenze/affluenza/serializers.py

# 8. affluenza/urls.py
cp affluenza_urls.py ~/Gestione_Presenze/affluenza/urls.py
```

**OPPURE** apri ogni file che ti ho dato e copia-incolla manualmente il contenuto.

---

### STEP 2: Creare populate_db.py

Nella **ROOT** del progetto (dove c'è manage.py), crea il file `populate_db.py`:

```bash
# Copia il file populate_db.py che ti ho dato nella root
cp populate_db.py ~/Gestione_Presenze/populate_db.py
```

---

### STEP 3: Verificare gestione_presenze/urls.py

Apri `gestione_presenze/urls.py` e verifica che ci sia questo:

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App URLs
    path('api/partecipante/', include('partecipante.urls')),
    path('api/admin/', include('admin_profile.urls')),
    path('api/affluenza/', include('affluenza.urls')),
]
```

---

### STEP 4: Testare il progetto

```bash
# 1. Attiva virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Popola database
python populate_db.py

# 3. Avvia server
python manage.py runserver

# 4. Testa login in un altro terminale
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin1",
    "password": "admin123"
  }'
```

Se vedi un JSON con "access" e "refresh" token → **FUNZIONA! ✅**

---

## 📋 CHECKLIST COMPLETA

Prima di considerare il progetto finito:

### File Creati:
- [ ] utente/serializers.py
- [ ] admin_profile/serializers.py
- [ ] admin_profile/urls.py
- [ ] partecipante/serializers.py
- [ ] partecipante/urls.py
- [ ] affluenza/serializers.py
- [ ] affluenza/permissions.py
- [ ] affluenza/urls.py
- [ ] populate_db.py (root)

### Test Funzionalità:
- [ ] Login admin funziona
- [ ] Login partecipante funziona
- [ ] populate_db.py crea utenti
- [ ] Django admin accessibile
- [ ] API restituiscono dati

---

## 🔧 SE QUALCOSA NON FUNZIONA

### Errore: "No module named 'rest_framework'"
```bash
pip install djangorestframework djangorestframework-simplejwt
```

### Errore: "table affluenza_affluenza doesn't exist"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Errore: ImportError nei serializers
Verifica che tutti i file serializers.py siano creati correttamente.

---

## 💬 PER LE TUE COLLEGHE

Quando arrivano, possono:

1. **Testare le API** con la guida in `API_TESTING_GUIDE.md`
2. **Modificare il flusso di registrazione** (come da diagrammi):
   - Modificare `utente/serializers.py` (UtenteCreateSerializer)
   - Creare view custom per registrazione
   - Aggiungere logica matricola
3. **Aggiungere funzionalità** secondo `DIVISIONE_LAVORO_3_PERSONE.md`

---

## 🎯 PRIORITÀ IMMEDIATE

1. **ADESSO**: Copia i file che ti ho creato
2. **POI**: Testa con populate_db.py
3. **INFINE**: Verifica API con curl o Postman

---

**Hai tutti i file pronti! Basta copiarli e testare! 🚀**

Se hai problemi con qualche file specifico, dimmi quale e te lo spiego meglio!
