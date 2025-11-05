from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListCreateView.as_view(), name='project_list_create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:project_id>/team/add/', views.add_team_member, name='add_team_member'),
    path('<int:project_id>/team/<int:member_id>/remove/', views.remove_team_member, name='remove_team_member'),
    path('stats/', views.project_stats, name='project_stats'),
]
