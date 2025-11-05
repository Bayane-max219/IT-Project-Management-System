from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from .models import Project, ProjectTeam
from .serializers import (
    ProjectSerializer, ProjectCreateSerializer, ProjectUpdateSerializer,
    ProjectTeamSerializer, ProjectStatsSerializer
)


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Project.objects.all().select_related('client', 'project_manager')
        elif user.is_client():
            return Project.objects.filter(client=user).select_related('project_manager')
        else:  # developer
            return Project.objects.filter(
                Q(project_manager=user) | Q(team_members__developer=user)
            ).distinct().select_related('client', 'project_manager')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        if not self.request.user.is_admin():
            raise permissions.PermissionDenied("Seuls les admins peuvent créer des projets.")
        serializer.save()


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Project.objects.all()
        elif user.is_client():
            return Project.objects.filter(client=user)
        else:  # developer
            return Project.objects.filter(
                Q(project_manager=user) | Q(team_members__developer=user)
            ).distinct()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProjectUpdateSerializer
        return ProjectSerializer
    
    def perform_update(self, serializer):
        user = self.request.user
        if not user.is_admin() and not user == serializer.instance.project_manager:
            raise permissions.PermissionDenied(
                "Seuls les admins et chefs de projet peuvent modifier les projets."
            )
        serializer.save()
    
    def perform_destroy(self, instance):
        if not self.request.user.is_admin():
            raise permissions.PermissionDenied("Seuls les admins peuvent supprimer des projets.")
        instance.delete()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_team_member(request, project_id):
    if not request.user.is_admin():
        return Response(
            {'error': 'Permission refusée'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        project = Project.objects.get(id=project_id)
        developer_id = request.data.get('developer_id')
        role_in_project = request.data.get('role_in_project', 'Développeur')
        
        from apps.authentication.models import User
        developer = User.objects.get(id=developer_id, role='developer')
        
        team_member, created = ProjectTeam.objects.get_or_create(
            project=project,
            developer=developer,
            defaults={'role_in_project': role_in_project}
        )
        
        if not created:
            return Response(
                {'error': 'Ce développeur fait déjà partie de l\'équipe'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ProjectTeamSerializer(team_member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Project.DoesNotExist:
        return Response({'error': 'Projet non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'Développeur non trouvé'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_team_member(request, project_id, member_id):
    if not request.user.is_admin():
        return Response(
            {'error': 'Permission refusée'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        team_member = ProjectTeam.objects.get(
            project_id=project_id, 
            id=member_id
        )
        team_member.delete()
        return Response({'message': 'Membre retiré de l\'équipe'})
        
    except ProjectTeam.DoesNotExist:
        return Response(
            {'error': 'Membre d\'équipe non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def project_stats(request):
    if not request.user.is_admin():
        return Response(
            {'error': 'Permission refusée'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(
        status__in=['planning', 'in_progress', 'testing']
    ).count()
    completed_projects = Project.objects.filter(status='completed').count()
    overdue_projects = Project.objects.filter(
        end_date__lt=timezone.now().date(),
        status__in=['planning', 'in_progress', 'testing']
    ).count()
    
    projects_by_status = dict(
        Project.objects.values('status').annotate(count=Count('id')).values_list('status', 'count')
    )
    
    projects_by_priority = dict(
        Project.objects.values('priority').annotate(count=Count('id')).values_list('priority', 'count')
    )
    
    stats = {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'overdue_projects': overdue_projects,
        'projects_by_status': projects_by_status,
        'projects_by_priority': projects_by_priority,
    }
    
    serializer = ProjectStatsSerializer(stats)
    return Response(serializer.data)
