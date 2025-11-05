#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User
from apps.projects.models import Project, ProjectTeam
from apps.tasks.models import Task

def create_sample_data():
    print("🚀 Création des données d'exemple...")
    
    # 1. CRÉER 5 DÉVELOPPEURS
    developers_data = [
        {
            'username': 'rakoto_dev',
            'email': 'rakoto@company.com',
            'password': 'dev123',
            'first_name': 'Rakoto',
            'last_name': 'Andriamampianina',
            'phone': '+261 34 12 345 67'
        },
        {
            'username': 'rabe_dev',
            'email': 'rabe@company.com',
            'password': 'dev123',
            'first_name': 'Rabe',
            'last_name': 'Rasoamanana',
            'phone': '+261 34 23 456 78'
        },
        {
            'username': 'hery_dev',
            'email': 'hery@company.com',
            'password': 'dev123',
            'first_name': 'Hery',
            'last_name': 'Razafy',
            'phone': '+261 34 34 567 89'
        },
        {
            'username': 'naina_dev',
            'email': 'naina@company.com',
            'password': 'dev123',
            'first_name': 'Naina',
            'last_name': 'Randriamanantsoa',
            'phone': '+261 34 45 678 90'
        },
        {
            'username': 'solo_dev',
            'email': 'solo@company.com',
            'password': 'dev123',
            'first_name': 'Solo',
            'last_name': 'Raharison',
            'phone': '+261 34 56 789 01'
        }
    ]
    
    developers = []
    for dev_data in developers_data:
        user, created = User.objects.get_or_create(
            email=dev_data['email'],
            defaults={
                'username': dev_data['username'],
                'first_name': dev_data['first_name'],
                'last_name': dev_data['last_name'],
                'phone': dev_data['phone'],
                'role': 'developer'
            }
        )
        if created:
            user.set_password(dev_data['password'])
            user.save()
            print(f"✅ Développeur créé: {user.first_name} {user.last_name}")
        else:
            print(f"ℹ️ Développeur existe déjà: {user.first_name} {user.last_name}")
        developers.append(user)
    
    # 2. CRÉER 2 CLIENTS
    clients_data = [
        {
            'username': 'client_fitiavana',
            'email': 'fitiavana@client.mg',
            'password': 'client123',
            'first_name': 'Fitiavana',
            'last_name': 'Entreprise',
            'phone': '+261 20 22 123 45'
        },
        {
            'username': 'client_tsara',
            'email': 'tsara@client.mg',
            'password': 'client123',
            'first_name': 'Tsara',
            'last_name': 'Solutions',
            'phone': '+261 20 22 234 56'
        }
    ]
    
    clients = []
    for client_data in clients_data:
        user, created = User.objects.get_or_create(
            email=client_data['email'],
            defaults={
                'username': client_data['username'],
                'first_name': client_data['first_name'],
                'last_name': client_data['last_name'],
                'phone': client_data['phone'],
                'role': 'client'
            }
        )
        if created:
            user.set_password(client_data['password'])
            user.save()
            print(f"✅ Client créé: {user.first_name} {user.last_name}")
        else:
            print(f"ℹ️ Client existe déjà: {user.first_name} {user.last_name}")
        clients.append(user)
    
    # 3. CRÉER 3 PROJETS
    projects_data = [
        {
            'name': 'Site E-commerce Fitiavana',
            'description': 'Développement d\'un site e-commerce moderne avec React et Django pour vendre des produits artisanaux malgaches.',
            'client': clients[0],
            'project_manager': developers[0],  # Rakoto comme chef de projet
            'status': 'in_progress',
            'priority': 'high',
            'start_date': datetime.now().date(),
            'end_date': (datetime.now() + timedelta(days=90)).date(),
            'budget': 15000.00,
            'team_members': [developers[0], developers[1]]  # Binôme Rakoto + Rabe
        },
        {
            'name': 'Application Mobile Tsara',
            'description': 'Application mobile cross-platform pour la gestion des commandes et livraisons avec React Native.',
            'client': clients[1],
            'project_manager': developers[2],  # Hery comme chef de projet
            'status': 'planning',
            'priority': 'medium',
            'start_date': (datetime.now() + timedelta(days=15)).date(),
            'end_date': (datetime.now() + timedelta(days=120)).date(),
            'budget': 12000.00,
            'team_members': [developers[2], developers[3]]  # Binôme Hery + Naina
        },
        {
            'name': 'Système de Gestion Interne',
            'description': 'Système de gestion des ressources humaines et comptabilité pour une PME malgache.',
            'client': clients[0],
            'project_manager': developers[4],  # Solo comme chef de projet
            'status': 'planning',
            'priority': 'low',
            'start_date': (datetime.now() + timedelta(days=30)).date(),
            'end_date': (datetime.now() + timedelta(days=150)).date(),
            'budget': 8000.00,
            'team_members': [developers[4]]  # Solo travaille seul
        }
    ]
    
    projects = []
    for proj_data in projects_data:
        project, created = Project.objects.get_or_create(
            name=proj_data['name'],
            defaults={
                'description': proj_data['description'],
                'client': proj_data['client'],
                'project_manager': proj_data['project_manager'],
                'status': proj_data['status'],
                'priority': proj_data['priority'],
                'start_date': proj_data['start_date'],
                'end_date': proj_data['end_date'],
                'budget': proj_data['budget']
            }
        )
        if created:
            print(f"✅ Projet créé: {project.name}")
            # Ajouter les membres de l'équipe
            for member in proj_data['team_members']:
                ProjectTeam.objects.get_or_create(
                    project=project,
                    developer=member,
                    defaults={'role_in_project': 'Développeur'}
                )
        else:
            print(f"ℹ️ Projet existe déjà: {project.name}")
        projects.append(project)
    
    # 4. CRÉER DES TÂCHES POUR CHAQUE PROJET
    tasks_data = [
        # Projet 1: Site E-commerce (Binôme Rakoto + Rabe)
        {
            'title': 'Setup Architecture Backend Django',
            'description': 'Configurer l\'architecture Django avec API REST, authentification JWT et base de données PostgreSQL.',
            'project': projects[0],
            'assigned_to': developers[0],  # Rakoto
            'status': 'in_progress',
            'priority': 'high',
            'estimated_hours': 16,
            'start_date': datetime.now().date(),
            'due_date': (datetime.now() + timedelta(days=7)).date()
        },
        {
            'title': 'Interface Utilisateur React',
            'description': 'Développer les composants React pour le catalogue produits, panier et checkout.',
            'project': projects[0],
            'assigned_to': developers[1],  # Rabe
            'status': 'todo',
            'priority': 'high',
            'estimated_hours': 20,
            'start_date': (datetime.now() + timedelta(days=3)).date(),
            'due_date': (datetime.now() + timedelta(days=14)).date()
        },
        
        # Projet 2: App Mobile (Binôme Hery + Naina)
        {
            'title': 'Analyse des Besoins Mobile',
            'description': 'Analyser les besoins fonctionnels et techniques pour l\'application mobile de gestion des commandes.',
            'project': projects[1],
            'assigned_to': developers[2],  # Hery
            'status': 'todo',
            'priority': 'medium',
            'estimated_hours': 12,
            'start_date': (datetime.now() + timedelta(days=15)).date(),
            'due_date': (datetime.now() + timedelta(days=20)).date()
        },
        {
            'title': 'Maquettes UI/UX Mobile',
            'description': 'Créer les maquettes et prototypes pour l\'interface utilisateur mobile avec Figma.',
            'project': projects[1],
            'assigned_to': developers[3],  # Naina
            'status': 'todo',
            'priority': 'medium',
            'estimated_hours': 14,
            'start_date': (datetime.now() + timedelta(days=18)).date(),
            'due_date': (datetime.now() + timedelta(days=25)).date()
        },
        
        # Projet 3: Système Interne (Solo)
        {
            'title': 'Conception Base de Données RH',
            'description': 'Concevoir et implémenter la base de données pour la gestion des employés, congés et paies.',
            'project': projects[2],
            'assigned_to': developers[4],  # Solo
            'status': 'todo',
            'priority': 'low',
            'estimated_hours': 18,
            'start_date': (datetime.now() + timedelta(days=30)).date(),
            'due_date': (datetime.now() + timedelta(days=40)).date()
        }
    ]
    
    # Récupérer l'admin pour created_by
    admin_user = User.objects.filter(role='admin').first()
    if not admin_user:
        admin_user = User.objects.get(email='miguelsingcol@gmail.com')
    
    for task_data in tasks_data:
        task, created = Task.objects.get_or_create(
            title=task_data['title'],
            project=task_data['project'],
            defaults={
                'description': task_data['description'],
                'assigned_to': task_data['assigned_to'],
                'created_by': admin_user,  # Ajouter le champ obligatoire
                'status': task_data['status'],
                'priority': task_data['priority'],
                'estimated_hours': task_data['estimated_hours'],
                'start_date': task_data['start_date'],
                'due_date': task_data['due_date']
            }
        )
        if created:
            print(f"✅ Tâche créée: {task.title}")
        else:
            print(f"ℹ️ Tâche existe déjà: {task.title}")
    
    print("\n🎉 Données d'exemple créées avec succès!")
    print("\n📋 RÉSUMÉ:")
    print(f"👥 Développeurs: {User.objects.filter(role='developer').count()}")
    print(f"🏢 Clients: {User.objects.filter(role='client').count()}")
    print(f"📁 Projets: {Project.objects.count()}")
    print(f"✅ Tâches: {Task.objects.count()}")
    
    print("\n🔐 COMPTES CRÉÉS:")
    print("👨‍💻 DÉVELOPPEURS:")
    for dev in User.objects.filter(role='developer'):
        print(f"  - {dev.email} / dev123 ({dev.first_name} {dev.last_name})")
    
    print("\n🏢 CLIENTS:")
    for client in User.objects.filter(role='client'):
        print(f"  - {client.email} / client123 ({client.first_name} {client.last_name})")

if __name__ == '__main__':
    create_sample_data()
