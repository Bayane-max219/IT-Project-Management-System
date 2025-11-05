from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import time, datetime, timedelta


class Pointage(models.Model):
    ARRIVAL = 'arrival'
    DEPARTURE = 'departure'
    BREAK_START = 'break_start'
    BREAK_END = 'break_end'
    
    POINTAGE_TYPES = [
        (ARRIVAL, "Arrivée"),
        (DEPARTURE, "Départ"),
        (BREAK_START, "Début pause"),
        (BREAK_END, "Fin pause"),
    ]
    
    STATUS_ON_TIME = 'on_time'
    STATUS_LATE = 'late'
    STATUS_EARLY = 'early'
    
    STATUS_CHOICES = [
        (STATUS_ON_TIME, "À l'heure"),
        (STATUS_LATE, "En retard"),
        (STATUS_EARLY, "En avance"),
    ]
    
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pointages',
        limit_choices_to={'role': 'developer'},
        verbose_name="Employé"
    )
    date = models.DateField(verbose_name="Date")
    
    # Heures de pointage
    arrival_time = models.TimeField(null=True, blank=True, verbose_name="Heure d'arrivée")
    break_start = models.TimeField(null=True, blank=True, verbose_name="Début pause")
    break_end = models.TimeField(null=True, blank=True, verbose_name="Fin pause")
    departure_time = models.TimeField(null=True, blank=True, verbose_name="Heure de départ")
    
    # Statut et retards
    arrival_status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        null=True, 
        blank=True,
        verbose_name="Statut arrivée"
    )
    departure_status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        null=True, 
        blank=True,
        verbose_name="Statut départ"
    )
    
    # Justifications
    late_reason = models.TextField(blank=True, null=True, verbose_name="Raison du retard")
    early_departure_reason = models.TextField(blank=True, null=True, verbose_name="Raison du départ anticipé")
    early_arrival_notes = models.TextField(blank=True, null=True, verbose_name="Notes d'arrivée anticipée")
    
    # Métriques
    late_minutes = models.IntegerField(default=0, verbose_name="Minutes de retard")
    early_departure_minutes = models.IntegerField(default=0, verbose_name="Minutes de départ anticipé")
    early_arrival_minutes = models.IntegerField(default=0, verbose_name="Minutes d'arrivée anticipée")
    total_work_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Heures travaillées")
    
    # Suivi
    is_justified = models.BooleanField(default=False, verbose_name="Justifié")
    justification_approved = models.BooleanField(null=True, verbose_name="Justification approuvée")
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_pointages',
        limit_choices_to={'role': 'admin'},
        verbose_name="Approuvé par"
    )
    approval_notes = models.TextField(blank=True, null=True, verbose_name="Notes d'approbation")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Pour la rétrocompatibilité
    is_late = models.BooleanField(default=False, verbose_name="En retard (déprécié)")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes (déprécié)")
    
    class Meta:
        db_table = 'pointages'
        verbose_name = 'Pointage'
        verbose_name_plural = 'Pointages'
        unique_together = ['employee', 'date']
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"
    
    # Note: total_work_hours est calculé et sauvegardé dans la méthode save()
    # Pas besoin de @property car c'est un champ du modèle
    
    @property
    def break_duration_minutes(self):
        """Calcule la durée de la pause en minutes"""
        if not self.break_start or not self.break_end:
            return 0
        
        break_start = datetime.combine(self.date, self.break_start)
        break_end = datetime.combine(self.date, self.break_end)
        duration = break_end - break_start
        return int(duration.total_seconds() / 60)
    
    def update_time_status(self, time_field, expected_time, tolerance_minutes=0):
        """Met à jour le statut (en avance, à l'heure, en retard) pour un champ de temps"""
        if not getattr(self, time_field):
            return
            
        time_value = getattr(self, time_field)
        expected_dt = datetime.combine(self.date, expected_time)
        actual_dt = datetime.combine(self.date, time_value)
        
        # Calculer la différence avec la tolérance
        tolerance_delta = timedelta(minutes=tolerance_minutes)
        early_limit = expected_dt - tolerance_delta
        late_limit = expected_dt + tolerance_delta
        
        # Déterminer le statut
        if actual_dt < early_limit:
            status_field = f"{time_field.split('_')[0]}_status"
            setattr(self, status_field, self.STATUS_EARLY)
            
            # Calculer les minutes d'avance
            minutes_early = int((expected_dt - actual_dt).total_seconds() / 60)
            if time_field == 'arrival_time':
                self.early_arrival_minutes = max(0, minutes_early - tolerance_minutes)
            elif time_field == 'departure_time':
                self.early_departure_minutes = max(0, minutes_early - tolerance_minutes)
                
        elif actual_dt > late_limit:
            status_field = f"{time_field.split('_')[0]}_status"
            setattr(self, status_field, self.STATUS_LATE)
            
            # Calculer les minutes de retard
            minutes_late = int((actual_dt - expected_dt).total_seconds() / 60)
            if time_field == 'arrival_time':
                self.late_minutes = max(0, minutes_late - tolerance_minutes)
                self.is_late = self.late_minutes > 0  # Rétrocompatibilité
        else:
            status_field = f"{time_field.split('_')[0]}_status"
            setattr(self, status_field, self.STATUS_ON_TIME)
    
    def save(self, *args, **kwargs):
        # Récupérer les paramètres de pointage
        settings = PointageSettings.get_settings()
        
        # Mettre à jour les statuts de temps
        self.update_time_status(
            'arrival_time',
            settings.expected_arrival_time,
            settings.tolerance_minutes
        )
        
        if self.departure_time:
            self.update_time_status(
                'departure_time',
                settings.expected_departure_time,
                settings.tolerance_minutes
            )
        
        # Calculer automatiquement les heures travaillées
        if self.arrival_time and self.departure_time:
            # Temps total présent
            total_time = datetime.combine(self.date, self.departure_time) - datetime.combine(self.date, self.arrival_time)
            
            # Soustraire la pause déjeuner si présente
            if self.break_start and self.break_end:
                break_duration = datetime.combine(self.date, self.break_end) - datetime.combine(self.date, self.break_start)
                total_time -= break_duration
            
            # Vérifier si la pause déjeuner est incluse dans les heures de travail
            lunch_start = datetime.combine(self.date, time(12, 0))  # 12h00
            lunch_end = datetime.combine(self.date, time(13, 0))    # 13h00
            
            if (datetime.combine(self.date, self.arrival_time) <= lunch_start and 
                datetime.combine(self.date, self.departure_time) >= lunch_end):
                total_time -= timedelta(hours=1)
            
            # Convertir en heures (format décimal)
            self.total_work_hours = round(total_time.total_seconds() / 3600, 2)
        
        super().save(*args, **kwargs)


