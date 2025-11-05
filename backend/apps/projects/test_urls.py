from django.urls import path
from . import test_views, test_stats_views

urlpatterns = [
    path('', test_views.projects_list, name='projects_list'),
    path('<int:pk>/', test_views.project_detail, name='project_detail'),
    path('stats/', test_stats_views.dashboard_stats, name='project_stats'),
    path('stats/dashboard/', test_stats_views.dashboard_stats, name='dashboard_stats'),
    path('stats/by-status/', test_stats_views.projects_by_status, name='projects_by_status'),
    path('stats/tasks-by-developer/', test_stats_views.tasks_by_developer, name='tasks_by_developer'),
]
