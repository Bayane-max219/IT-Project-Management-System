from django.contrib import admin
from .models import Pointage, PointageSettings, AbsenceRequest


@admin.register(Pointage)
class PointageAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'arrival_time', 'departure_time', 'is_late', 'late_minutes', 'total_work_hours')
    list_filter = ('date', 'is_late', 'employee')
    search_fields = ('employee__email', 'employee__first_name', 'employee__last_name')
    date_hierarchy = 'date'
    readonly_fields = ('is_late', 'late_minutes', 'total_work_hours', 'break_duration_minutes')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('employee', 'date')
        }),
        ('Horaires', {
            'fields': ('arrival_time', 'break_start', 'break_end', 'departure_time')
        }),
        ('Retard', {
            'fields': ('is_late', 'late_minutes', 'late_reason')
        }),
        ('Statistiques', {
            'fields': ('total_work_hours', 'break_duration_minutes'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
    
    def total_work_hours(self, obj):
        return f"{obj.total_work_hours:.2f}h" if obj.total_work_hours else "N/A"
    total_work_hours.short_description = 'Heures travaillées'


@admin.register(PointageSettings)
class PointageSettingsAdmin(admin.ModelAdmin):
    list_display = ('expected_arrival_time', 'expected_departure_time', 'break_duration_minutes', 'tolerance_minutes')
    
    def has_add_permission(self, request):
        # Permet seulement un seul objet de paramètres
        return not PointageSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AbsenceRequest)
class AbsenceRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'absence_type', 'start_date', 'end_date', 'status', 'duration_days')
    list_filter = ('absence_type', 'status', 'start_date', 'end_date')
    search_fields = ('employee__email', 'employee__first_name', 'employee__last_name', 'reason')
    date_hierarchy = 'start_date'
    readonly_fields = ('duration_days', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('employee', 'absence_type', 'start_date', 'end_date', 'duration_days')
        }),
        ('Détails', {
            'fields': ('reason', 'status')
        }),
        ('Approbation', {
            'fields': ('approved_by', 'approval_notes')
        }),
        ('Dates système', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def duration_days(self, obj):
        return f"{obj.duration_days} jour(s)"
    duration_days.short_description = 'Durée'
