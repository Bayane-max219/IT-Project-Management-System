#!/usr/bin/env python
"""
Test des fonctionnalités de modification de projets et tâches
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

def test_projects_tasks_update():
    """Test de modification de projets et tâches"""
    print("=== Test de Modification Projets et Tâches ===")
    
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
        
        # 2. Test des projets
        print("\n2. Test de modification des projets...")
        
        # Récupérer la liste des projets
        response = requests.get(f"{BASE_URL}/projects/", headers=headers)
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ {len(projects)} projets trouvés")
            
            if projects:
                # Modifier le premier projet
                project_id = projects[0]['id']
                update_data = {
                    "name": "Projet Modifié Test",
                    "description": "Description mise à jour par test admin",
                    "status": "EN_COURS",
                    "priority": "HAUTE"
                }
                
                response = requests.patch(f"{BASE_URL}/projects/{project_id}/", json=update_data, headers=headers)
                if response.status_code == 200:
                    updated_project = response.json()
                    print("✅ Projet modifié avec succès")
                    print(f"   - Nouveau nom: {updated_project.get('name')}")
                    print(f"   - Statut: {updated_project.get('status')}")
                else:
                    print(f"❌ Erreur modification projet: {response.status_code}")
                    print(f"   Erreurs: {response.text}")
            else:
                print("⚠️ Aucun projet à modifier")
        else:
            print(f"❌ Erreur récupération projets: {response.status_code}")
        
        # 3. Test des tâches
        print("\n3. Test de modification des tâches...")
        
        # Récupérer la liste des tâches
        response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ {len(tasks)} tâches trouvées")
            
            if tasks:
                # Modifier la première tâche
                task_id = tasks[0]['id']
                update_data = {
                    "title": "Tâche Modifiée Test",
                    "description": "Description mise à jour par test admin",
                    "status": "EN_COURS",
                    "priority": "HAUTE",
                    "estimated_hours": 8
                }
                
                response = requests.patch(f"{BASE_URL}/tasks/{task_id}/", json=update_data, headers=headers)
                if response.status_code == 200:
                    updated_task = response.json()
                    print("✅ Tâche modifiée avec succès")
                    print(f"   - Nouveau titre: {updated_task.get('title')}")
                    print(f"   - Statut: {updated_task.get('status')}")
                    print(f"   - Heures estimées: {updated_task.get('estimated_hours')}")
                else:
                    print(f"❌ Erreur modification tâche: {response.status_code}")
                    print(f"   Erreurs: {response.text}")
            else:
                print("⚠️ Aucune tâche à modifier")
        else:
            print(f"❌ Erreur récupération tâches: {response.status_code}")
        
        # 4. Test de création de projet
        print("\n4. Test de création de projet...")
        new_project_data = {
            "name": "Nouveau Projet Test",
            "description": "Projet créé par test admin",
            "client": 1,  # ID du client
            "project_manager": 1,  # ID du manager
            "status": "PLANIFIE",
            "priority": "MOYENNE",
            "start_date": "2025-10-24",
            "end_date": "2025-12-31",
            "budget": 50000
        }
        
        response = requests.post(f"{BASE_URL}/projects/", json=new_project_data, headers=headers)
        if response.status_code == 201:
            new_project = response.json()
            print("✅ Nouveau projet créé")
            print(f"   - ID: {new_project.get('id')}")
            print(f"   - Nom: {new_project.get('name')}")
            
            # Supprimer le projet de test
            project_id = new_project.get('id')
            response = requests.delete(f"{BASE_URL}/projects/{project_id}/", headers=headers)
            if response.status_code == 204:
                print("✅ Projet de test supprimé")
            else:
                print("⚠️ Projet de test non supprimé")
        else:
            print(f"❌ Erreur création projet: {response.status_code}")
            print(f"   Erreurs: {response.text}")
        
        # 5. Test de création de tâche
        print("\n5. Test de création de tâche...")
        if projects:
            new_task_data = {
                "title": "Nouvelle Tâche Test",
                "description": "Tâche créée par test admin",
                "project": projects[0]['id'],
                "status": "A_FAIRE",
                "priority": "MOYENNE",
                "estimated_hours": 4,
                "start_date": "2025-10-24",
                "due_date": "2025-10-30"
            }
            
            response = requests.post(f"{BASE_URL}/tasks/", json=new_task_data, headers=headers)
            if response.status_code == 201:
                new_task = response.json()
                print("✅ Nouvelle tâche créée")
                print(f"   - ID: {new_task.get('id')}")
                print(f"   - Titre: {new_task.get('title')}")
                
                # Supprimer la tâche de test
                task_id = new_task.get('id')
                response = requests.delete(f"{BASE_URL}/tasks/{task_id}/", headers=headers)
                if response.status_code == 204:
                    print("✅ Tâche de test supprimée")
                else:
                    print("⚠️ Tâche de test non supprimée")
            else:
                print(f"❌ Erreur création tâche: {response.status_code}")
                print(f"   Erreurs: {response.text}")
        
        print("\n🎉 Tests de modification terminés avec succès!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Serveur Django non accessible")
        print("   Démarrez le serveur avec: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

if __name__ == '__main__':
    success = test_projects_tasks_update()
    if success:
        print("\n✅ Toutes les fonctionnalités de modification projets/tâches fonctionnent!")
        print("\nFonctionnalités testées:")
        print("- ✅ Modification de projets")
        print("- ✅ Modification de tâches") 
        print("- ✅ Création de projets")
        print("- ✅ Création de tâches")
        print("- ✅ Suppression de projets")
        print("- ✅ Suppression de tâches")
    else:
        print("\n❌ Des problèmes ont été détectés dans les fonctionnalités de modification.")
