#!/usr/bin/env python
"""
Debug complet du processus de pointage
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage, PointageSettings
from datetime import date, time, datetime, timedelta

today = date.today()
pointage = Pointage.objects.filter(date=today).last()

print("🔍 DEBUG COMPLET DU DERNIER POINTAGE")
print("="*60)

if not pointage:
    print("❌ Aucun pointage trouvé")
    exit(1)

print(f"👤 Employé: {pointage.employee.first_name} {pointage.employee.last_name}")
print(f"📅 Date: {pointage.date}")
print(f"⏰ Heure arrivée: {pointage.arrival_time}")
print(f"📊 Statut: {pointage.arrival_status}")
print(f"⏱️ Minutes retard: {pointage.late_minutes}")
print(f"📝 Raison: '{pointage.late_reason}' (type: {type(pointage.late_reason)})")
print(f"✅ Justifié: {pointage.is_justified}")

# Vérifier les paramètres
settings = PointageSettings.objects.first()
if settings:
    print(f"\n⚙️ PARAMÈTRES:")
    print(f"   Heure attendue: {settings.expected_arrival_time}")
    print(f"   Tolérance: {settings.tolerance_minutes} minutes")
    
    # Calculer si c'est vraiment un retard
    tolerance_time = (
        datetime.combine(today, settings.expected_arrival_time) + 
        timedelta(minutes=settings.tolerance_minutes)
    ).time()
    
    print(f"   Limite tolérance: {tolerance_time}")
    
    if pointage.arrival_time > tolerance_time:
        print(f"   ✅ RETARD CONFIRMÉ: {pointage.arrival_time} > {tolerance_time}")
        print(f"   → Le système DEVRAIT demander une justification")
    else:
        print(f"   ❌ PAS DE RETARD: {pointage.arrival_time} <= {tolerance_time}")
        print(f"   → Le système ne demande pas de justification")

print(f"\n🔍 ANALYSE:")
if pointage.late_reason is None and pointage.arrival_status == 'late':
    print("❌ PROBLÈME: Retard détecté mais aucune justification sauvegardée")
    print("   Causes possibles:")
    print("   1. Le frontend n'envoie pas la justification")
    print("   2. Le backend ne reçoit pas la justification")
    print("   3. Erreur dans le processus de sauvegarde")
elif pointage.arrival_status != 'late':
    print("ℹ️ INFO: Pas de retard détecté, justification non nécessaire")
else:
    print("✅ OK: Justification présente")

print(f"\n💡 PROCHAINE ÉTAPE:")
print("Regardez les logs du serveur Django pour voir si les messages de debug apparaissent")
