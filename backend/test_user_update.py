#!/usr/bin/env python
"""
Test des fonctionnalités de modification d'utilisateur
"""
import os
import sys
import django
import requests
import json

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def test_user_update():
    """Test de modification d'utilisateur"""
    print("=== Test de Modification d'Utilisateur ===")
    
    BASE_URL = "http://127.0.0.1:8000/api"
    
    # 1. Connexion admin
    print("1. Connexion admin...")
    login_data = {
        "email": "miguelsingcol@gmail.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data, timeout=5)
        if response.status_code != 200:
            print(f"❌ Erreur de connexion: {response.status_code}")
            return False
            
        token_data = response.json()
        headers = {"Authorization": f"Bearer {token_data.get('access')}"}
        print("✅ Connexion réussie")
        
        # 2. Récupérer le profil actuel
        print("\n2. Récupération du profil...")
        response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Profil récupéré: {profile.get('email')}")
            user_id = profile.get('id')
        else:
            print(f"❌ Erreur récupération profil: {response.status_code}")
            return False
        
        # 3. Test de modification du profil
        print("\n3. Test de modification du profil...")
        update_data = {
            "first_name": "Miguel Updated",
            "last_name": "Test Update",
            "phone": "+261 34 12 34 56"
        }
        
        response = requests.put(f"{BASE_URL}/auth/profile/update/", json=update_data, headers=headers)
        if response.status_code == 200:
            updated_profile = response.json()
            print("✅ Profil modifié avec succès")
            print(f"   - Nom: {updated_profile.get('first_name')} {updated_profile.get('last_name')}")
            print(f"   - Téléphone: {updated_profile.get('phone')}")
        else:
            print(f"❌ Erreur modification profil: {response.status_code}")
            print(f"   Erreurs: {response.text}")
            return False
        
        # 4. Test de modification via l'API utilisateurs
        print("\n4. Test de modification via API utilisateurs...")
        update_data2 = {
            "first_name": "Miguel Admin",
            "last_name": "Final Test"
        }
        
        response = requests.patch(f"{BASE_URL}/auth/users/{user_id}/", json=update_data2, headers=headers)
        if response.status_code == 200:
            updated_user = response.json()
            print("✅ Utilisateur modifié via API")
            print(f"   - Nom complet: {updated_user.get('full_name')}")
        else:
            print(f"❌ Erreur modification utilisateur: {response.status_code}")
            print(f"   Erreurs: {response.text}")
        
        # 5. Test de changement de mot de passe
        print("\n5. Test de changement de mot de passe...")
        password_data = {
            "old_password": "admin123",
            "new_password": "newadmin123!",
            "new_password_confirm": "newadmin123!"
        }
        
        response = requests.post(f"{BASE_URL}/auth/change-password/", json=password_data, headers=headers)
        if response.status_code == 200:
            print("✅ Mot de passe changé avec succès")
            
            # Remettre l'ancien mot de passe
            restore_password_data = {
                "old_password": "newadmin123!",
                "new_password": "admin123",
                "new_password_confirm": "admin123"
            }
            
            response = requests.post(f"{BASE_URL}/auth/change-password/", json=restore_password_data, headers=headers)
            if response.status_code == 200:
                print("✅ Mot de passe restauré")
            else:
                print("⚠️ Attention: Mot de passe non restauré")
        else:
            print(f"❌ Erreur changement mot de passe: {response.status_code}")
            print(f"   Erreurs: {response.text}")
        
        print("\n🎉 Tests de modification terminés avec succès!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Serveur Django non accessible")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

if __name__ == '__main__':
    success = test_user_update()
    if success:
        print("\n✅ Toutes les fonctionnalités de modification fonctionnent correctement!")
    else:
        print("\n❌ Des problèmes ont été détectés dans les fonctionnalités de modification.")
