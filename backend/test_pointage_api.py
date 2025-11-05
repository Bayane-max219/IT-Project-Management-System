#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.views import pointage_stats
from apps.authentication.models import User
from django.test import RequestFactory
from rest_framework.authtoken.models import Token

def test_pointage_stats():
    print("🔍 Test de l'API des statistiques de pointage...")
    
    try:
        # Créer une requête factice avec authentification
        factory = RequestFactory()
        request = factory.get('/api/pointage/stats/')
        
        # Récupérer l'utilisateur admin
        user = User.objects.get(email='miguelsingcol@gmail.com')
        request.user = user
        
        print(f"👤 Utilisateur: {user.email}")
        print(f"📋 Rôle: {user.role}")
        print(f"🔍 is_admin(): {user.is_admin()}")
        print(f"🔐 is_authenticated: {user.is_authenticated}")
        
        # Appeler la fonction
        response = pointage_stats(request)
        
        print(f"✅ Réponse API: Status {response.status_code}")
        print(f"📄 Données: {response.data}")
        
        if response.status_code == 200:
            print("🎉 L'API fonctionne correctement !")
        else:
            print("❌ L'API retourne une erreur")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_pointage_stats()
