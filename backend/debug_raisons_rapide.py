#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage
from datetime import date

today = date.today()
pointages = Pointage.objects.filter(date=today)

print(f"POINTAGES AUJOURD'HUI: {pointages.count()}")
for p in pointages:
    print(f"- {p.employee.first_name}: '{p.late_reason}' (statut: {p.arrival_status})")
