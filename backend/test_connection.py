#!/usr/bin/env python
import os
import sys
import django
import requests

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User

def test_connection():
    print("🔍 Test de connexion du système...")
    
    # 1. Test de la base de données
    print("\n1️⃣ Test de la base de données:")
    try:
        admin_count = User.objects.filter(role='admin').count()
        dev_count = User.objects.filter(role='developer').count()
        client_count = User.objects.filter(role='client').count()
        
        print(f"✅ Base de données OK")
        print(f"   - Admins: {admin_count}")
        print(f"   - Développeurs: {dev_count}")
        print(f"   - Clients: {client_count}")
        
        # Vérifier les comptes spécifiques
        admin = User.objects.filter(email='miguelsingcol@gmail.com').first()
        dev = User.objects.filter(email='rakoto@company.com').first()
        client = User.objects.filter(email='client@example.com').first()
        
        print(f"   - Admin Miguel: {'✅' if admin else '❌'}")
        print(f"   - Dev Rakoto: {'✅' if dev else '❌'}")
        print(f"   - Client Demo: {'✅' if client else '❌'}")
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False
    
    # 2. Test de l'API backend
    print("\n2️⃣ Test de l'API backend:")
    try:
        response = requests.get('http://localhost:8000/api/auth/users/', timeout=5)
        if response.status_code == 401:  # Non autorisé = normal
            print("✅ API backend accessible (401 = normal sans token)")
        else:
            print(f"✅ API backend répond: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ API backend non accessible - Serveur non démarré?")
        return False
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        return False
    
    # 3. Test de connexion
    print("\n3️⃣ Test de connexion:")
    try:
        login_data = {
            'email': 'miguelsingcol@gmail.com',
            'password': 'admin123'
        }
        response = requests.post('http://localhost:8000/api/auth/login/', 
                               json=login_data, timeout=5)
        
        if response.status_code == 200:
            print("✅ Connexion admin fonctionne!")
            data = response.json()
            print(f"   - Token reçu: {'✅' if 'access' in data else '❌'}")
        else:
            print(f"❌ Erreur connexion: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test connexion: {e}")
        return False
    
    print("\n🎉 TOUS LES TESTS PASSENT!")
    print("\n📋 Instructions:")
    print("1. Assurez-vous que les serveurs sont démarrés:")
    print("   Backend: python manage.py runserver")
    print("   Frontend: npm start")
    print()
    print("2. Connectez-vous avec:")
    print("   Email: miguelsingcol@gmail.com")
    print("   Mot de passe: admin123")
    print()
    print("3. Si l'erreur persiste, videz le cache du navigateur (Ctrl+F5)")
    
    return True

if __name__ == '__main__':
    test_connection()
