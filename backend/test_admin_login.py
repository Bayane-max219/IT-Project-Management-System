#!/usr/bin/env python
"""
Test rapide de connexion admin après correction des URLs
"""
import os
import sys
import django
import requests

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def test_admin_login():
    """Test de connexion admin"""
    print("=== Test de Connexion Admin ===")
    
    # URL de l'API
    BASE_URL = "http://127.0.0.1:8000/api"
    
    # Données de connexion admin
    login_data = {
        "email": "miguelsingcol@gmail.com",
        "password": "admin123"
    }
    
    try:
        print("Test de connexion admin...")
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Connexion admin réussie!")
            print(f"   - Utilisateur: {data.get('user', {}).get('email', 'N/A')}")
            print(f"   - Rôle: {data.get('user', {}).get('role', 'N/A')}")
            print(f"   - Token reçu: {'Oui' if data.get('access') else 'Non'}")
            
            # Test d'une requête authentifiée
            headers = {"Authorization": f"Bearer {data.get('access')}"}
            response = requests.get(f"{BASE_URL}/auth/users/", headers=headers, timeout=5)
            
            if response.status_code == 200:
                users = response.json()
                print(f"✅ Accès aux utilisateurs: {len(users)} utilisateurs trouvés")
            else:
                print(f"❌ Erreur accès utilisateurs: {response.status_code}")
            
            return True
            
        else:
            print(f"❌ Erreur de connexion: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Serveur Django non accessible")
        print("   Démarrez le serveur avec: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

if __name__ == '__main__':
    success = test_admin_login()
    if success:
        print("\n🎉 Connexion admin fonctionnelle!")
        print("Vous pouvez maintenant utiliser l'interface avec les identifiants admin.")
    else:
        print("\n❌ Problème de connexion détecté.")
        print("Vérifiez que le serveur Django est en cours d'exécution.")
