#!/usr/bin/env python
"""
Script pour corriger les statuts des pointages existants
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage, PointageSettings

print("\n" + "="*80)
print("  CORRECTION DES STATUTS DE POINTAGE")
print("="*80)

# Récupérer les paramètres
try:
    settings = PointageSettings.objects.first()
    if not settings:
        print("❌ Aucun paramètre de pointage trouvé")
        sys.exit(1)
    
    print(f"✅ Paramètres trouvés:")
    print(f"   Heure arrivée attendue: {settings.expected_arrival_time}")
    print(f"   Tolérance: {settings.tolerance_minutes} minutes")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Récupérer tous les pointages sans statut
pointages_sans_statut = Pointage.objects.filter(arrival_status__isnull=True, arrival_time__isnull=False)

print(f"\n📋 Pointages à corriger: {pointages_sans_statut.count()}")

if not pointages_sans_statut.exists():
    print("✅ Tous les pointages ont déjà un statut")
    sys.exit(0)

corrected_count = 0

for pointage in pointages_sans_statut:
    print(f"\n🔧 Correction: {pointage.employee.first_name} {pointage.employee.last_name} - {pointage.date}")
    
    # Calculer les limites pour ce jour
    tolerance_time = (
        datetime.combine(pointage.date, settings.expected_arrival_time) + 
        timedelta(minutes=settings.tolerance_minutes)
    ).time()
    
    early_limit = (
        datetime.combine(pointage.date, settings.expected_arrival_time) - 
        timedelta(minutes=30)
    ).time()
    
    arrival_time = pointage.arrival_time
    
    # Définir le statut
    if arrival_time > tolerance_time:
        pointage.arrival_status = Pointage.STATUS_LATE
        # Calculer les minutes de retard
        expected_arrival = datetime.combine(pointage.date, settings.expected_arrival_time)
        actual_arrival = datetime.combine(pointage.date, arrival_time)
        late_minutes = int((actual_arrival - expected_arrival).total_seconds() / 60)
        pointage.late_minutes = late_minutes
        
        print(f"   ⏰ RETARD: {late_minutes} minutes")
        
    elif arrival_time < early_limit:
        pointage.arrival_status = Pointage.STATUS_EARLY
        # Calculer les minutes d'avance
        expected_arrival = datetime.combine(pointage.date, settings.expected_arrival_time)
        actual_arrival = datetime.combine(pointage.date, arrival_time)
        early_minutes = int((expected_arrival - actual_arrival).total_seconds() / 60)
        pointage.early_arrival_minutes = early_minutes
        
        print(f"   ⏰ AVANCE: {early_minutes} minutes")
        
    else:
        pointage.arrival_status = Pointage.STATUS_ON_TIME
        print(f"   ✅ À L'HEURE")
    
    # Sauvegarder
    pointage.save()
    corrected_count += 1

print(f"\n🎉 CORRECTION TERMINÉE !")
print(f"✅ {corrected_count} pointage(s) corrigé(s)")

# Vérifier les statistiques d'aujourd'hui
from datetime import date
today = date.today()
today_pointages = Pointage.objects.filter(date=today)
late_today = today_pointages.filter(arrival_status=Pointage.STATUS_LATE).count()

print(f"\n📊 STATISTIQUES D'AUJOURD'HUI:")
print(f"   Total pointages: {today_pointages.count()}")
print(f"   Retards: {late_today}")

if late_today > 0:
    print(f"\n📋 DÉTAILS DES RETARDS:")
    for p in today_pointages.filter(arrival_status=Pointage.STATUS_LATE):
        print(f"   • {p.employee.first_name} {p.employee.last_name}: {p.late_minutes} min de retard")

print(f"\n💡 Le dashboard admin devrait maintenant afficher {late_today} retard(s)")
print("   Rafraîchissez la page admin pour voir les changements")
