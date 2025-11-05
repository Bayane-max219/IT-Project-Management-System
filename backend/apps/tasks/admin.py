from django.contrib import admin
from .models import Task, TaskComment, TaskAttachment


class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 1
    readonly_fields = ('created_at',)


class TaskAttachmentInline(admin.TabularInline):
    model = TaskAttachment
    extra = 1
    readonly_fields = ('uploaded_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'priority', 'due_date', 'is_overdue')
    list_filter = ('status', 'priority', 'project', 'assigned_to', 'due_date')
    search_fields = ('title', 'description', 'project__name', 'assigned_to__email')
    date_hierarchy = 'created_at'
    inlines = [TaskCommentInline, TaskAttachmentInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'description', 'project', 'assigned_to', 'created_by')
        }),
        ('Statut et priorité', {
            'fields': ('status', 'priority')
        }),
        ('Planification', {
            'fields': ('estimated_hours', 'actual_hours', 'start_date', 'due_date')
        }),
        ('Dates système', {
            'fields': ('completed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'En retard'


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('task__title', 'author__email', 'content')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'task', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'uploaded_by')
    search_fields = ('filename', 'task__title', 'uploaded_by__email')
    readonly_fields = ('uploaded_at',)
