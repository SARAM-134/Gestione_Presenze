# Progetto Gestione Presenze - Piano di Sviluppo

## 📋 Panoramica del Progetto

**Durata**: 2 giorni (oggi e domani pomeriggio)  
**Team**: 3 sviluppatori junior  
**Stack**: Python, Django, SQLite  
**Obiettivo**: Sistema backend per gestione presenze/assenze con due ruoli utente

---

## 🗄️ Schema Database

### Tabelle Principali

```sql
-- Tabella Utente (base per admin e partecipante)
utente
├── id (PK, AutoIncrement)
├── username (Unique, String)
├── email (String)
├── password (Hashed String)
├── nome (String)
├── cognome (String)
├── ruolo (Enum: 'admin', 'partecipante')
├── created_at (DateTime)
└── updated_at (DateTime)

-- Tabella Partecipante (estende utente)
partecipante
├── id (PK, FK -> utente.id)
├── profilo (Text, nullable) -- per funzionalità opzionali
└── attivo (Boolean, default=True)

-- Tabella Admin (estende utente)
admin
├── id (PK, FK -> utente.id)
└── area_riservata_accesso (Boolean, default=True)

-- Tabella Affluenza (presenze/assenze)
affluenza
├── id (PK, AutoIncrement)
├── partecipante_id (FK -> partecipante.id)
├── data (Date)
├── ore_totali (Decimal)
├── assenze (Decimal, default=0)
├── note (Text, nullable)
├── created_by (FK -> admin.id, nullable)
└── created_at (DateTime)
```

---

## 🏗️ Architettura Django

### Struttura del Progetto

```
attendance_project/
├── manage.py
├── attendance_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── __init__.py
│   ├── models.py          # Modelli: Utente, Partecipante, Admin, Affluenza
│   ├── views.py           # API Views
│   ├── serializers.py     # Django REST Framework serializers
│   ├── permissions.py     # Custom permissions
│   ├── urls.py            # URL routing
│   └── admin.py           # Django admin configuration
├── requirements.txt
└── README.md
```

---

## 👥 Divisione del Lavoro (3 Persone)

### **PERSONA 1 - Backend Foundation & Models** 
**Tempo stimato: 6-8 ore**

#### Responsabilità:
1. **Setup iniziale del progetto**
   - Creare progetto Django
   - Configurare settings.py (database SQLite, installed apps)
   - Setup virtual environment
   - Creare requirements.txt

2. **Modelli Django (models.py)**
   - Model `Utente` con User authentication Django
   - Model `Partecipante` (OneToOne con User)
   - Model `Admin` (OneToOne con User)
   - Model `Affluenza`
   - Implementare `__str__` methods
   - Creare migrations e migrare database

3. **Django Admin Configuration**
   - Registrare tutti i modelli
   - Customizzare admin interface per gestione facile

#### Deliverables:
- [ ] Progetto Django funzionante
- [ ] Database con tutte le tabelle
- [ ] Django admin accessibile
- [ ] File requirements.txt
- [ ] README con istruzioni setup

---

### **PERSONA 2 - API & Authentication**
**Tempo stimato: 6-8 ore**

#### Responsabilità:
1. **Sistema di Autenticazione**
   - Login/Logout endpoints
   - Token-based authentication (Django REST Framework Token o JWT)
   - Permission classes per Admin/Partecipante

2. **API Endpoints per Partecipante**
   ```
   GET  /api/partecipante/presenze/        # Visualizza proprie presenze
   GET  /api/partecipante/stats/           # Percentuale presenza
   PUT  /api/partecipante/profilo/         # Aggiorna profilo (opzionale)
   ```

3. **Serializers**
   - UtentSerializer
   - PartecipanteSerializer
   - AffluenzaSerializer (con calcolo percentuali)

#### Deliverables:
- [ ] Sistema login/logout funzionante
- [ ] API per visualizzazione presenze partecipante
- [ ] Calcolo automatico percentuale presenza
- [ ] Documentazione API (può essere semplice README)

---

### **PERSONA 3 - Admin Features & Business Logic**
**Tempo stimato: 6-8 ore**

#### Responsabilità:
1. **API Endpoints per Admin**
   ```
   GET    /api/admin/partecipanti/              # Lista tutti partecipanti
   POST   /api/admin/affluenza/                 # Aggiungi presenza/assenza
   PUT    /api/admin/affluenza/<id>/            # Modifica presenza/assenza
   DELETE /api/admin/affluenza/<id>/            # Cancella record
   GET    /api/admin/partecipante/<id>/presenze/ # Presenze di un partecipante
   ```

2. **Business Logic**
   - Validazione: non permettere presenze future
   - Validazione: ore totali e assenze logiche
   - Collegamento affluenza con admin che l'ha creata
   - Calcolo automatico percentuali

3. **Testing & Integration**
   - Testare tutti gli endpoint con tool come Postman
   - Gestione errori e validazioni
   - Popolare database con dati di test

