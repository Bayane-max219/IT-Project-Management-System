from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, time, timedelta
from apps.authentication.serializers import UserSerializer
from .models import Pointage, PointageSettings, AbsenceRequest


class PointageSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.IntegerField(write_only=True, required=False)
    total_work_hours = serializers.ReadOnlyField()
    break_duration_minutes = serializers.ReadOnlyField()
    arrival_status_display = serializers.CharField(source='get_arrival_status_display', read_only=True)
    departure_status_display = serializers.CharField(source='get_departure_status_display', read_only=True)
    
    class Meta:
        model = Pointage
        fields = [
            # Informations de base
            'id', 'employee', 'employee_id', 'date', 
            
            # Horaires
            'arrival_time', 'break_start', 'break_end', 'departure_time',
            
            # Statuts
            'arrival_status', 'arrival_status_display',
            'departure_status', 'departure_status_display',
            
            # Justifications
            'late_reason', 'early_departure_reason', 'early_arrival_notes',
            
            # Métriques
            'late_minutes', 'early_departure_minutes', 'early_arrival_minutes',
            'total_work_hours', 'break_duration_minutes',
            
            # Validation
            'is_justified', 'justification_approved', 'approved_by', 'approval_notes',
            
            # Métadonnées
            'created_at', 'updated_at',
            
            # Rétrocompatibilité
            'is_late', 'notes'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'arrival_status', 'departure_status',
            'late_minutes', 'early_departure_minutes', 'early_arrival_minutes',
            'is_justified', 'justification_approved', 'approved_by',
            'arrival_status_display', 'departure_status_display',
            'is_late'  # Rétrocompatibilité
        ]
    
    def validate(self, attrs):
        # Récupérer les paramètres de pointage
        settings = PointageSettings.get_settings()
        
        # Validation des heures
        if attrs.get('break_start') and attrs.get('break_end'):
            if attrs['break_start'] >= attrs['break_end']:
                raise serializers.ValidationError(
                    "L'heure de fin de pause doit être postérieure à l'heure de début."
                )
        
        if attrs.get('arrival_time') and attrs.get('departure_time'):
            if attrs['arrival_time'] >= attrs['departure_time']:
                raise serializers.ValidationError(
                    "L'heure de départ doit être postérieure à l'heure d'arrivée."
                )
        
        # Validation des retards et des arrivées anticipées
        date = attrs.get('date', getattr(self.instance, 'date', timezone.now().date()))
        
        # Vérification des retards d'arrivée
        if 'arrival_time' in attrs:
            arrival_time = attrs['arrival_time']
            tolerance_time = (
                datetime.combine(date, settings.expected_arrival_time) + 
                timezone.timedelta(minutes=settings.tolerance_minutes)
            ).time()
            
            # Si en retard, vérifier qu'une raison est fournie
            if arrival_time > tolerance_time and not attrs.get('late_reason'):
                raise serializers.ValidationError({
                    'late_reason': "Veuillez fournir une raison pour votre retard."
                })
        
        # Vérification des départs anticipés
        if 'departure_time' in attrs and 'arrival_time' in attrs:
            departure_time = attrs['departure_time']
            tolerance_time = (
                datetime.combine(date, settings.expected_departure_time) - 
                timezone.timedelta(minutes=settings.tolerance_minutes)
            ).time()
            
            # Si départ anticipé, vérifier qu'une raison est fournie
            if (departure_time < tolerance_time and 
                departure_time > attrs.get('arrival_time', time(0, 0)) and
                not attrs.get('early_departure_reason')):
                raise serializers.ValidationError({
                    'early_departure_reason': "Veuillez fournir une raison pour votre départ anticipé."
                })
        
        return attrs
    
    def create(self, validated_data):
        # Si employee_id n'est pas fourni, utiliser l'utilisateur connecté
        if 'employee_id' not in validated_data:
            validated_data['employee'] = self.context['request'].user
        else:
            from apps.authentication.models import User
            try:
                employee = User.objects.get(id=validated_data.pop('employee_id'), role='developer')
                validated_data['employee'] = employee
            except User.DoesNotExist:
                raise serializers.ValidationError("Employé invalide.")
        
        return super().create(validated_data)


class PointageSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointageSettings
        fields = [
            'id', 'expected_arrival_time', 'expected_departure_time',
            'break_duration_minutes', 'tolerance_minutes', 'working_days',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AbsenceRequestSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.IntegerField(write_only=True, required=False)
    approved_by = UserSerializer(read_only=True)
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = AbsenceRequest
        fields = [
            'id', 'employee', 'employee_id', 'absence_type', 'start_date',
            'end_date', 'reason', 'status', 'approved_by', 'approval_notes',
            'duration_days', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'approved_by', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        if attrs.get('start_date') and attrs.get('end_date'):
            if attrs['start_date'] > attrs['end_date']:
                raise serializers.ValidationError(
                    "La date de début ne peut pas être postérieure à la date de fin."
                )
        return attrs
    
    def create(self, validated_data):
        # Si employee_id n'est pas fourni, utiliser l'utilisateur connecté
        if 'employee_id' not in validated_data:
            validated_data['employee'] = self.context['request'].user
        else:
            from apps.authentication.models import User
            try:
                employee = User.objects.get(id=validated_data.pop('employee_id'), role='developer')
                validated_data['employee'] = employee
            except User.DoesNotExist:
                raise serializers.ValidationError("Employé invalide.")
        
        return super().create(validated_data)


class PointageStatsSerializer(serializers.Serializer):
    # Informations de base
    date = serializers.DateField()
    total_employees = serializers.IntegerField()
    present_today = serializers.IntegerField()
    late_today = serializers.IntegerField()
    early_departures_today = serializers.IntegerField()
    absent_today = serializers.IntegerField()
    attendance_rate = serializers.FloatField()
    
    # Horaires
    average_arrival_time = serializers.CharField(allow_null=True)
    total_work_hours_today = serializers.FloatField()
    
    # Détails
    late_employees = serializers.ListField()
    early_departures = serializers.ListField()
    
    # Statistiques de justification
    justification_stats = serializers.DictField()
    
    # Rétrocompatibilité
    late_employees_today = serializers.SerializerMethodField()
    
    def get_late_employees_today(self, obj):
        # Rétrocompatibilité avec l'ancien format
        return [{
            'name': f"{emp.get('full_name', '')}",
            'minutes_late': emp.get('late_minutes', 0)
        } for emp in obj.get('late_employees', [])]
