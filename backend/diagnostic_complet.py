#!/usr/bin/env python
"""
Diagnostic complet des problèmes de pointage
"""
import os
import sys
import django
from datetime import date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage
from django.contrib.auth import get_user_model

User = get_user_model()

print("🔍 DIAGNOSTIC COMPLET DES PROBLÈMES")
print("="*80)

today = date.today()
print(f"📅 Date: {today}")

# 1. Vérifier les pointages d'aujourd'hui
print("\n1️⃣ POINTAGES D'AUJOURD'HUI:")
pointages = Pointage.objects.filter(date=today)
print(f"   Total: {pointages.count()}")

for p in pointages:
    print(f"\n   👤 {p.employee.first_name} {p.employee.last_name}")
    print(f"      Arrivée: {p.arrival_time}")
    print(f"      Statut: {p.arrival_status}")
    print(f"      Minutes retard: {p.late_minutes}")
    print(f"      Raison: '{p.late_reason}'")
    print(f"      Justifié: {p.is_justified}")

# 2. Tester l'API des statistiques admin
print("\n2️⃣ TEST API STATISTIQUES ADMIN:")
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
            print(f"   ✅ API fonctionne")
            print(f"   Retards: {data['late_today']}")
            print(f"   Employés en retard: {len(data.get('late_employees', []))}")
            
            for emp in data.get('late_employees', []):
                print(f"      • {emp.get('full_name')}: '{emp.get('late_reason')}'")
        else:
            print(f"   ❌ Erreur {response.status_code}: {response.data}")
    else:
        print("   ❌ Aucun admin trouvé")
        
except Exception as e:
    print(f"   ❌ Exception: {e}")

# 3. Tester l'API today pointage
print("\n3️⃣ TEST API TODAY POINTAGE:")
try:
    from apps.pointage.views import today_pointage
    
    dev = User.objects.filter(role='developer').first()
    if dev:
        request.user = dev
        response = today_pointage(request)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Données: {response.data}")
        else:
            print(f"   ❌ Erreur: {response.data}")
    else:
        print("   ❌ Aucun développeur trouvé")
        
except Exception as e:
    print(f"   ❌ Exception: {e}")

# 4. Recommandations
print("\n4️⃣ RECOMMANDATIONS:")

if pointages.count() == 0:
    print("   📝 Aucun pointage aujourd'hui - Tester un nouveau pointage")
else:
    retards = pointages.filter(arrival_status=Pointage.STATUS_LATE)
    if retards.count() == 0:
        print("   📝 Aucun retard détecté - Vérifier le calcul des statuts")
    else:
        sans_raison = retards.filter(late_reason__isnull=True)
        if sans_raison.count() > 0:
            print(f"   📝 {sans_raison.count()} retard(s) sans raison - Corriger")

print("\n💡 SOLUTIONS:")
print("   1. Supprimer tous les pointages: python clean_restart.py")
print("   2. Corriger les raisons manquantes: python corriger_raisons_manquantes.py")
print("   3. Tester un nouveau pointage avec justification")
print("   4. Vérifier que le frontend utilise les bons champs")
