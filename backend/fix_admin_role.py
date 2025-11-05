#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User

def fix_admin_role():
    try:
        # Chercher l'utilisateur Miguel
        miguel = User.objects.get(email='miguelsingcol@gmail.com')
        print(f"✅ Utilisateur trouvé: {miguel.email}")
        print(f"📋 Rôle actuel: {miguel.role}")
        print(f"👤 Superutilisateur: {miguel.is_superuser}")
        print(f"🛡️ Staff: {miguel.is_staff}")
        
        # Mettre à jour le rôle
        miguel.role = 'admin'
        miguel.is_superuser = True
        miguel.is_staff = True
        miguel.save()
        
        print(f"🎉 Rôle mis à jour avec succès!")
        print(f"📋 Nouveau rôle: {miguel.role}")
        print(f"👤 Superutilisateur: {miguel.is_superuser}")
        print(f"🛡️ Staff: {miguel.is_staff}")
        
        # Vérifier la méthode is_admin()
        print(f"🔍 Test is_admin(): {miguel.is_admin()}")
        
    except User.DoesNotExist:
        print("❌ Utilisateur Miguel non trouvé!")
        print("📋 Utilisateurs existants:")
        for user in User.objects.all():
            print(f"  - {user.email} ({user.role})")

if __name__ == '__main__':
    fix_admin_role()
