#!/usr/bin/env python
import os
import django
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.pointage.models import Pointage
from datetime import date

today = date.today()
pointages = Pointage.objects.filter(date=today, arrival_status=Pointage.STATUS_LATE)

print("API SIMULATION:")
late_employees = []
for p in pointages:
    emp = {
        'id': p.employee.id,
        'full_name': f"{p.employee.first_name} {p.employee.last_name}",
        'late_reason': p.late_reason,
        'late_minutes': p.late_minutes
    }
    late_employees.append(emp)

print(json.dumps(late_employees, indent=2, default=str))
