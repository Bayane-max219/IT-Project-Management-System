from django.urls import path
from . import views

urlpatterns = [
    # Pointages CRUD
    path('', views.PointageListCreateView.as_view(), name='pointage_list_create'),
    path('<int:pk>/', views.PointageDetailView.as_view(), name='pointage_detail'),
    path('my-pointages/', views.MyPointageView.as_view(), name='my_pointages'),
    
    # Actions de pointage
    path('clock-in/', views.clock_in, name='clock_in'),
    path('clock-out/', views.clock_out, name='clock_out'),
    path('break-start/', views.break_start, name='break_start'),
    path('break-end/', views.break_end, name='break_end'),
    path('today/', views.today_pointage, name='today_pointage'),
    
    # Statistiques et gestion des justifications
    path('stats/', views.pointage_stats, name='pointage_stats'),
    path('justify/<int:pointage_id>/', views.justify_pointage, name='justify_pointage'),
    path('justifications/pending/', views.pending_justifications, name='pending_justifications'),
    
    # Demandes d'absence
    path('absences/', views.AbsenceRequestListCreateView.as_view(), name='absence_list_create'),
    path('absences/<int:pk>/', views.AbsenceRequestDetailView.as_view(), name='absence_detail'),
    path('absences/<int:absence_id>/approve/', views.approve_absence, name='approve_absence'),
]
