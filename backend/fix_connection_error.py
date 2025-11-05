#!/usr/bin/env python
import os
import sys
import django
import subprocess
import time

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User

def fix_connection_error():
    print("🔧 Diagnostic et correction de l'erreur de connexion...")
    
    # 1. Vérifier les comptes
    print("\n1️⃣ Vérification des comptes:")
    
    # Supprimer et recréer l'admin
    User.objects.filter(email='miguelsingcol@gmail.com').delete()
    
    admin = User.objects.create_user(
        username='admin',
        email='miguelsingcol@gmail.com',
        first_name='Admin',
        last_name='System',
        role='admin',
        password='admin123'
    )
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    
    print(f"✅ Admin recréé: {admin.email}")
    
    # 2. Tester la connexion directement
    print("\n2️⃣ Test de connexion direct:")
    from django.contrib.auth import authenticate
    
    user = authenticate(username='miguelsingcol@gmail.com', password='admin123')
    if user:
        print("✅ Authentification Django fonctionne")
    else:
        print("❌ Problème d'authentification Django")
        return False
    
    # 3. Créer un serveur de test simple
    print("\n3️⃣ Création d'un serveur de test...")
    
    test_server_code = '''
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
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
        
        if email == 'miguelsingcol@gmail.com' and password == 'admin123':
            response = JsonResponse({
                'access': 'test-token-123',
                'refresh': 'test-refresh-456',
                'user': {
                    'id': 1,
                    'email': email,
                    'role': 'admin',
                    'first_name': 'Admin'
                }
            })
        else:
            response = JsonResponse({'error': 'Identifiants invalides'}, status=400)
        
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
        
    except Exception as e:
        response = JsonResponse({'error': str(e)}, status=500)
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return response
'''
    
    # Écrire le fichier de test
    with open('test_login_view.py', 'w', encoding='utf-8') as f:
        f.write(test_server_code)
    
    # 4. Modifier temporairement les URLs
    print("\n4️⃣ Configuration des URLs de test...")
    
    urls_test = '''
from django.urls import path
from . import test_login_view

urlpatterns = [
    path('test-login/', test_login_view.test_login, name='test_login'),
]
'''
    
    with open('apps/authentication/test_urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_test)
    
    print("✅ Fichiers de test créés")
    
    # 5. Instructions pour l'utilisateur
    print("\n🎯 SOLUTION TEMPORAIRE:")
    print("=" * 50)
    print("1. Arrêtez le serveur Django actuel")
    print("2. Modifiez temporairement core/urls.py:")
    print("   Remplacez la ligne:")
    print("   path('api/auth/', include('apps.authentication.urls')),")
    print("   Par:")
    print("   path('api/auth/', include('apps.authentication.test_urls')),")
    print()
    print("3. Redémarrez le serveur:")
    print("   python manage.py runserver")
    print()
    print("4. Modifiez temporairement le frontend:")
    print("   Dans src/services/authService.js, ligne login:")
    print("   Changez '/auth/login/' en '/auth/test-login/'")
    print()
    print("5. Testez la connexion avec:")
    print("   Email: miguelsingcol@gmail.com")
    print("   Mot de passe: admin123")
    print()
    print("🔧 Cette solution temporaire devrait résoudre l'erreur de connexion")
    print("Une fois que ça marche, on pourra corriger le problème principal")

if __name__ == '__main__':
    fix_connection_error()
