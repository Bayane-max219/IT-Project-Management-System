from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def pointage_stats(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    # Statistiques de pointage
    pointage_stats_data = {
        'total_employees': 2,
        'present_today': 1,
        'late_today': 0,
        'absent_today': 1,
        'average_hours_today': 8.5,
        'total_hours_week': 42.5,
        'attendance_rate': 50.0,
        'by_employee': [
            {
                'employee': 'Rakoto Developer',
                'status': 'present',
                'arrival_time': '08:00',
                'hours_worked': 8.5,
                'is_late': False
            },
            {
                'employee': 'Marie Client',
                'status': 'absent',
                'arrival_time': None,
                'hours_worked': 0,
                'is_late': False
            }
        ],
        'weekly_summary': {
            'monday': 1,
            'tuesday': 1,
            'wednesday': 1,
            'thursday': 1,
            'friday': 1,
            'saturday': 0,
            'sunday': 0
        }
    }
    
    response = JsonResponse(pointage_stats_data)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    return response
