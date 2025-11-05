#!/usr/bin/env python
"""
Script pour réinitialiser le mot de passe d'un développeur
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("\n" + "="*80)
print("  RÉINITIALISATION MOT DE PASSE DÉVELOPPEUR")
print("="*80)

# Récupérer tous les développeurs
developers = User.objects.filter(role='developer')

if not developers.exists():
    print("❌ Aucun développeur trouvé")
    sys.exit(1)

print("Développeurs trouvés:")
for i, dev in enumerate(developers, 1):
    print(f"{i}. {dev.first_name} {dev.last_name} ({dev.email})")

print("\n" + "="*80)
print("  RÉINITIALISATION AUTOMATIQUE")
print("="*80)

# Réinitialiser tous les développeurs avec le mot de passe "dev123"
nouveau_password = "dev123"

for dev in developers:
    dev.set_password(nouveau_password)
    dev.save()
    print(f"✅ {dev.first_name} {dev.last_name}")
    print(f"   📧 Email: {dev.email}")
    print(f"   🔑 Nouveau mot de passe: {nouveau_password}")
    print("-" * 60)

print(f"\n🎉 TOUS LES DÉVELOPPEURS ONT LE MOT DE PASSE: {nouveau_password}")
print("\nVous pouvez maintenant vous connecter avec:")
print("- Email du développeur")
print(f"- Mot de passe: {nouveau_password}")

print("\n💡 Pour changer individuellement, utilisez:")
print("   python voir_mot_de_passe_dev.py")
