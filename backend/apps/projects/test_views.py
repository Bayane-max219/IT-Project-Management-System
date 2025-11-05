from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["GET", "POST", "OPTIONS"])
def projects_list(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Données de test pour les projets
    projects_data = [
        {
            'id': 1,
            'name': 'Site E-commerce Moderne',
            'description': 'Développement d\'un site e-commerce avec React et Django',
            'client': {
                'id': 3,
                'first_name': 'Marie',
                'last_name': 'Client',
                'email': 'client@example.com'
            },
            'project_manager': {
                'id': 1,
                'first_name': 'Admin',
                'last_name': 'System',
                'email': 'miguelsingcol@gmail.com'
            },
            'start_date': '2024-01-01',
            'end_date': '2024-03-01',
            'budget': 50000.00,
            'status': 'in_progress',
            'created_at': '2024-01-01T00:00:00Z'
        },
        {
            'id': 2,
            'name': 'Application Mobile Gestion',
            'description': 'App mobile pour la gestion des stocks',
            'client': {
                'id': 3,
                'first_name': 'Marie',
                'last_name': 'Client',
                'email': 'client@example.com'
            },
            'project_manager': {
                'id': 1,
                'first_name': 'Admin',
                'last_name': 'System',
                'email': 'miguelsingcol@gmail.com'
            },
            'start_date': '2024-01-10',
            'end_date': '2024-04-10',
            'budget': 75000.00,
            'status': 'planning',
            'created_at': '2024-01-10T00:00:00Z'
        }
    ]
    
    response = JsonResponse(projects_data, safe=False)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE", "OPTIONS"])
def project_detail(request, pk):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Projet de test basé sur l'ID
    project_data = {
        'id': pk,
        'name': f'Projet Test {pk}',
        'description': f'Description du projet {pk}',
        'client': {
            'id': 3,
            'first_name': 'Marie',
            'last_name': 'Client',
            'email': 'client@example.com'
        },
        'project_manager': {
            'id': 1,
            'first_name': 'Admin',
            'last_name': 'System',
            'email': 'miguelsingcol@gmail.com'
        },
        'start_date': '2024-01-01',
        'end_date': '2024-03-01',
        'budget': 50000.00,
        'status': 'in_progress',
        'created_at': '2024-01-01T00:00:00Z'
    }
    
    response = JsonResponse(project_data)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response
