from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListCreateView.as_view(), name='task_list_create'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('my-tasks/', views.MyTasksView.as_view(), name='my_tasks'),
    path('<int:task_id>/status/', views.update_task_status, name='update_task_status'),
    path('<int:task_id>/comments/', views.TaskCommentListCreateView.as_view(), name='task_comments'),
    path('stats/', views.task_stats, name='task_stats'),
]
