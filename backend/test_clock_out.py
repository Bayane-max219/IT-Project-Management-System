#!/usr/bin/env python
"""
Script pour tester et déboguer le pointage de départ (clock-out)
"""
import os
import sys
import django
from datetime import datetime, date, time

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage, PointageSettings
from apps.authentication.models import User
from django.utils import timezone

def test_clock_out():
    """Tester le pointage de départ"""
    print("\n" + "="*80)
    print("  TEST POINTAGE DE DÉPART (CLOCK-OUT)")
    print("="*80)
    
    # 1. Récupérer les paramètres
    print("\n📋 1. PARAMÈTRES")
    print("─"*80)
    
    try:
        settings = PointageSettings.objects.first()
        if not settings:
            print("❌ ERREUR: Aucun paramètre trouvé !")
            return
        
        print(f"✅ Heure départ attendue: {settings.expected_departure_time}")
        print(f"✅ Tolérance: {settings.tolerance_minutes} minutes")
        
        # Calculer les limites
        expected_departure = datetime.combine(date.today(), settings.expected_departure_time)
        early_limit = expected_departure - timezone.timedelta(minutes=settings.tolerance_minutes)
        late_limit = expected_departure + timezone.timedelta(minutes=settings.tolerance_minutes)
        
        print(f"   Limite anticipée: {early_limit.time()}")
        print(f"   Limite retard: {late_limit.time()}")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return
    
    # 2. Trouver le pointage d'aujourd'hui
    print("\n📅 2. POINTAGE D'AUJOURD'HUI")
    print("─"*80)
    
    today = date.today()
    pointages = Pointage.objects.filter(date=today)
    
    if not pointages.exists():
        print("❌ Aucun pointage aujourd'hui")
        print("   Solution: Pointez d'abord votre arrivée")
        return
    
    for pointage in pointages:
        print(f"\n  Développeur: {pointage.employee.first_name} {pointage.employee.last_name}")
        print(f"  Arrivée: {pointage.arrival_time}")
        print(f"  Départ: {pointage.departure_time or '❌ Non pointé'}")
        
        if pointage.departure_time:
            print(f"  ⚠️  Départ déjà pointé à {pointage.departure_time}")
            continue
        
        # 3. Simuler un pointage de départ
        print("\n🧪 3. SIMULATION POINTAGE DÉPART")
        print("─"*80)
        
        now = timezone.now().time()
        print(f"  Heure actuelle: {now}")
        
        # Vérifier si c'est anticipé ou en retard
        if now < early_limit.time():
            minutes_early = int((expected_departure - datetime.combine(today, now)).total_seconds() / 60)
            print(f"  ⚠️  DÉPART ANTICIPÉ de {minutes_early} minutes")
            print(f"  → Une justification sera demandée")
            print(f"  → Le frontend doit envoyer: {{ 'reason': 'votre raison' }}")
        elif now > late_limit.time():
            minutes_late = int((datetime.combine(today, now) - expected_departure).total_seconds() / 60)
            print(f"  ⚠️  DÉPART EN RETARD de {minutes_late} minutes")
            print(f"  → Une justification sera demandée")
            print(f"  → Le frontend doit envoyer: {{ 'reason': 'votre raison' }}")
        else:
            print(f"  ✅ DÉPART À L'HEURE")
            print(f"  → Aucune justification nécessaire")
        
        # 4. Tester la requête
        print("\n🔍 4. TEST DE LA REQUÊTE")
        print("─"*80)
        
        print(f"  Endpoint: POST /api/pointage/clock-out/")
        print(f"  User: {pointage.employee.email}")
        print(f"  Pointage ID: {pointage.id}")
        
        # Vérifier les conditions
        errors = []
        
        if not pointage.arrival_time:
            errors.append("❌ Pas d'heure d'arrivée")
        
        if pointage.departure_time:
            errors.append("❌ Départ déjà pointé")
        
        if errors:
            print("\n  ERREURS DÉTECTÉES:")
            for error in errors:
                print(f"    {error}")
        else:
            print("\n  ✅ Toutes les conditions sont remplies")
            print(f"  ✅ Le pointage de départ devrait fonctionner")
    
    print("\n" + "="*80)
    print("✅ TEST TERMINÉ")
    print("="*80 + "\n")

if __name__ == '__main__':
    test_clock_out()
