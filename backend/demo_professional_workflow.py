#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User, RegistrationKey
from apps.authentication.email_service import send_account_creation_email, generate_password, generate_registration_key

def demo_professional_workflow():
    print("🎯 Démonstration du Workflow Professionnel")
    print("=" * 50)
    
    # 1. Admin crée un développeur avec email automatique
    print("\n1️⃣ CRÉATION D'UN DÉVELOPPEUR AVEC EMAIL")
    print("-" * 40)
    
    admin = User.objects.get(email='miguelsingcol@gmail.com')
    password = generate_password()
    
    developer = User.objects.create_user(
        username='jean_rakoto',
        email='jean.rakoto@example.com',
        first_name='Jean',
        last_name='Rakoto',
        role='developer',
        phone='+261 34 12 345 67'
    )
    developer.set_password(password)
    developer.save()
    
    print(f"✅ Développeur créé: {developer.email}")
    print(f"🔑 Mot de passe temporaire: {password}")
    
    # Simuler l'envoi d'email
    email_sent = send_account_creation_email(developer, password, created_by_admin=True)
    print(f"📧 Email envoyé: {'✅ Oui' if email_sent else '❌ Non (mode console)'}")
    
    # 2. Admin envoie une invitation avec clé
    print("\n2️⃣ INVITATION AVEC CLÉ D'INSCRIPTION")
    print("-" * 40)
    
    registration_key = generate_registration_key()
    client_email = 'marie.client@entreprise.mg'
    
    reg_key = RegistrationKey.objects.create(
        key=registration_key,
        email=client_email,
        role='client',
        created_by=admin
    )
    
    print(f"✅ Clé d'invitation créée pour: {client_email}")
    print(f"🔑 Clé: {registration_key}")
    print(f"⏰ Expire le: {reg_key.expires_at}")
    print(f"🔗 Lien d'inscription: http://localhost:3000/register?key={registration_key}")
    
    # 3. Statistiques du système
    print("\n3️⃣ ÉTAT DU SYSTÈME")
    print("-" * 40)
    
    stats = {
        'admins': User.objects.filter(role='admin').count(),
        'developers': User.objects.filter(role='developer').count(),
        'clients': User.objects.filter(role='client').count(),
        'active_keys': RegistrationKey.objects.filter(is_used=False).count()
    }
    
    print(f"👥 Utilisateurs:")
    print(f"   - Administrateurs: {stats['admins']}")
    print(f"   - Développeurs: {stats['developers']}")
    print(f"   - Clients: {stats['clients']}")
    print(f"🔑 Clés d'invitation actives: {stats['active_keys']}")
    
    # 4. Instructions pour tester
    print("\n4️⃣ INSTRUCTIONS DE TEST")
    print("-" * 40)
    print("🚀 Pour tester le système:")
    print("1. Démarrez les serveurs:")
    print("   Backend:  python manage.py runserver")
    print("   Frontend: npm start")
    print()
    print("2. Connectez-vous en tant qu'admin:")
    print("   Email: miguelsingcol@gmail.com")
    print("   Mot de passe: [votre mot de passe]")
    print()
    print("3. Testez les nouvelles fonctionnalités:")
    print("   - Page Utilisateurs → 'Créer & Envoyer Email'")
    print("   - Page Utilisateurs → 'Envoyer Invitation'")
    print()
    print("4. Interface de connexion:")
    print("   - Plus de comptes de test visibles")
    print("   - Message professionnel affiché")
    print()
    print("5. Système de pointage:")
    print("   - Heures normales: 8h00 - 17h00")
    print("   - Pause déjeuner: 12h00 - 13h00")
    print("   - Tolérance: 15 minutes")
    
    print("\n🎉 Système professionnel prêt à l'emploi !")

if __name__ == '__main__':
    demo_professional_workflow()
