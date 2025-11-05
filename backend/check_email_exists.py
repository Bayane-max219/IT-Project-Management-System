#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User

def check_email_exists(email):
    """Vérifier si un email existe déjà dans la base"""
    print(f"🔍 Vérification de l'email: {email}")
    
    user_exists = User.objects.filter(email=email).exists()
    print(f"📧 Email existe: {user_exists}")
    
    if user_exists:
        user = User.objects.get(email=email)
        print(f"👤 Utilisateur trouvé:")
        print(f"   - ID: {user.id}")
        print(f"   - Username: {user.username}")
        print(f"   - Nom: {user.first_name} {user.last_name}")
        print(f"   - Rôle: {user.role}")
        print(f"   - Actif: {user.is_active}")
        print(f"   - Créé le: {user.created_at}")
    else:
        print("✅ Email disponible pour invitation")

if __name__ == '__main__':
    # Vérifier l'email de test
    check_email_exists('bayane437@gmail.com')
    
    # Vérifier quelques autres emails
    test_emails = [
        'franco.test@example.com',
        'nouveau.dev@company.com',
        'invitation.test@gmail.com'
    ]
    
    for email in test_emails:
        print(f"\n" + "="*50)
        check_email_exists(email)
