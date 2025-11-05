from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["GET", "POST", "OPTIONS"])
def users_list(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Données de test pour les utilisateurs
    users_data = [
        {
            'id': 1,
            'username': 'admin',
            'email': 'miguelsingcol@gmail.com',
            'first_name': 'Admin',
            'last_name': 'System',
            'role': 'admin',
            'phone': '+261 34 00 000 00',
            'is_active': True,
            'created_at': '2024-01-01T00:00:00Z'
        },
        {
            'id': 2,
            'username': 'rakoto_dev',
            'email': 'rakoto@company.com',
            'first_name': 'Rakoto',
            'last_name': 'Developer',
            'role': 'developer',
            'phone': '+261 34 12 345 67',
            'is_active': True,
            'created_at': '2024-01-02T00:00:00Z'
        },
        {
            'id': 3,
            'username': 'client_demo',
            'email': 'client@example.com',
            'first_name': 'Marie',
            'last_name': 'Client',
            'role': 'client',
            'phone': '+261 34 98 765 43',
            'is_active': True,
            'created_at': '2024-01-03T00:00:00Z'
        }
    ]
    
    response = JsonResponse(users_data, safe=False)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def profile_view(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Profil de test basé sur le token (simulé)
    profile_data = {
        'id': 1,
        'username': 'admin',
        'email': 'miguelsingcol@gmail.com',
        'first_name': 'Admin',
        'last_name': 'System',
        'role': 'admin',
        'phone': '+261 34 00 000 00',
        'is_active': True,
        'full_name': 'Admin System'
    }
    
    response = JsonResponse(profile_data)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def logout_view(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    response = JsonResponse({'message': 'Déconnexion réussie'})
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response