class PointageSettings(models.Model):
    """Paramètres globaux pour le système de pointage"""
    expected_arrival_time = models.TimeField(default=time(8, 0), verbose_name="Heure d'arrivée attendue")
    expected_departure_time = models.TimeField(default=time(17, 0), verbose_name="Heure de départ attendue")
    break_duration_minutes = models.IntegerField(default=60, verbose_name="Durée pause (minutes)")
    tolerance_minutes = models.IntegerField(default=15, verbose_name="Tolérance retard (minutes)")
    working_days = models.CharField(
        max_length=20,
        default='1,2,3,4,5',  # Lundi à Vendredi
        verbose_name="Jours travaillés (1=Lundi, 7=Dimanche)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pointage_settings'
        verbose_name = 'Paramètres pointage'
        verbose_name_plural = 'Paramètres pointage'
    
    def __str__(self):
        return f"Paramètres pointage - {self.expected_arrival_time} à {self.expected_departure_time}"
    
    @classmethod
    def get_settings(cls):
        """Récupère les paramètres (crée des paramètres par défaut si aucun n'existe)"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class AbsenceRequest(models.Model):
    """Demandes d'absence des employés"""
    ABSENCE_TYPES = [
        ('sick_leave', 'Congé maladie'),
        ('vacation', 'Congé payé'),
        ('personal', 'Congé personnel'),
        ('maternity', 'Congé maternité'),
        ('other', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ]
    
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='absence_requests',
        limit_choices_to={'role': 'developer'},
        verbose_name="Employé"
    )
    absence_type = models.CharField(
        max_length=20,
        choices=ABSENCE_TYPES,
        verbose_name="Type d'absence"
    )
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    reason = models.TextField(verbose_name="Raison")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Statut"
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_absences',
        limit_choices_to={'role': 'admin'},
        verbose_name="Approuvé par"
    )
    approval_notes = models.TextField(blank=True, null=True, verbose_name="Notes d'approbation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'absence_requests'
        verbose_name = 'Demande d\'absence'
        verbose_name_plural = 'Demandes d\'absence'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.absence_type} ({self.start_date} - {self.end_date})"
    
    @property
    def duration_days(self):
        """Calcule la durée de l'absence en jours"""
        return (self.end_date - self.start_date).days + 1
