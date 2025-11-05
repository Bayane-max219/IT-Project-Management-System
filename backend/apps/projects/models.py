from django.db import models
from django.conf import settings


class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planification'),
        ('in_progress', 'En cours'),
        ('testing', 'Tests'),
        ('completed', 'Terminé'),
        ('on_hold', 'En pause'),
        ('cancelled', 'Annulé'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom du projet")
    description = models.TextField(verbose_name="Description")
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_projects',
        limit_choices_to={'role': 'client'},
        verbose_name="Client"
    )
    project_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_projects',
        limit_choices_to={'role__in': ['admin', 'developer']},
        verbose_name="Chef de projet"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planning',
        verbose_name="Statut"
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name="Priorité"
    )
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin prévue")
    actual_end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin réelle")
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Budget"
    )
    progress = models.IntegerField(default=0, verbose_name="Progression (%)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'projects'
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.status not in ['completed', 'cancelled']:
            return timezone.now().date() > self.end_date
        return False
    
    @property
    def days_remaining(self):
        from django.utils import timezone
        if self.status not in ['completed', 'cancelled']:
            delta = self.end_date - timezone.now().date()
            return delta.days
        return 0
    
    def update_progress(self):
        """Calcule automatiquement la progression basée sur les tâches"""
        tasks = self.tasks.all()
        if not tasks:
            self.progress = 0
        else:
            completed_tasks = tasks.filter(status='completed').count()
            self.progress = (completed_tasks / tasks.count()) * 100
        self.save()


class ProjectTeam(models.Model):
    """Table de liaison pour les membres de l'équipe projet"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='team_members')
    developer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'developer'}
    )
    role_in_project = models.CharField(
        max_length=100,
        default='Développeur',
        verbose_name="Rôle dans le projet"
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'project_teams'
        unique_together = ['project', 'developer']
        verbose_name = 'Membre équipe'
        verbose_name_plural = 'Membres équipe'
    
    def __str__(self):
        return f"{self.developer.full_name} - {self.project.name}"
