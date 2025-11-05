from django.contrib import admin
from .models import Project, ProjectTeam


class ProjectTeamInline(admin.TabularInline):
    model = ProjectTeam
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'project_manager', 'status', 'priority', 'progress', 'start_date', 'end_date')
    list_filter = ('status', 'priority', 'start_date', 'end_date')
    search_fields = ('name', 'client__email', 'project_manager__email')
    date_hierarchy = 'start_date'
    inlines = [ProjectTeamInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'description', 'client', 'project_manager')
        }),
        ('Planification', {
            'fields': ('status', 'priority', 'start_date', 'end_date', 'actual_end_date')
        }),
        ('Budget et progression', {
            'fields': ('budget', 'progress')
        }),
    )


@admin.register(ProjectTeam)
class ProjectTeamAdmin(admin.ModelAdmin):
    list_display = ('project', 'developer', 'role_in_project', 'joined_at')
    list_filter = ('role_in_project', 'joined_at')
    search_fields = ('project__name', 'developer__email')
