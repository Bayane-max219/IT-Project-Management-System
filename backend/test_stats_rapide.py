#!/usr/bin/env python
"""
Test rapide des statistiques de pointage
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.views import pointage_stats
from django.contrib.auth import get_user_model
from django.test import RequestFactory

User = get_user_model()

print("🧪 TEST DES STATISTIQUES DE POINTAGE")

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
        print("✅ STATISTIQUES RÉCUPÉRÉES AVEC SUCCÈS")
        print(f"   Total développeurs: {data['total_employees']}")
        print(f"   Présents aujourd'hui: {data['present_today']}")
        print(f"   Retards aujourd'hui: {data['late_today']}")
        print(f"   Heure moyenne d'arrivée: {data['average_arrival_time']}")
        
        if data['late_employees']:
            print(f"\n📋 DÉVELOPPEURS EN RETARD:")
            for emp in data['late_employees']:
                print(f"   • {emp['full_name']}: {emp['late_minutes']} min")
        else:
            print("\n✅ Aucun retard aujourd'hui")
            
    else:
        print(f"❌ ERREUR {response.status_code}")
        print(response.data)
        
except Exception as e:
    print(f"❌ EXCEPTION: {e}")
    import traceback
    traceback.print_exc()

print("\n💡 Si tout fonctionne, rafraîchissez le dashboard admin !")
