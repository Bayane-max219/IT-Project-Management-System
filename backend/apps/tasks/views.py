from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from .models import Task, TaskComment, TaskAttachment
from .serializers import (
    TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer, TaskCommentSerializer,
    TaskAttachmentSerializer, TaskStatsSerializer
)


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.select_related('project', 'assigned_to', 'created_by')
        
        if user.is_admin():
            return queryset
        elif user.is_client():
            return queryset.filter(project__client=user)
        else:  # developer
            return queryset.filter(
                Q(assigned_to=user) | 
                Q(project__project_manager=user) |
                Q(project__team_members__developer=user)
            ).distinct()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.is_client():
            raise permissions.PermissionDenied("Les clients ne peuvent pas créer de tâches.")
        serializer.save(created_by=user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.select_related('project', 'assigned_to', 'created_by')
        
        if user.is_admin():
            return queryset
        elif user.is_client():
            return queryset.filter(project__client=user)
        else:  # developer
            return queryset.filter(
                Q(assigned_to=user) | 
                Q(project__project_manager=user) |
                Q(project__team_members__developer=user)
            ).distinct()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskUpdateSerializer
        return TaskSerializer
    
    def perform_update(self, serializer):
        user = self.request.user
        task = self.get_object()
        
        # Les développeurs ne peuvent modifier que leurs propres tâches
        if user.is_developer() and task.assigned_to != user:
            # Sauf s'ils sont chef de projet
            if task.project.project_manager != user:
                raise permissions.PermissionDenied(
                    "Vous ne pouvez modifier que vos propres tâches."
                )
        
        serializer.save()
    
    def perform_destroy(self, instance):
        user = self.request.user
        if not user.is_admin() and instance.created_by != user:
            raise permissions.PermissionDenied(
                "Seuls les admins et créateurs peuvent supprimer des tâches."
            )
        instance.delete()


class MyTasksView(generics.ListAPIView):
    """Vue pour récupérer les tâches assignées à l'utilisateur connecté"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_developer():
            return Task.objects.filter(assigned_to=user).select_related('project', 'created_by')
        return Task.objects.none()


class TaskCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return TaskComment.objects.filter(task_id=task_id).select_related('author')
    
    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        try:
            task = Task.objects.get(id=task_id)
            # Vérifier l'accès à la tâche
            user = self.request.user
            if not user.is_admin():
                if user.is_client() and task.project.client != user:
                    raise permissions.PermissionDenied("Accès refusé.")
                elif user.is_developer():
                    if not (task.assigned_to == user or 
                           task.project.project_manager == user or
                           task.project.team_members.filter(developer=user).exists()):
                        raise permissions.PermissionDenied("Accès refusé.")
            
            serializer.save(task=task, author=user)
        except Task.DoesNotExist:
            raise permissions.PermissionDenied("Tâche non trouvée.")


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_task_status(request, task_id):
    """Endpoint spécifique pour mettre à jour le statut d'une tâche"""
    try:
        task = Task.objects.get(id=task_id)
        user = request.user
        
        # Vérifier les permissions
        if not user.is_admin():
            if user.is_client():
                return Response(
                    {'error': 'Les clients ne peuvent pas modifier le statut des tâches'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            elif user.is_developer() and task.assigned_to != user:
                if task.project.project_manager != user:
                    return Response(
                        {'error': 'Vous ne pouvez modifier que vos propres tâches'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
        
        new_status = request.data.get('status')
        if new_status not in dict(Task.STATUS_CHOICES):
            return Response(
                {'error': 'Statut invalide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = new_status
        task.save()
        
        serializer = TaskSerializer(task)
        return Response(serializer.data)
        
    except Task.DoesNotExist:
        return Response(
            {'error': 'Tâche non trouvée'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def task_stats(request):
    """Statistiques des tâches pour les admins"""
    if not request.user.is_admin():
        return Response(
            {'error': 'Permission refusée'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    total_tasks = Task.objects.count()
    todo_tasks = Task.objects.filter(status='todo').count()
    in_progress_tasks = Task.objects.filter(status='in_progress').count()
    completed_tasks = Task.objects.filter(status='completed').count()
    overdue_tasks = Task.objects.filter(
        due_date__lt=timezone.now().date(),
        status__in=['todo', 'in_progress', 'testing', 'blocked']
    ).count()
    
    tasks_by_status = dict(
        Task.objects.values('status').annotate(count=Count('id')).values_list('status', 'count')
    )
    
    tasks_by_priority = dict(
        Task.objects.values('priority').annotate(count=Count('id')).values_list('priority', 'count')
    )
    
    # Tâches par développeur
    from apps.authentication.models import User
    tasks_by_developer = {}
    developers = User.objects.filter(role='developer')
    for dev in developers:
        task_count = Task.objects.filter(assigned_to=dev).count()
        if task_count > 0:
            tasks_by_developer[dev.full_name] = task_count
    
    stats = {
        'total_tasks': total_tasks,
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'tasks_by_status': tasks_by_status,
        'tasks_by_priority': tasks_by_priority,
        'tasks_by_developer': tasks_by_developer,
    }
    
    serializer = TaskStatsSerializer(stats)
    return Response(serializer.data)
