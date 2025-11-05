#!/usr/bin/env python
"""
Script de diagnostic pour le système de pointage
"""
import os
import sys
import django
from datetime import datetime, date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage, PointageSettings
from apps.authentication.models import User

def diagnostic_pointage():
    """Diagnostiquer les problèmes de pointage"""
    print("\n" + "="*80)
    print("  DIAGNOSTIC SYSTÈME DE POINTAGE")
    print("="*80)
    
    # 1. Vérifier les paramètres de pointage
    print("\n📋 1. PARAMÈTRES DE POINTAGE")
    print("─"*80)
    
    try:
        settings = PointageSettings.objects.first()
        if settings:
            print(f"✅ Paramètres trouvés")
            print(f"   Heure arrivée attendue: {settings.expected_arrival_time}")
            print(f"   Heure départ attendue: {settings.expected_departure_time}")
            print(f"   Tolérance: {settings.tolerance_minutes} minutes")
            print(f"   Durée pause: {settings.break_duration_minutes} minutes")
        else:
            print("❌ ERREUR: Aucun paramètre de pointage trouvé !")
            print("   Solution: Créer les paramètres via l'admin Django")
            return
    except Exception as e:
        print(f"❌ ERREUR lors de la récupération des paramètres: {e}")
        return
    
    # 2. Vérifier les développeurs
    print("\n👥 2. DÉVELOPPEURS ACTIFS")
    print("─"*80)
    
    developers = User.objects.filter(role='developer', is_active=True)
    print(f"Total: {developers.count()} développeur(s)")
    
    for dev in developers:
        print(f"  • {dev.first_name} {dev.last_name} ({dev.email})")
    
    # 3. Vérifier les pointages d'aujourd'hui
    print("\n📅 3. POINTAGES D'AUJOURD'HUI")
    print("─"*80)
    
    today = date.today()
    today_pointages = Pointage.objects.filter(date=today)
    
    if today_pointages.exists():
        print(f"Total: {today_pointages.count()} pointage(s)")
        
        for pointage in today_pointages:
            print(f"\n  Développeur: {pointage.employee.first_name} {pointage.employee.last_name}")
            print(f"  Date: {pointage.date}")
            print(f"  Arrivée: {pointage.arrival_time or '❌ Non pointé'}")
            print(f"  Départ: {pointage.departure_time or '❌ Non pointé'}")
            print(f"  Pause début: {pointage.break_start or '❌ Non pointé'}")
            print(f"  Pause fin: {pointage.break_end or '❌ Non pointé'}")
            
            if pointage.late_reason:
                print(f"  ⚠️  Retard: {pointage.late_reason}")
            if pointage.early_departure_reason:
                print(f"  ⚠️  Départ anticipé: {pointage.early_departure_reason}")
    else:
        print("Aucun pointage aujourd'hui")
    
    # 4. Vérifier les pointages incomplets
    print("\n⚠️  4. POINTAGES INCOMPLETS")
    print("─"*80)
    
    incomplete = Pointage.objects.filter(
        date=today,
        arrival_time__isnull=False,
        departure_time__isnull=True
    )
    
    if incomplete.exists():
        print(f"Total: {incomplete.count()} pointage(s) incomplet(s)")
        for p in incomplete:
            print(f"  • {p.employee.first_name} {p.employee.last_name} - Arrivée: {p.arrival_time}, Départ: Non pointé")
    else:
        print("✅ Aucun pointage incomplet")
    
    # 5. Vérifier les erreurs potentielles
    print("\n🔍 5. VÉRIFICATION DES ERREURS POTENTIELLES")
    print("─"*80)
    
    errors = []
    
    # Vérifier si des pointages ont des pauses sans arrivée
    invalid_breaks = Pointage.objects.filter(
        date=today,
        arrival_time__isnull=True,
        break_start__isnull=False
    )
    
    if invalid_breaks.exists():
        errors.append(f"❌ {invalid_breaks.count()} pointage(s) avec pause mais sans arrivée")
    
    # Vérifier si des pointages ont un départ sans arrivée
    invalid_departures = Pointage.objects.filter(
        date=today,
        arrival_time__isnull=True,
        departure_time__isnull=False
    )
    
    if invalid_departures.exists():
        errors.append(f"❌ {invalid_departures.count()} pointage(s) avec départ mais sans arrivée")
    
    if errors:
        for error in errors:
            print(f"  {error}")
    else:
        print("✅ Aucune erreur détectée")
    
    # 6. Tester la création d'un pointage
    print("\n🧪 6. TEST DE CRÉATION DE POINTAGE")
    print("─"*80)
    
    if developers.exists():
        test_dev = developers.first()
        print(f"Test avec: {test_dev.first_name} {test_dev.last_name}")
        
        # Vérifier si un pointage existe déjà aujourd'hui
        existing = Pointage.objects.filter(employee=test_dev, date=today).first()
        
        if existing:
            print(f"✅ Pointage existant trouvé (ID: {existing.id})")
            print(f"   État: Arrivée={existing.arrival_time}, Départ={existing.departure_time}")
        else:
            print("ℹ️  Aucun pointage aujourd'hui pour cet utilisateur")
            print("   Un pointage sera créé lors du premier clock-in")
    
    print("\n" + "="*80)
    print("✅ DIAGNOSTIC TERMINÉ")
    print("="*80 + "\n")

if __name__ == '__main__':
    diagnostic_pointage()
