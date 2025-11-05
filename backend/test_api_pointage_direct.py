#!/usr/bin/env python
"""
Test direct de l'API pointage stats
"""
import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

print("🔍 TEST DIRECT API POINTAGE STATS")
print("="*50)

# Test de l'API directement
try:
    # Simuler une requête à l'API
    url = "http://127.0.0.1:8000/api/pointage/stats/"
    
    # Il faut un token d'authentification, récupérons un admin
    from django.contrib.auth import get_user_model
    User = get_user_model()
    admin_user = User.objects.filter(role='admin').first()
    
    if not admin_user:
        print("❌ Aucun admin trouvé")
        exit(1)
    
    print(f"👤 Admin trouvé: {admin_user.first_name} {admin_user.last_name}")
    
    # Simuler l'appel de la vue directement
    from apps.pointage.views import pointage_stats
    from django.http import HttpRequest
    from django.contrib.auth.models import AnonymousUser
    
    # Créer une fausse requête
    request = HttpRequest()
    request.method = 'GET'
    request.user = admin_user
    
    # Appeler la vue
    response = pointage_stats(request)
    
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.data
        print(f"📋 DONNÉES RETOURNÉES:")
        print(f"   total_employees: {data.get('total_employees')}")
        print(f"   present_today: {data.get('present_today')}")
        print(f"   late_today: {data.get('late_today')}")
        print(f"   absent_today: {data.get('absent_today')}")
        print(f"   attendance_rate: {data.get('attendance_rate')}")
        print(f"   late_employees count: {len(data.get('late_employees', []))}")
        
        print(f"\n🔍 RÉPONSE COMPLÈTE:")
        print(json.dumps(dict(data), indent=2, default=str))
        
    else:
        print(f"❌ Erreur: {response.data}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