#### Deliverables:
- [ ] API admin complete e funzionanti
- [ ] Validazioni business logic
- [ ] Database popolato con dati di esempio
- [ ] Test documentati

---

## 📅 Timeline Suggerita (2 Giorni)

### **GIORNO 1 - Mattina (3-4 ore)**
- **Tutti insieme**: Brainstorming, setup repository Git, definire struttura
- **Persona 1**: Setup progetto + primi modelli
- **Persona 2**: Studio Django REST Framework + setup authentication
- **Persona 3**: Progettazione API endpoints + studio validazioni

### **GIORNO 1 - Pomeriggio (3-4 ore)**
- **Persona 1**: Completare modelli + migrations + admin
- **Persona 2**: Implementare authentication + primi endpoints partecipante
- **Persona 3**: Implementare primi endpoints admin

### **GIORNO 2 - Mattina (3-4 ore)**
- **Persona 1**: Supporto debugging + documentazione
- **Persona 2**: Completare API partecipante + calcolo stats
- **Persona 3**: Completare API admin + business logic

### **GIORNO 2 - Pomeriggio (2-3 ore)**
- **Tutti insieme**: Testing integrazione, fix bugs, preparazione demo
- Testing completo del sistema
- Popolamento database con dati realistici
- Preparazione presentazione/demo

---

## 🛠️ Setup Iniziale (Da fare SUBITO insieme)

### 1. Repository Git
```bash
# Persona 1 crea repository
git init
git add .
git commit -m "Initial commit"

# Creare branch per ogni persona
git branch backend-models
git branch api-auth
git branch admin-features
```

### 2. Virtual Environment e Dependencies
```bash
# Tutti
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate  # Windows

# Persona 1 crea requirements.txt
pip install django djangorestframework
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add requirements"
```

### 3. Creare Progetto Django
```bash
# Persona 1
django-admin startproject attendance_project
cd attendance_project
python manage.py startapp core
```

---

## 💡 Consigli Importanti per Junior Developers

### ✅ Best Practices

1. **Comunicazione Costante**
   - Usare Git con branch separati
   - Daily standup: 5-10 min mattina e pomeriggio
   - Messaggi chiari su cosa state facendo

2. **Git Workflow**
   ```bash
   # Ogni persona lavora sul proprio branch
   git checkout -b feature/mia-feature
   
   # Commit frequenti
   git add .
   git commit -m "Descrizione chiara di cosa ho fatto"
   
   # Merge regolare con main
   git checkout main
   git pull
   git checkout feature/mia-feature
   git merge main
   ```

3. **Testing Pratico**
   - Usare Postman o simili per testare API
   - Creare uno script Python per popolare database
   - Testare ogni endpoint appena implementato

4. **Documentazione Minima**
   - Ogni persona documenta i propri endpoints
   - Commentare codice complesso
   - README con istruzioni setup

### ⚠️ Problemi Comuni da Evitare

1. **Non Comunicare**: Rischio di fare lavoro duplicato
2. **Non Usare Git Correttamente**: Possibili conflitti catastrofici
3. **Non Testare Subito**: Bug scoperti troppo tardi
4. **Scope Creep**: Restare focalizzati sulle funzionalità base

### 🎯 Funzionalità Opzionali (Solo se avete tempo)

- [ ] Paginazione risultati API
- [ ] Filtri avanzati (per data, partecipante)
- [ ] Export dati in CSV
- [ ] Dashboard statistiche admin
- [ ] Email notifiche
- [ ] Frontend semplice con HTML/Bootstrap

---

## 📚 Risorse Utili

- Django Docs: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- SQLite Browser: https://sqlitebrowser.org/ (per vedere database)
- Postman: https://www.postman.com/ (per testare API)

---

## 🎓 Struttura Minima per Demo Finale

### Cosa Mostrare:
1. **Admin Login** → Creare affluenza per partecipante
2. **Partecipante Login** → Vedere proprie presenze e percentuale
3. **Admin** → Vedere lista partecipanti e modificare record
4. **Database** → Mostrare relazioni funzionanti

### Dati di Test da Preparare:
- 2 Admin
- 5-10 Partecipanti
- 20-30 record affluenza con date varie
- Alcuni partecipanti con >75% presenza, altri <75%

---

## ✅ Checklist Finale

### Giorno 1 EOD
- [ ] Progetto Django creato e funzionante
- [ ] Tutti i modelli implementati e migrati
- [ ] Authentication funzionante
- [ ] Almeno 2-3 endpoints testati

### Giorno 2 EOD
- [ ] Tutte le API funzionanti
- [ ] Business logic implementata
- [ ] Database popolato con dati test
- [ ] Demo preparata
- [ ] Codice su Git repository
- [ ] README completo

---

**Buon lavoro! 💪 Ricordate: meglio un MVP (Minimum Viable Product) funzionante che tante funzionalità incomplete!**
