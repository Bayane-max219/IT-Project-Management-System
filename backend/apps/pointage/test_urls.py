from django.urls import path
from . import test_views

urlpatterns = [
    path('stats/', test_views.pointage_stats, name='pointage_stats'),
]
