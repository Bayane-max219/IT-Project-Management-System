from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
import json

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def test_login(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        print(f"🔍 Tentative de connexion: {email}")
        
        # Test direct avec les comptes créés
        if email == 'miguelsingcol@gmail.com' and password == 'admin123':
            response = JsonResponse({
                'access': 'test-admin-token-123',
                'refresh': 'test-admin-refresh-456',
                'user': {
                    'id': 1,
                    'email': email,
                    'role': 'admin',
                    'first_name': 'Admin',
                    'last_name': 'System'
                }
            })
            print("✅ Connexion admin réussie")
        elif email == 'rakoto@company.com' and password == 'dev123':
            response = JsonResponse({
                'access': 'test-dev-token-123',
                'refresh': 'test-dev-refresh-456',
                'user': {
                    'id': 2,
                    'email': email,
                    'role': 'developer',
                    'first_name': 'Rakoto',
                    'last_name': 'Developer'
                }
            })
            print("✅ Connexion développeur réussie")
        elif email == 'client@example.com' and password == 'client123':
            response = JsonResponse({
                'access': 'test-client-token-123',
                'refresh': 'test-client-refresh-456',
                'user': {
                    'id': 3,
                    'email': email,
                    'role': 'client',
                    'first_name': 'Marie',
                    'last_name': 'Client'
                }
            })
            print("✅ Connexion client réussie")
        else:
            response = JsonResponse({'error': 'Identifiants invalides'}, status=400)
            print(f"❌ Identifiants invalides pour: {email}")
        
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        response = JsonResponse({'error': str(e)}, status=500)
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response
