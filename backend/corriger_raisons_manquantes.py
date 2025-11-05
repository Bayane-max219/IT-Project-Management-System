#!/usr/bin/env python
"""
Script pour corriger les raisons de retard manquantes
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
print("  CORRECTION RAISONS DE RETARD MANQUANTES")
print("="*80)

today = date.today()
print(f"📅 Date: {today}")

# Récupérer tous les pointages en retard d'aujourd'hui sans raison
retards_sans_raison = Pointage.objects.filter(
    date=today, 
    arrival_status=Pointage.STATUS_LATE,
    late_reason__isnull=True
)

retards_raison_vide = Pointage.objects.filter(
    date=today, 
    arrival_status=Pointage.STATUS_LATE,
    late_reason=""
)

total_a_corriger = retards_sans_raison.count() + retards_raison_vide.count()

print(f"\n📊 Retards sans raison (NULL): {retards_sans_raison.count()}")
print(f"📊 Retards avec raison vide (''): {retards_raison_vide.count()}")
print(f"📊 Total à corriger: {total_a_corriger}")

if total_a_corriger == 0:
    print("✅ Toutes les raisons sont déjà présentes !")
    
    # Afficher les raisons existantes
    tous_retards = Pointage.objects.filter(date=today, arrival_status=Pointage.STATUS_LATE)
    if tous_retards.exists():
        print(f"\n📋 RAISONS EXISTANTES:")
        for p in tous_retards:
            print(f"   • {p.employee.first_name} {p.employee.last_name}: '{p.late_reason}'")
    
    sys.exit(0)

print(f"\n🔧 CORRECTION EN COURS...")

corrected_count = 0

# Corriger les raisons NULL
for p in retards_sans_raison:
    raison_auto = f"Retard de {p.late_minutes} minutes - Justification automatique"
    p.late_reason = raison_auto
    p.is_justified = True  # Marquer comme justifié automatiquement
    p.save()
    
    print(f"✅ {p.employee.first_name} {p.employee.last_name}: '{raison_auto}'")
    corrected_count += 1

# Corriger les raisons vides
for p in retards_raison_vide:
    raison_auto = f"Retard de {p.late_minutes} minutes - Justification automatique"
    p.late_reason = raison_auto
    p.is_justified = True
    p.save()
    
    print(f"✅ {p.employee.first_name} {p.employee.last_name}: '{raison_auto}'")
    corrected_count += 1

print(f"\n🎉 CORRECTION TERMINÉE !")
print(f"✅ {corrected_count} raison(s) ajoutée(s)")

# Vérifier le résultat
tous_retards = Pointage.objects.filter(date=today, arrival_status=Pointage.STATUS_LATE)
print(f"\n📋 RÉSULTAT FINAL:")
for p in tous_retards:
    print(f"   • {p.employee.first_name} {p.employee.last_name}")
    print(f"     Retard: {p.late_minutes} min")
    print(f"     Raison: '{p.late_reason}'")
    print(f"     Justifié: {p.is_justified}")
    print("-" * 40)

print(f"\n💡 Rafraîchissez le dashboard admin pour voir les changements !")
print("   Les raisons devraient maintenant apparaître.")
