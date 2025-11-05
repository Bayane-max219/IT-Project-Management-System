from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["GET", "POST", "OPTIONS"])
def tasks_list(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Données de test pour les tâches
    tasks_data = [
        {
            'id': 1,
            'title': 'Setup Architecture Backend',
            'description': 'Configurer Django REST Framework et base de données',
            'project': {
                'id': 1,
                'name': 'Site E-commerce Moderne'
            },
            'assigned_to': {
                'id': 2,
                'first_name': 'Rakoto',
                'last_name': 'Developer',
                'email': 'rakoto@company.com'
            },
            'created_by': {
                'id': 1,
                'first_name': 'Admin',
                'last_name': 'System'
            },
            'status': 'in_progress',
            'priority': 'high',
            'estimated_hours': 16,
            'actual_hours': 8,
            'start_date': '2024-01-01',
            'due_date': '2024-01-05',
            'completed_at': None,
            'created_at': '2024-01-01T00:00:00Z'
        },
        {
            'id': 2,
            'title': 'Interface Utilisateur React',
            'description': 'Développer les composants React pour le frontend',
            'project': {
                'id': 1,
                'name': 'Site E-commerce Moderne'
            },
            'assigned_to': {
                'id': 2,
                'first_name': 'Rakoto',
                'last_name': 'Developer',
                'email': 'rakoto@company.com'
            },
            'created_by': {
                'id': 1,
                'first_name': 'Admin',
                'last_name': 'System'
            },
            'status': 'todo',
            'priority': 'medium',
            'estimated_hours': 24,
            'actual_hours': 0,
            'start_date': '2024-01-03',
            'due_date': '2024-01-10',
            'completed_at': None,
            'created_at': '2024-01-01T00:00:00Z'
        },
        {
            'id': 3,
            'title': 'Analyse des Besoins Mobile',
            'description': 'Analyser les besoins pour l\'application mobile',
            'project': {
                'id': 2,
                'name': 'Application Mobile Gestion'
            },
            'assigned_to': {
                'id': 2,
                'first_name': 'Rakoto',
                'last_name': 'Developer',
                'email': 'rakoto@company.com'
            },
            'created_by': {
                'id': 1,
                'first_name': 'Admin',
                'last_name': 'System'
            },
            'status': 'todo',
            'priority': 'high',
            'estimated_hours': 8,
            'actual_hours': 0,
            'start_date': '2024-01-10',
            'due_date': '2024-01-15',
            'completed_at': None,
            'created_at': '2024-01-10T00:00:00Z'
        }
    ]
    
    response = JsonResponse(tasks_data, safe=False)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def my_tasks(request):
    """Endpoint spécial pour les tâches du développeur connecté"""
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Tâches assignées au développeur Rakoto (ID: 2)
    my_tasks_data = [
        {
            'id': 1,
            'title': 'Setup Architecture Backend',
            'description': 'Configurer Django REST Framework et base de données',
            'project': {
                'id': 1,
                'name': 'Site E-commerce Moderne'
            },
            'status': 'in_progress',
            'priority': 'high',
            'estimated_hours': 16,
            'actual_hours': 8,
            'start_date': '2024-01-01',
            'due_date': '2024-01-05',
            'is_overdue': False,
            'days_remaining': 2
        },
        {
            'id': 2,
            'title': 'Interface Utilisateur React',
            'description': 'Développer les composants React pour le frontend',
            'project': {
                'id': 1,
                'name': 'Site E-commerce Moderne'
            },
            'status': 'todo',
            'priority': 'medium',
            'estimated_hours': 24,
            'actual_hours': 0,
            'start_date': '2024-01-03',
            'due_date': '2024-01-10',
            'is_overdue': False,
            'days_remaining': 7
        },
        {
            'id': 3,
            'title': 'Analyse des Besoins Mobile',
            'description': 'Analyser les besoins pour l\'application mobile',
            'project': {
                'id': 2,
                'name': 'Application Mobile Gestion'
            },
            'status': 'todo',
            'priority': 'high',
            'estimated_hours': 8,
            'actual_hours': 0,
            'start_date': '2024-01-10',
            'due_date': '2024-01-15',
            'is_overdue': False,
            'days_remaining': 12
        }
    ]
    
    response = JsonResponse(my_tasks_data, safe=False)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE", "OPTIONS"])
def task_detail(request, pk):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Tâche de test basée sur l'ID
    task_data = {
        'id': pk,
        'title': f'Tâche Test {pk}',
        'description': f'Description de la tâche {pk}',
        'project': {
            'id': 1,
            'name': 'Site E-commerce Moderne'
        },
        'assigned_to': {
            'id': 2,
            'first_name': 'Rakoto',
            'last_name': 'Developer',
            'email': 'rakoto@company.com'
        },
        'created_by': {
            'id': 1,
            'first_name': 'Admin',
            'last_name': 'System'
        },
        'status': 'todo',
        'priority': 'medium',
        'estimated_hours': 8,
        'actual_hours': 0,
        'start_date': '2024-01-01',
        'due_date': '2024-01-05',
        'completed_at': None,
        'created_at': '2024-01-01T00:00:00Z'
    }
    
    response = JsonResponse(task_data)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def task_stats(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Statistiques des tâches - Format exact pour le frontend
    task_stats_data = {
        'total_tasks': 3,
        'in_progress_tasks': 1,
        'completed_tasks': 0,
        'todo_tasks': 2,
        'overdue_tasks': 0,
        'tasks_by_priority': {
            'Haute': 2,
            'Moyenne': 1,
            'Basse': 0
        },
        'tasks_by_developer': {
            'Rakoto Developer': 3,
            'Admin System': 0
        }
    }
    
    response = JsonResponse(task_stats_data)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response
