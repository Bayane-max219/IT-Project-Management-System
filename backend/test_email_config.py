#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail

def test_email_config():
    """Tester la configuration email"""
    print("🔍 TEST CONFIGURATION EMAIL")
    print("="*50)
    
    print(f"📧 EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"📧 EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"📧 EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"📧 EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"📧 EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"📧 EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'VIDE!'}")
    print(f"📧 DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    # Test d'envoi
    if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
        print(f"\n✅ Configuration semble correcte")
        
        try:
            print(f"\n🧪 Test d'envoi d'email...")
            send_mail(
                'Test IT Project Manager',
                'Ceci est un test de configuration email.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],  # Envoyer à soi-même
                fail_silently=False,
            )
            print(f"✅ Email de test envoyé avec succès !")
        except Exception as e:
            print(f"❌ Erreur d'envoi: {e}")
    else:
        print(f"\n❌ Configuration incomplète:")
        if not settings.EMAIL_HOST_USER:
            print(f"   - EMAIL_HOST_USER manquant")
        if not settings.EMAIL_HOST_PASSWORD:
            print(f"   - EMAIL_HOST_PASSWORD manquant")

if __name__ == '__main__':
    test_email_config()
