#!/usr/bin/env python
"""
Test complet du client Marie avec serveur
"""
import os
import sys
import django
import requests
import time
import subprocess
import threading

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def start_server():
    """Démarrer le serveur Django en arrière-plan"""
    print("Démarrage du serveur Django...")
    try:
        # Tuer les processus existants sur le port 8000
        subprocess.run("taskkill /f /im python.exe", shell=True, capture_output=True)
        time.sleep(2)
        
        # Démarrer le serveur
        process = subprocess.Popen(
            ["python", "manage.py", "runserver", "127.0.0.1:8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # Attendre que le serveur démarre
        print("Attente du démarrage du serveur...")
        time.sleep(5)
        
        # Tester si le serveur répond
        for i in range(10):
            try:
                response = requests.get("http://127.0.0.1:8000/api/", timeout=2)
                if response.status_code in [200, 404]:  # 404 est OK, ça veut dire que le serveur répond
                    print("✅ Serveur démarré avec succès")
                    return process
            except:
                print(f"Tentative {i+1}/10...")
                time.sleep(2)
        
        print("❌ Impossible de démarrer le serveur")
        return None
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return None

def test_client_complete():
    """Test complet du client"""
    print("=== Test Complet Client Marie ===")
    
    BASE_URL = "http://127.0.0.1:8000/api"
    
    # 1. Vérifier les données en base
    print("\n1. Vérification des données en base...")
    from apps.authentication.models import User
    from apps.projects.models import Project
    
    try:
        marie = User.objects.get(email="client@example.com")
        projects = Project.objects.filter(client=marie)
        
        print(f"✅ Marie trouvée: {marie.email} (ID: {marie.id})")
        print(f"✅ Projets en base: {projects.count()}")
        
        for project in projects:
            print(f"  - {project.name}")
            print(f"    Status: '{project.status}'")
            print(f"    Priority: '{project.priority}'")
            print(f"    Client ID: {project.client_id}")
            
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False
    
    # 2. Démarrer le serveur
    print("\n2. Démarrage du serveur...")
    server_process = start_server()
    
    if not server_process:
        print("❌ Impossible de démarrer le serveur")
        return False
    
    try:
        # 3. Test de connexion
        print("\n3. Test de connexion client...")
        login_data = {
            "email": "client@example.com",
            "password": "client123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data, timeout=10)
        print(f"Status connexion: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Connexion réussie")
            print(f"User: {data.get('user', {})}")
            
            token = data.get('access')
            headers = {"Authorization": f"Bearer {token}"}
            
            # 4. Test API projets
            print("\n4. Test API projets...")
            response = requests.get(f"{BASE_URL}/projects/", headers=headers, timeout=10)
            print(f"Status projets: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                projects_api = response.json()
                print(f"✅ Projets API: {len(projects_api)}")
                
                for project in projects_api:
                    print(f"  - {project.get('name')}")
                    print(f"    ID: {project.get('id')}")
                    print(f"    Status: {project.get('status')}")
                    print(f"    Client: {project.get('client', {})}")
                    
                if len(projects_api) > 0:
                    print("\n🎉 SUCCESS! Marie peut voir ses projets via l'API")
                    return True
                else:
                    print("\n❌ PROBLEM: L'API ne retourne aucun projet")
                    return False
            else:
                print(f"❌ Erreur API projets: {response.text}")
                return False
        else:
            print(f"❌ Erreur de connexion: {response.text}")
            return False
            
    finally:
        # Arrêter le serveur
        if server_process:
            print("\nArrêt du serveur...")
            server_process.terminate()
            time.sleep(2)

def main():
    """Fonction principale"""
    print("🚀 Démarrage du test complet...")
    
    # 1. Corriger les statuts d'abord
    print("1. Correction des statuts...")
    exec(open('fix_project_status.py').read())
    
    # 2. Tester l'API
    print("\n2. Test de l'API...")
    success = test_client_complete()
    
    if success:
        print("\n🎉 RÉSULTAT: Le client Marie peut maintenant voir ses projets!")
        print("\nPour tester manuellement:")
        print("1. Démarrez le serveur: python manage.py runserver")
        print("2. Démarrez le frontend: cd ../frontend && npm start")
        print("3. Connectez-vous avec client@example.com / client123")
    else:
        print("\n❌ RÉSULTAT: Il y a encore un problème à résoudre")

if __name__ == '__main__':
    main()
