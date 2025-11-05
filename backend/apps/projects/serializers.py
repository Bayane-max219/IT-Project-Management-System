from rest_framework import serializers
from apps.authentication.serializers import UserSerializer
from .models import Project, ProjectTeam


class ProjectTeamSerializer(serializers.ModelSerializer):
    developer = UserSerializer(read_only=True)
    developer_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ProjectTeam
        fields = ['id', 'developer', 'developer_id', 'role_in_project', 'joined_at']


class ProjectSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    client_id = serializers.IntegerField(write_only=True)
    project_manager = UserSerializer(read_only=True)
    project_manager_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    team_members = ProjectTeamSerializer(many=True, read_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'client', 'client_id',
            'project_manager', 'project_manager_id', 'status', 'priority',
            'start_date', 'end_date', 'actual_end_date', 'budget',
            'progress', 'team_members', 'is_overdue', 'days_remaining',
            'created_at', 'updated_at'
        ]
    
    def validate_client_id(self, value):
        from apps.authentication.models import User
        try:
            client = User.objects.get(id=value, role='client')
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Client invalide.")
    
    def validate_project_manager_id(self, value):
        if value is None:
            return value
        from apps.authentication.models import User
        try:
            manager = User.objects.get(id=value, role__in=['admin', 'developer'])
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Chef de projet invalide.")
    
    def validate(self, attrs):
        if attrs.get('start_date') and attrs.get('end_date'):
            if attrs['start_date'] > attrs['end_date']:
                raise serializers.ValidationError(
                    "La date de début ne peut pas être postérieure à la date de fin."
                )
        return attrs


class ProjectCreateSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True)
    project_manager_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    team_member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'client_id', 'project_manager_id',
            'status', 'priority', 'start_date', 'end_date',
            'budget', 'team_member_ids'
        ]
    
    def validate_client_id(self, value):
        from apps.authentication.models import User
        try:
            client = User.objects.get(id=value, role='client')
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Client invalide.")
    
    def validate_project_manager_id(self, value):
        if value is None:
            return value
        from apps.authentication.models import User
        try:
            manager = User.objects.get(id=value, role__in=['admin', 'developer'])
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Chef de projet invalide.")
    
    def create(self, validated_data):
        team_member_ids = validated_data.pop('team_member_ids', [])
        client_id = validated_data.pop('client_id')
        project_manager_id = validated_data.pop('project_manager_id', None)
        
        # Récupérer les objets utilisateur
        from apps.authentication.models import User
        client = User.objects.get(id=client_id)
        project_manager = User.objects.get(id=project_manager_id) if project_manager_id else None
        
        # Créer le projet
        project = Project.objects.create(
            client=client,
            project_manager=project_manager,
            **validated_data
        )
        
        # Ajouter les membres de l'équipe
        for member_id in team_member_ids:
            try:
                developer = User.objects.get(id=member_id, role='developer')
                ProjectTeam.objects.create(
                    project=project,
                    developer=developer
                )
            except User.DoesNotExist:
                continue
        
        return project


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """Serializer spécialisé pour la mise à jour des projets"""
    client_id = serializers.IntegerField(required=False)
    project_manager_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'client_id', 'project_manager_id', 
            'status', 'priority', 'start_date', 'end_date', 
            'actual_end_date', 'budget', 'progress'
        ]
    
    def validate_client_id(self, value):
        if value is None:
            return value
        from apps.authentication.models import User
        try:
            client = User.objects.get(id=value, role='client')
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Client invalide.")
    
    def validate_project_manager_id(self, value):
        if value is None:
            return value
        from apps.authentication.models import User
        try:
            manager = User.objects.get(id=value, role__in=['admin', 'developer'])
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Chef de projet invalide.")
    
    def validate(self, attrs):
        start_date = attrs.get('start_date') or (self.instance.start_date if self.instance else None)
        end_date = attrs.get('end_date') or (self.instance.end_date if self.instance else None)
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                "La date de début ne peut pas être postérieure à la date de fin."
            )
        return attrs
    
    def update(self, instance, validated_data):
        # Gérer les clés étrangères
        if 'client_id' in validated_data:
            from apps.authentication.models import User
            client_id = validated_data.pop('client_id')
            if client_id:
                instance.client = User.objects.get(id=client_id)
            else:
                instance.client = None
        
        if 'project_manager_id' in validated_data:
            from apps.authentication.models import User
            manager_id = validated_data.pop('project_manager_id')
            if manager_id:
                instance.project_manager = User.objects.get(id=manager_id)
            else:
                instance.project_manager = None
        
        # Mettre à jour les autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class ProjectStatsSerializer(serializers.Serializer):
    total_projects = serializers.IntegerField()
    active_projects = serializers.IntegerField()
    completed_projects = serializers.IntegerField()
    overdue_projects = serializers.IntegerField()
    projects_by_status = serializers.DictField()
    projects_by_priority = serializers.DictField()
