#!/usr/bin/env python
"""
Debug des APIs de pointage
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

print("🔍 DEBUG APIs POINTAGE")

# Créer un client de test
client = Client()

# Trouver un développeur
dev = User.objects.filter(role='developer').first()
if not dev:
    print("❌ Aucun développeur trouvé")
    sys.exit(1)

print(f"👤 Développeur: {dev.first_name} {dev.last_name}")

# Se connecter
client.force_login(dev)

print("\n📋 TEST DES ENDPOINTS:")

# Test 1: /api/pointage/today/
print("\n1. Test GET /api/pointage/today/")
response = client.get('/api/pointage/today/')
print(f"   Status: {response.status_code}")
if response.status_code != 200:
    print(f"   Erreur: {response.content.decode()}")
else:
    print(f"   ✅ Succès: {response.json()}")

# Test 2: /api/pointage/clock-in/
print("\n2. Test POST /api/pointage/clock-in/")
response = client.post('/api/pointage/clock-in/', {})
print(f"   Status: {response.status_code}")
if response.status_code not in [200, 201]:
    print(f"   Erreur: {response.content.decode()}")
else:
    print(f"   ✅ Succès: {response.json()}")

# Test 3: Vérifier les pointages existants
print("\n3. Pointages existants aujourd'hui:")
from apps.pointage.models import Pointage
today = date.today()
pointages = Pointage.objects.filter(date=today)
print(f"   Nombre: {pointages.count()}")
for p in pointages:
    print(f"   • {p.employee.first_name}: {p.arrival_time}")

print("\n💡 Si les tests échouent, il y a un problème dans le backend")
print("   Si les tests réussissent, le problème est dans le frontend")
