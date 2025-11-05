#!/usr/bin/env python
"""
Script rapide pour corriger les retards d'aujourd'hui
"""
import os
import sys
import django
from datetime import datetime, timedelta, date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage, PointageSettings

print("🔧 CORRECTION RAPIDE DES RETARDS")

# Récupérer les paramètres
settings = PointageSettings.objects.first()
print(f"Heure attendue: {settings.expected_arrival_time}")
print(f"Tolérance: {settings.tolerance_minutes} min")

# Date d'aujourd'hui
today = date.today()
print(f"Date: {today}")

# Trouver tous les pointages d'aujourd'hui sans statut
pointages = Pointage.objects.filter(date=today, arrival_time__isnull=False)
print(f"Pointages trouvés: {pointages.count()}")

for p in pointages:
    print(f"\n👤 {p.employee.first_name} {p.employee.last_name}")
    print(f"   Arrivée: {p.arrival_time}")
    print(f"   Statut actuel: {p.arrival_status}")
    
    # Calculer si c'est en retard
    tolerance_time = (
        datetime.combine(today, settings.expected_arrival_time) + 
        timedelta(minutes=settings.tolerance_minutes)
    ).time()
    
    if p.arrival_time > tolerance_time:
        # C'est un retard
        expected = datetime.combine(today, settings.expected_arrival_time)
        actual = datetime.combine(today, p.arrival_time)
        late_minutes = int((actual - expected).total_seconds() / 60)
        
        p.arrival_status = Pointage.STATUS_LATE
        p.late_minutes = late_minutes
        p.save()
        
        print(f"   ✅ CORRIGÉ: RETARD de {late_minutes} minutes")
    else:
        p.arrival_status = Pointage.STATUS_ON_TIME
        p.save()
        print(f"   ✅ CORRIGÉ: À L'HEURE")

# Vérifier les retards
retards = Pointage.objects.filter(date=today, arrival_status=Pointage.STATUS_LATE)
print(f"\n📊 RÉSULTAT: {retards.count()} retard(s) aujourd'hui")

for r in retards:
    print(f"   • {r.employee.first_name} {r.employee.last_name}: {r.late_minutes} min")

print("\n🎉 TERMINÉ ! Rafraîchissez le dashboard admin.")
