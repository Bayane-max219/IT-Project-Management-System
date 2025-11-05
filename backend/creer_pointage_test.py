#!/usr/bin/env python
"""
Créer un pointage de test avec retard et justification
"""
import os
import sys
import django
from datetime import date, time, datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage, PointageSettings
from django.contrib.auth import get_user_model

User = get_user_model()

print("🧪 CRÉATION D'UN POINTAGE DE TEST")
print("="*80)

# Nettoyer d'abord
today = date.today()
Pointage.objects.filter(date=today).delete()
print("🧹 Pointages existants supprimés")

# Trouver un développeur
dev = User.objects.filter(role='developer').first()
if not dev:
    print("❌ Aucun développeur trouvé")
    sys.exit(1)

print(f"👤 Développeur: {dev.first_name} {dev.last_name}")

# Récupérer les paramètres
settings = PointageSettings.objects.first()
if not settings:
    print("❌ Aucun paramètre de pointage")
    sys.exit(1)

print(f"⏰ Heure attendue: {settings.expected_arrival_time}")
print(f"⏱️ Tolérance: {settings.tolerance_minutes} minutes")

# Créer un pointage en retard avec justification
arrival_time = time(10, 30)  # 10h30 = retard de 2h30
late_minutes = 150  # 2h30 en minutes

pointage = Pointage.objects.create(
    employee=dev,
    date=today,
    arrival_time=arrival_time,
    arrival_status=Pointage.STATUS_LATE,
    late_minutes=late_minutes,
    late_reason="Problème de transport - Embouteillages exceptionnels",
    is_justified=True
)

print(f"\n✅ POINTAGE CRÉÉ:")
print(f"   Date: {pointage.date}")
print(f"   Arrivée: {pointage.arrival_time}")
print(f"   Statut: {pointage.arrival_status}")
print(f"   Minutes de retard: {pointage.late_minutes}")
print(f"   Raison: '{pointage.late_reason}'")
print(f"   Justifié: {pointage.is_justified}")

# Vérifier que ça marche dans l'API
print(f"\n🔍 VÉRIFICATION API:")
try:
    from apps.pointage.views import pointage_stats
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.get('/api/pointage/stats/')
    
    admin = User.objects.filter(role='admin').first()
    if admin:
        request.user = admin
        response = pointage_stats(request)
        
        if response.status_code == 200:
            data = response.data
            print(f"   ✅ API Stats fonctionne")
            print(f"   Retards détectés: {data['late_today']}")
            
            late_employees = data.get('late_employees', [])
            print(f"   Employés en retard: {len(late_employees)}")
            
            for emp in late_employees:
                print(f"      • {emp.get('full_name')}")
                print(f"        Raison: '{emp.get('late_reason')}'")
                print(f"        Minutes: {emp.get('late_minutes')}")
        else:
            print(f"   ❌ Erreur API: {response.status_code}")
    else:
        print("   ❌ Aucun admin trouvé")
        
except Exception as e:
    print(f"   ❌ Exception: {e}")

print(f"\n🎯 MAINTENANT:")
print("1. Rafraîchir le dashboard admin")
print("2. Vérifier que la raison apparaît")
print("3. Tester un nouveau pointage pour la synchronisation")

print(f"\n💡 Si la raison n'apparaît toujours pas:")
print("   Le problème est dans le frontend (champs mal mappés)")
print("   Si elle apparaît: le problème était dans les données")
