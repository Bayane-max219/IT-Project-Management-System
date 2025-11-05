#!/usr/bin/env python
"""
Test de l'API des statistiques de pointage
"""
import os
import sys
import django
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.views import pointage_stats
from django.contrib.auth import get_user_model
from django.test import RequestFactory

User = get_user_model()

print("\n" + "="*80)
print("  TEST API STATISTIQUES POINTAGE")
print("="*80)

# Créer une requête factice
factory = RequestFactory()
request = factory.get('/api/pointage/stats/')

# Trouver un admin
admin = User.objects.filter(role='admin').first()
if not admin:
    print("❌ Aucun admin trouvé")
    sys.exit(1)

request.user = admin
print(f"👤 Admin: {admin.first_name} {admin.last_name}")

try:
    # Tester la fonction
    response = pointage_stats(request)
    
    if response.status_code == 200:
        data = response.data
        print("✅ API FONCTIONNE")
        
        print(f"\n📊 STATISTIQUES GÉNÉRALES:")
        print(f"   Total développeurs: {data['total_employees']}")
        print(f"   Présents aujourd'hui: {data['present_today']}")
        print(f"   Retards aujourd'hui: {data['late_today']}")
        
        print(f"\n📋 DÉVELOPPEURS EN RETARD:")
        late_employees = data.get('late_employees', [])
        print(f"   Nombre: {len(late_employees)}")
        
        for emp in late_employees:
            print(f"\n   👤 {emp.get('full_name', 'NOM MANQUANT')}")
            print(f"      ID: {emp.get('id')}")
            print(f"      Arrivée: {emp.get('arrival_time')}")
            print(f"      Minutes retard: {emp.get('late_minutes')}")
            print(f"      Raison: '{emp.get('late_reason')}' ({type(emp.get('late_reason'))})")
            print(f"      Justifié: {emp.get('is_justified')}")
            print(f"      Approuvé: {emp.get('justification_approved')}")
        
        print(f"\n📄 DONNÉES JSON COMPLÈTES:")
        print(json.dumps(data, indent=2, default=str))
        
    else:
        print(f"❌ ERREUR {response.status_code}")
        print(response.data)
        
except Exception as e:
    print(f"❌ EXCEPTION: {e}")
    import traceback
    traceback.print_exc()

print(f"\n💡 Si les raisons sont présentes ici, le problème est dans le frontend")
print("   Sinon, le problème est dans le backend")
