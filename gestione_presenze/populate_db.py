#!/usr/bin/env python
"""
Script per popolare il database con dati di test
Eseguire con: python populate_db.py
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestione_presenze.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from utente.models import Utente
from admin_profile.models import Admin
from partecipante.models import Partecipante
from affluenza.models import Affluenza


def clear_database():
    """Pulisce il database (opzionale)"""
    print("🗑️  Pulizia database...")
    Affluenza.objects.all().delete()
    Partecipante.objects.all().delete()
    Admin.objects.all().delete()
    Utente.objects.all().delete()
    print("✅ Database pulito")


def create_admins():
    """Crea utenti admin"""
    print("\n👤 Creazione Admin...")
    
    admins_data = [
        {
            'username': 'admin1',
            'email': 'admin1@example.com',
            'nome': 'Mario',
            'cognome': 'Rossi',
            'password': 'admin123',
            'ruolo': 'admin'
        },
        {
            'username': 'admin2',
            'email': 'admin2@example.com',
            'nome': 'Laura',
            'cognome': 'Bianchi',
            'password': 'admin123',
            'ruolo': 'admin'
        }
    ]
    
    created_admins = []
    for data in admins_data:
        password = data.pop('password')
        utente = Utente.objects.create(**data)
        utente.set_password(password)
        utente.save()
        
        # Crea profilo admin
        admin_profile = Admin.objects.create(
            utente=utente,
            area_riservata_accesso=True
        )
        created_admins.append(admin_profile)
        print(f"  ✅ Admin creato: {utente.username} (password: admin123)")
    
    return created_admins


def create_partecipanti():
    """Crea utenti partecipanti"""
    print("\n👥 Creazione Partecipanti...")
    
    partecipanti_data = [
        {
            'username': 'part1',
            'email': 'part1@example.com',
            'nome': 'Giovanni',
            'cognome': 'Verdi',
            'password': 'part123',
            'ruolo': 'partecipante'
        },
        {
            'username': 'part2',
            'email': 'part2@example.com',
            'nome': 'Anna',
            'cognome': 'Neri',
            'password': 'part123',
            'ruolo': 'partecipante'
        },
        {
            'username': 'part3',
            'email': 'part3@example.com',
            'nome': 'Luca',
            'cognome': 'Gialli',
            'password': 'part123',
            'ruolo': 'partecipante'
        },
        {
            'username': 'part4',
            'email': 'part4@example.com',
            'nome': 'Sofia',
            'cognome': 'Blu',
            'password': 'part123',
            'ruolo': 'partecipante'
        }
    ]
    
    created_partecipanti = []
    for data in partecipanti_data:
        password = data.pop('password')
        utente = Utente.objects.create(**data)
        utente.set_password(password)
        utente.save()
        
        # Crea profilo partecipante
        partecipante = Partecipante.objects.create(
            utente=utente,
            attivo=True,
            profilo=f"Partecipante al corso - {utente.nome} {utente.cognome}"
        )
        created_partecipanti.append(partecipante)
        print(f"  ✅ Partecipante creato: {utente.username} (password: part123)")
    
    return created_partecipanti


def create_affluenze(partecipanti, admins):
    """Crea record di affluenza per i partecipanti"""
    print("\n📊 Creazione record affluenza...")
    
    if not admins:
        print("  ⚠️  Nessun admin disponibile, skip creazione affluenze")
        return
    
    admin = admins[0]  # Usa il primo admin come creatore
    oggi = date.today()
    
    # Crea affluenze per gli ultimi 10 giorni
    for i in range(10):
        data_affluenza = oggi - timedelta(days=i)
        
        for partecipante in partecipanti:
            # Varia le ore e le assenze in modo casuale
            import random
            ore_totali = Decimal('8.00')
            assenze = Decimal(str(random.choice([0.0, 0.5, 1.0, 2.0])))
            
            try:
                affluenza = Affluenza.objects.create(
                    partecipante=partecipante,
                    data=data_affluenza,
                    ore_totali=ore_totali,
                    assenze=assenze,
                    created_by=admin,
                    note=f"Record automatico per {data_affluenza}"
                )
                print(f"  ✅ Affluenza: {partecipante.utente.cognome} - {data_affluenza} (presenti: {affluenza.ore_presenti()}h)")
            except Exception as e:
                print(f"  ⚠️  Errore creazione affluenza: {e}")


def print_summary():
    """Stampa riepilogo dati creati"""
    print("\n" + "="*60)
    print("📋 RIEPILOGO DATABASE")
    print("="*60)
    
    print(f"\n👤 Admin: {Admin.objects.count()}")
    for admin in Admin.objects.all():
        print(f"   - {admin.utente.username} ({admin.utente.email})")
    
    print(f"\n👥 Partecipanti: {Partecipante.objects.count()}")
    for part in Partecipante.objects.all():
        percentuale = part.calcola_percentuale_presenza()
        print(f"   - {part.utente.username} ({part.utente.email}) - Presenza: {percentuale}%")
    
    print(f"\n📊 Record Affluenza: {Affluenza.objects.count()}")
    
    print("\n" + "="*60)
    print("🔑 CREDENZIALI DI ACCESSO")
    print("="*60)
    print("\nAdmin:")
    print("  Username: admin1 | Password: admin123")
    print("  Username: admin2 | Password: admin123")
    print("\nPartecipanti:")
    print("  Username: part1 | Password: part123")
    print("  Username: part2 | Password: part123")
    print("  Username: part3 | Password: part123")
    print("  Username: part4 | Password: part123")
    print("\n" + "="*60)


def main():
    """Funzione principale"""
    print("\n" + "="*60)
    print("🚀 POPOLAMENTO DATABASE - GESTIONE PRESENZE")
    print("="*60)
    
    # Chiedi conferma
    risposta = input("\n⚠️  Vuoi pulire il database prima di popolare? (s/n): ")
    if risposta.lower() == 's':
        clear_database()
    
    # Crea dati
    admins = create_admins()
    partecipanti = create_partecipanti()
    create_affluenze(partecipanti, admins)
    
    # Stampa riepilogo
    print_summary()
    
    print("\n✅ Popolamento completato con successo!")
    print("\n💡 Puoi ora avviare il server con: python manage.py runserver")
    print("💡 E testare il login con: curl -X POST http://localhost:8000/api/auth/login/ \\")
    print("     -H \"Content-Type: application/json\" \\")
    print("     -d '{\"username\": \"admin1\", \"password\": \"admin123\"}'")
    print()


if __name__ == '__main__':
    main()
