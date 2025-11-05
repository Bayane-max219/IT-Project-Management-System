#!/usr/bin/env python
"""
Script pour déboguer les raisons de retard manquantes
"""
import os
import sys
import django
from datetime import date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage

print("\n" + "="*80)
print("  DEBUG RAISONS DE RETARD")
print("="*80)

today = date.today()
print(f"📅 Date: {today}")

# Récupérer tous les pointages en retard d'aujourd'hui
retards_today = Pointage.objects.filter(
    date=today, 
    arrival_status=Pointage.STATUS_LATE
)

print(f"\n📊 Pointages en retard aujourd'hui: {retards_today.count()}")

if not retards_today.exists():
    print("❌ Aucun retard trouvé aujourd'hui")
    
    # Vérifier tous les pointages d'aujourd'hui
    all_today = Pointage.objects.filter(date=today)
    print(f"\n📋 Tous les pointages d'aujourd'hui: {all_today.count()}")
    
    for p in all_today:
        print(f"   • {p.employee.first_name} {p.employee.last_name}")
        print(f"     Arrivée: {p.arrival_time}")
        print(f"     Statut: {p.arrival_status}")
        print(f"     Retard minutes: {p.late_minutes}")
        print(f"     Raison: {p.late_reason or 'AUCUNE'}")
        print("-" * 40)
else:
    print(f"\n📋 DÉTAILS DES RETARDS:")
    for p in retards_today:
        print(f"\n👤 {p.employee.first_name} {p.employee.last_name}")
        print(f"   📅 Date: {p.date}")
        print(f"   ⏰ Arrivée: {p.arrival_time}")
        print(f"   📊 Statut: {p.arrival_status}")
        print(f"   ⏱️  Minutes de retard: {p.late_minutes}")
        print(f"   📝 Raison: '{p.late_reason}' ({type(p.late_reason)})")
        print(f"   ✅ Justifié: {p.is_justified}")
        print(f"   ✔️  Approuvé: {p.justification_approved}")
        
        # Vérifier si la raison est vide
        if not p.late_reason:
            print(f"   ❌ PROBLÈME: Raison manquante !")
        else:
            print(f"   ✅ Raison présente: '{p.late_reason}'")
        
        print("-" * 60)

print(f"\n🔧 SOLUTION:")
print("Si les raisons sont manquantes, c'est que:")
print("1. Les pointages ont été créés avant la correction")
print("2. Les développeurs n'ont pas fourni de raison")
print("3. Il y a un bug dans la sauvegarde des raisons")

print(f"\n💡 POUR CORRIGER:")
print("1. Demander aux développeurs de pointer à nouveau")
print("2. Ou ajouter manuellement les raisons manquantes")
print("3. Ou utiliser le script de correction")

# Proposer une correction automatique
print(f"\n🛠️  CORRECTION AUTOMATIQUE:")
for p in retards_today:
    if not p.late_reason:
        raison_auto = f"Retard de {p.late_minutes} minutes - Raison non spécifiée"
        print(f"   Proposer pour {p.employee.first_name}: '{raison_auto}'")

print(f"\nExécutez 'python corriger_raisons_manquantes.py' pour appliquer les corrections")
