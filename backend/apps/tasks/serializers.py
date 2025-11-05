from rest_framework import serializers
from apps.authentication.serializers import UserSerializer
from apps.projects.serializers import ProjectSerializer
from .models import Task, TaskComment, TaskAttachment


class TaskCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskComment
        fields = ['id', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class TaskAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskAttachment
        fields = ['id', 'file', 'filename', 'uploaded_by', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at']


class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    project_id = serializers.IntegerField(write_only=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    created_by = UserSerializer(read_only=True)
    comments = TaskCommentSerializer(many=True, read_only=True)
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project', 'project_id',
            'assigned_to', 'assigned_to_id', 'created_by', 'status',
            'priority', 'estimated_hours', 'actual_hours', 'start_date',
            'due_date', 'completed_at', 'comments', 'attachments',
            'is_overdue', 'days_remaining', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'completed_at', 'created_at', 'updated_at']
    
    def validate_project_id(self, value):
        from apps.projects.models import Project
        try:
            project = Project.objects.get(id=value)
            # Vérifier que l'utilisateur a accès à ce projet
            user = self.context['request'].user
            if not user.is_admin():
                if user.is_client() and project.client != user:
                    raise serializers.ValidationError("Accès refusé à ce projet.")
                elif user.is_developer():
                    from django.db.models import Q
                    if not Project.objects.filter(
                        Q(id=value) & (Q(project_manager=user) | Q(team_members__developer=user))
                    ).exists():
                        raise serializers.ValidationError("Accès refusé à ce projet.")
            return value
        except Project.DoesNotExist:
            raise serializers.ValidationError("Projet invalide.")
    
    def validate_assigned_to_id(self, value):
        if value is None:
            return value
        from apps.authentication.models import User
        try:
            developer = User.objects.get(id=value, role='developer')
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Développeur invalide.")
    
    def validate(self, attrs):
        if attrs.get('start_date') and attrs.get('due_date'):
            if attrs['start_date'] > attrs['due_date']:
                raise serializers.ValidationError(
                    "La date de début ne peut pas être postérieure à la date limite."
                )
        return attrs


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'project', 'assigned_to',
            'status', 'priority', 'estimated_hours', 'start_date', 'due_date'
        ]
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Serializer spécialisé pour la mise à jour des tâches"""
    project_id = serializers.IntegerField(required=False)
    assigned_to_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'project_id', 'assigned_to_id',
            'status', 'priority', 'estimated_hours', 'actual_hours',
            'start_date', 'due_date'
        ]
    
    def validate_project_id(self, value):
        if value is None:
            return value
        from apps.projects.models import Project
        try:
            project = Project.objects.get(id=value)
            # Vérifier que l'utilisateur a accès à ce projet
            user = self.context['request'].user
            if not user.is_admin():
                if user.is_client() and project.client != user:
                    raise serializers.ValidationError("Accès refusé à ce projet.")
                elif user.is_developer():
                    from django.db.models import Q
                    if not Project.objects.filter(
                        Q(id=value) & (Q(project_manager=user) | Q(team_members__developer=user))
                    ).exists():
                        raise serializers.ValidationError("Accès refusé à ce projet.")
            return value
        except Project.DoesNotExist:
            raise serializers.ValidationError("Projet invalide.")
    
    def validate_assigned_to_id(self, value):
        if value is None:
            return value
        from apps.authentication.models import User
        try:
            developer = User.objects.get(id=value, role='developer')
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Développeur invalide.")
    
    def validate(self, attrs):
        start_date = attrs.get('start_date') or (self.instance.start_date if self.instance else None)
        due_date = attrs.get('due_date') or (self.instance.due_date if self.instance else None)
        
        if start_date and due_date and start_date > due_date:
            raise serializers.ValidationError(
                "La date de début ne peut pas être postérieure à la date limite."
            )
        return attrs
    
    def update(self, instance, validated_data):
        # Gérer les clés étrangères
        if 'project_id' in validated_data:
            from apps.projects.models import Project
            project_id = validated_data.pop('project_id')
            if project_id:
                instance.project = Project.objects.get(id=project_id)
        
        if 'assigned_to_id' in validated_data:
            from apps.authentication.models import User
            assigned_to_id = validated_data.pop('assigned_to_id')
            if assigned_to_id:
                instance.assigned_to = User.objects.get(id=assigned_to_id)
            else:
                instance.assigned_to = None
        
        # Gérer le statut et la date de completion
        if 'status' in validated_data:
            new_status = validated_data['status']
            if new_status == 'TERMINEE' and instance.status != 'TERMINEE':
                from django.utils import timezone
                instance.completed_at = timezone.now()
            elif new_status != 'TERMINEE' and instance.status == 'TERMINEE':
                instance.completed_at = None
        
        # Mettre à jour les autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class TaskStatsSerializer(serializers.Serializer):
    total_tasks = serializers.IntegerField()
    todo_tasks = serializers.IntegerField()
    in_progress_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()
    tasks_by_status = serializers.DictField()
    tasks_by_priority = serializers.DictField()
    tasks_by_developer = serializers.DictField()
