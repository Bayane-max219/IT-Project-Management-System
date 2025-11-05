from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def dashboard_stats(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Statistiques du dashboard - Format exact pour le frontend
    stats_data = {
        'total_projects': 2,
        'active_projects': 2,
        'completed_projects': 0,
        'projects_by_status': {
            'Planification': 1,
            'En cours': 1,
            'Terminé': 0,
            'En pause': 0
        },
        'tasks_by_developer': {
            'Rakoto Developer': 3,
            'Admin System': 0
        }
    }
    
    response = JsonResponse(stats_data)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def projects_by_status(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Projets par statut pour le graphique
    projects_stats = [
        {'status': 'planning', 'count': 1, 'label': 'Planification'},
        {'status': 'in_progress', 'count': 1, 'label': 'En cours'},
        {'status': 'completed', 'count': 0, 'label': 'Terminé'},
        {'status': 'on_hold', 'count': 0, 'label': 'En pause'}
    ]
    
    response = JsonResponse(projects_stats, safe=False)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def tasks_by_developer(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Tâches par développeur pour le graphique
    tasks_stats = [
        {
            'developer': 'Rakoto Developer',
            'todo': 2,
            'in_progress': 1,
            'completed': 0,
            'total': 3
        }
    ]
    
    response = JsonResponse(tasks_stats, safe=False)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response
