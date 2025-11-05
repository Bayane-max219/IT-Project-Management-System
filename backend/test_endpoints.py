#!/usr/bin/env python
"""
Script de test pour vérifier les endpoints API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_login():
    """Test de connexion"""
    print("\n" + "="*60)
    print("TEST 1: Connexion")
    print("="*60)
    
    url = f"{BASE_URL}/auth/login/"
    data = {
        "email": "admin@example.com",  # Changez avec un email valide
        "password": "admin123"  # Changez avec un mot de passe valide
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Connexion réussie")
            print(f"Access Token: {result.get('access', 'N/A')[:50]}...")
            return result.get('access')
        else:
            print(f"❌ Erreur: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def test_profile(token):
    """Test de récupération du profil"""
    print("\n" + "="*60)
    print("TEST 2: Récupération du profil")
    print("="*60)
    
    if not token:
        print("❌ Pas de token disponible")
        return False
    
    url = f"{BASE_URL}/auth/profile/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Profil récupéré")
            print(f"Email: {result.get('email')}")
            print(f"Nom: {result.get('first_name')} {result.get('last_name')}")
            return True
        else:
            print(f"❌ Erreur: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_update_profile(token):
    """Test de mise à jour du profil"""
    print("\n" + "="*60)
    print("TEST 3: Mise à jour du profil")
    print("="*60)
    
    if not token:
        print("❌ Pas de token disponible")
        return False
    
    url = f"{BASE_URL}/auth/profile/update/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "first_name": "Test",
        "last_name": "Update"
    }
    
    try:
        response = requests.put(url, json=data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Profil mis à jour")
            print(f"Nouveau nom: {result.get('first_name')} {result.get('last_name')}")
            return True
        else:
            print(f"❌ Erreur: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_pointage_today(token):
    """Test de récupération du pointage du jour"""
    print("\n" + "="*60)
    print("TEST 4: Pointage du jour")
    print("="*60)
    
    if not token:
        print("❌ Pas de token disponible")
        return False
    
    url = f"{BASE_URL}/pointage/today/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Pointage récupéré")
            print(f"Date: {result.get('date')}")
            print(f"Arrivée: {result.get('arrival_time', 'Non pointé')}")
            print(f"Départ: {result.get('departure_time', 'Non pointé')}")
            return True
        elif response.status_code == 404:
            print("ℹ️  Aucun pointage aujourd'hui")
            return True
        else:
            print(f"❌ Erreur: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_clock_out(token):
    """Test de pointage de départ"""
    print("\n" + "="*60)
    print("TEST 5: Pointage de départ")
    print("="*60)
    
    if not token:
        print("❌ Pas de token disponible")
        return False
    
    url = f"{BASE_URL}/pointage/clock-out/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ Départ enregistré")
            return True
        elif response.status_code == 400:
            result = response.json()
            if result.get('requires_justification'):
                print("ℹ️  Justification requise")
                print(f"Message: {result.get('message')}")
                return True
            else:
                print(f"❌ Erreur: {result}")
                return False
        else:
            print(f"❌ Erreur: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("  TESTS DES ENDPOINTS API")
    print("="*60)
    print("\n⚠️  IMPORTANT: Modifiez les identifiants de connexion dans le script")
    print("   (email et mot de passe d'un utilisateur valide)\n")
    
    # Test de connexion
    token = test_login()
    
    if not token:
        print("\n❌ Impossible de continuer sans token")
        return
    
    # Tests avec le token
    results = []
    results.append(("Récupération profil", test_profile(token)))
    results.append(("Mise à jour profil", test_update_profile(token)))
    results.append(("Pointage du jour", test_pointage_today(token)))
    results.append(("Pointage départ", test_clock_out(token)))
    
    # Résumé
    print("\n" + "="*60)
    print("  RÉSUMÉ DES TESTS")
    print("="*60)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:.<40} {status}")
    
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
