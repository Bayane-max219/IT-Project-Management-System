from django.urls import path
from . import test_views

urlpatterns = [
    path('', test_views.tasks_list, name='tasks_list'),
    path('<int:pk>/', test_views.task_detail, name='task_detail'),
    path('my-tasks/', test_views.my_tasks, name='my_tasks'),
    path('stats/', test_views.task_stats, name='task_stats'),
]
