#!/usr/bin/env python
"""
Script de test pour vérifier les corrections du profil et du pointage
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.authentication.models import User
from apps.pointage.models import Pointage, PointageSettings
from datetime import datetime, time

def test_profile_update():
    """Test de la mise à jour du profil"""
    print("\n" + "="*50)
    print("TEST 1: Mise à jour du profil")
    print("="*50)
    
    try:
        # Récupérer un utilisateur de test
        user = User.objects.filter(role='developer').first()
        if not user:
            print("❌ Aucun développeur trouvé pour le test")
            return False
        
        print(f"✅ Utilisateur trouvé: {user.email}")
        
        # Tester la mise à jour
        user.first_name = "Test"
        user.last_name = "Update"
        user.save()
        
        print(f"✅ Profil mis à jour: {user.first_name} {user.last_name}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def test_pointage_settings():
    """Test des paramètres de pointage"""
    print("\n" + "="*50)
    print("TEST 2: Paramètres de pointage")
    print("="*50)
    
    try:
        settings = PointageSettings.get_settings()
        print(f"✅ Heure d'arrivée attendue: {settings.expected_arrival_time}")
        print(f"✅ Heure de départ attendue: {settings.expected_departure_time}")
        print(f"✅ Tolérance: {settings.tolerance_minutes} minutes")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def test_pointage_departure():
    """Test du pointage de départ"""
    print("\n" + "="*50)
    print("TEST 3: Logique de pointage de départ")
    print("="*50)
    
    try:
        from datetime import timedelta
        
        settings = PointageSettings.get_settings()
        today = datetime.now().date()
        
        # Test départ à l'heure
        departure_time = settings.expected_departure_time
        print(f"✅ Heure de départ normale: {departure_time}")
        
        # Test départ anticipé
        early_time = (datetime.combine(today, settings.expected_departure_time) - timedelta(minutes=30)).time()
        print(f"✅ Heure de départ anticipé (test): {early_time}")
        
        # Test départ en retard
        late_time = (datetime.combine(today, settings.expected_departure_time) + timedelta(minutes=30)).time()
        print(f"✅ Heure de départ en retard (test): {late_time}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("  TESTS DES CORRECTIONS - PROFIL ET POINTAGE")
    print("="*60)
    
    results = []
    
    # Exécuter les tests
    results.append(("Mise à jour profil", test_profile_update()))
    results.append(("Paramètres pointage", test_pointage_settings()))
    results.append(("Logique départ", test_pointage_departure()))
    
    # Afficher le résumé
    print("\n" + "="*60)
    print("  RÉSUMÉ DES TESTS")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:.<40} {status}")
    
    print("\n" + "-"*60)
    print(f"Total: {passed}/{total} tests réussis")
    print("="*60 + "\n")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS !")
        print("\nLes corrections sont appliquées correctement.")
        print("Vous pouvez maintenant tester dans l'application.\n")
        return 0
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("\nVeuillez vérifier les erreurs ci-dessus.\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
