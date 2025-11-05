from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone
from datetime import datetime, time, timedelta
from .models import Pointage, PointageSettings, AbsenceRequest
from .serializers import (
    PointageSerializer, PointageSettingsSerializer,
    AbsenceRequestSerializer, PointageStatsSerializer
)
from django.shortcuts import get_object_or_404
from django.db import transaction

def get_madagascar_time():
    """Obtenir l'heure actuelle à Madagascar (UTC+3)"""
    # Utiliser timezone.localtime() qui respecte TIME_ZONE dans settings.py
    return timezone.localtime()

def format_timedelta_as_time(td):
    """Convertir un timedelta en format d'heure HH:MM"""
    if not td:
        return None
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"


class PointageListCreateView(generics.ListCreateAPIView):
    serializer_class = PointageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Pointage.objects.all().select_related('employee')
        else:
            return Pointage.objects.filter(employee=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_developer() and not user.is_admin():
            raise permissions.PermissionDenied("Seuls les développeurs peuvent faire du pointage.")
        serializer.save()


class PointageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PointageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Pointage.objects.all()
        else:
            return Pointage.objects.filter(employee=user)


class MyPointageView(generics.ListAPIView):
    """Vue pour récupérer les pointages de l'utilisateur connecté"""
    serializer_class = PointageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_developer():
            return Pointage.objects.filter(employee=user).order_by('-date')
        return Pointage.objects.none()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def clock_in(request):
    """Pointage d'arrivée avec gestion des retards et des arrivées anticipées"""
    # DEBUG: Afficher tout ce qui est reçu
    print(f"🔍 BACKEND DEBUG:")
    print(f"   request.method: {request.method}")
    print(f"   request.content_type: {request.content_type}")
    print(f"   request.body: {request.body}")
    print(f"   request.data: {request.data}")
    print(f"   request.POST: {request.POST}")
    
    user = request.user
    print(f"🔍 USER: {user} (role: {getattr(user, 'role', 'N/A')})")
    
    if not user.is_developer():
        print(f"❌ USER NOT DEVELOPER")
        return Response(
            {'error': 'Seuls les développeurs peuvent pointer'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    print(f"✅ USER IS DEVELOPER")
    
    # Utiliser l'heure locale de Madagascar
    try:
        madagascar_now = get_madagascar_time()
        today = madagascar_now.date()
        now = madagascar_now.time()
        print(f"🔍 TEMPS: {today} {now}")
    except Exception as e:
        print(f"❌ ERREUR TEMPS: {e}")
        return Response({'error': f'Erreur temps: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Vérifier si un pointage existe déjà pour aujourd'hui
    try:
        print(f"🔍 RECHERCHE POINTAGE EXISTANT...")
        pointage, created = Pointage.objects.get_or_create(
            employee=user,
            date=today,
            defaults={
                'arrival_time': now,
                'arrival_status': Pointage.STATUS_ON_TIME
            }
        )
        print(f"🔍 POINTAGE: created={created}, id={pointage.id}")
    except Exception as e:
        print(f"❌ ERREUR CRÉATION POINTAGE: {e}")
        return Response({'error': f'Erreur création pointage: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Mettre à jour l'heure d'arrivée
    pointage.arrival_time = now
    
    # Vérifier si une justification est nécessaire
    settings = PointageSettings.get_settings()
    tolerance_time = (
        datetime.combine(today, settings.expected_arrival_time) + 
        timedelta(minutes=settings.tolerance_minutes)
    ).time()
    
    # Si en retard, demander une justification
    if now > tolerance_time:
        # DEBUG: Afficher toutes les données reçues
        print(f"🔍 DEBUG JUSTIFICATION:")
        print(f"   request.data: {request.data}")
        print(f"   reason: {request.data.get('reason')}")
        print(f"   late_reason: {request.data.get('late_reason')}")
        
        # Si pas de raison fournie, retourner une erreur
        reason = request.data.get('reason') or request.data.get('late_reason')
        print(f"   reason finale: '{reason}'")
        
        if not reason:
            return Response(
                {
                    'requires_justification': True,
                    'message': 'Veuillez fournir une raison pour votre retard.',
                    'expected_arrival': settings.expected_arrival_time.strftime('%H:%M'),
                    'actual_arrival': now.strftime('%H:%M'),
                    'tolerance_minutes': settings.tolerance_minutes
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        pointage.late_reason = reason
        pointage.is_justified = True
        print(f"   ✅ Justification assignée: '{pointage.late_reason}'")
    
    # Si arrivée très en avance, demander des notes
    early_limit = (
        datetime.combine(today, settings.expected_arrival_time) - 
        timedelta(minutes=30)  # 30 minutes avant l'heure prévue
    ).time()
    
    if now < early_limit and 'early_arrival_notes' not in request.data:
        return Response(
            {
                'requires_early_notes': True,
                'message': 'Veuillez indiquer la raison de votre arrivée anticipée.',
                'expected_arrival': settings.expected_arrival_time.strftime('%H:%M'),
                'actual_arrival': now.strftime('%H:%M')
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if 'early_arrival_notes' in request.data:
        pointage.early_arrival_notes = request.data['early_arrival_notes']
    
    # Définir le statut d'arrivée
    if now > tolerance_time:
        pointage.arrival_status = Pointage.STATUS_LATE
        # Calculer les minutes de retard
        expected_arrival = datetime.combine(today, settings.expected_arrival_time)
        actual_arrival = datetime.combine(today, now)
        late_minutes = int((actual_arrival - expected_arrival).total_seconds() / 60)
        pointage.late_minutes = late_minutes
    elif now < early_limit:
        pointage.arrival_status = Pointage.STATUS_EARLY
        # Calculer les minutes d'avance
        expected_arrival = datetime.combine(today, settings.expected_arrival_time)
        actual_arrival = datetime.combine(today, now)
        early_minutes = int((expected_arrival - actual_arrival).total_seconds() / 60)
        pointage.early_arrival_minutes = early_minutes
    else:
        pointage.arrival_status = Pointage.STATUS_ON_TIME
    
    # Sauvegarder le pointage
    print(f"🔍 AVANT SAUVEGARDE:")
    print(f"   pointage.late_reason: '{pointage.late_reason}'")
    print(f"   pointage.is_justified: {pointage.is_justified}")
    print(f"   pointage.arrival_status: {pointage.arrival_status}")
    
    try:
        pointage.save()
        print(f"✅ SAUVEGARDE RÉUSSIE")
        
        # Vérifier après sauvegarde
        pointage.refresh_from_db()
        print(f"🔍 APRÈS SAUVEGARDE:")
        print(f"   pointage.late_reason: '{pointage.late_reason}'")
        print(f"   pointage.is_justified: {pointage.is_justified}")
        
    except Exception as e:
        print(f"❌ ERREUR SAUVEGARDE: {e}")
        return Response({'error': f'Erreur sauvegarde: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Retourner les informations de pointage
    serializer = PointageSerializer(pointage)
    print(f"🔍 DONNÉES SÉRIALISÉES: {serializer.data}")
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def clock_out(request):
    """Pointage de départ avec gestion des départs anticipés"""
    try:
        user = request.user
        if not user.is_developer():
            return Response(
                {'error': 'Seuls les développeurs peuvent pointer'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Utiliser l'heure locale de Madagascar
        madagascar_now = get_madagascar_time()
        today = madagascar_now.date()
        now = madagascar_now.time()
        
        try:
            pointage = Pointage.objects.get(employee=user, date=today)
        except Pointage.DoesNotExist:
            return Response(
                {'error': 'Veuillez d\'abord pointer votre arrivée'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        print(f"❌ Erreur dans clock_out (début): {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'Erreur serveur: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if pointage.departure_time:
        return Response(
            {'error': 'Vous avez déjà pointé votre départ aujourd\'hui'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Vérifier si le départ est anticipé ou en retard
    settings = PointageSettings.get_settings()
    early_limit = (
        datetime.combine(today, settings.expected_departure_time) - 
        timedelta(minutes=settings.tolerance_minutes)
    ).time()
    
    late_limit = (
        datetime.combine(today, settings.expected_departure_time) + 
        timedelta(minutes=settings.tolerance_minutes)
    ).time()
    
    # Si départ anticipé, demander une justification
    if now < early_limit:
        minutes_early = int((datetime.combine(today, settings.expected_departure_time) - datetime.combine(today, now)).total_seconds() / 60)
        if 'reason' not in request.data or not request.data['reason']:
            return Response(
                {
                    'requires_justification': True,
                    'message': f'Vous partez {minutes_early} minutes en avance. Veuillez fournir une raison.',
                    'expected_departure': settings.expected_departure_time.strftime('%H:%M'),
                    'actual_departure': now.strftime('%H:%M'),
                    'minutes_difference': minutes_early,
                    'tolerance_minutes': settings.tolerance_minutes,
                    'type': 'early'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        pointage.early_departure_reason = request.data['reason']
    
    # Si départ en retard, demander une justification
    elif now > late_limit:
        minutes_late = int((datetime.combine(today, now) - datetime.combine(today, settings.expected_departure_time)).total_seconds() / 60)
        if 'reason' not in request.data or not request.data['reason']:
            return Response(
                {
                    'requires_justification': True,
                    'message': f'Vous partez {minutes_late} minutes en retard. Veuillez fournir une raison.',
                    'expected_departure': settings.expected_departure_time.strftime('%H:%M'),
                    'actual_departure': now.strftime('%H:%M'),
                    'minutes_difference': minutes_late,
                    'tolerance_minutes': settings.tolerance_minutes,
                    'type': 'late'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if not pointage.late_reason:
            pointage.late_reason = f"Départ en retard: {request.data['reason']}"
        else:
            pointage.late_reason += f" | Départ en retard: {request.data['reason']}"
    
    # Mettre à jour l'heure de départ
    try:
        pointage.departure_time = now
        pointage.save()
        
        serializer = PointageSerializer(pointage)
        return Response(serializer.data)
    except Exception as e:
        print(f"❌ Erreur dans clock_out (sauvegarde): {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'Erreur lors de la sauvegarde: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def break_start(request):
    """Début de pause avec gestion des retards/avances"""
    user = request.user
    if not user.is_developer():
        return Response(
            {'error': 'Seuls les développeurs peuvent pointer'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Utiliser l'heure locale de Madagascar
    madagascar_now = get_madagascar_time()
    today = madagascar_now.date()
    now = madagascar_now.time()
    
    try:
        pointage = Pointage.objects.get(employee=user, date=today)
    except Pointage.DoesNotExist:
        return Response(
            {'error': 'Veuillez d\'abord pointer votre arrivée'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if pointage.break_start:
        return Response(
            {'error': 'Vous avez déjà commencé votre pause aujourd\'hui'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Vérifier si la pause est en retard ou en avance par rapport à 12h00
    settings = PointageSettings.get_settings()
    expected_break_time = time(12, 0)  # 12h00
    tolerance_minutes = settings.tolerance_minutes
    
    early_limit = (
        datetime.combine(today, expected_break_time) - 
        timedelta(minutes=tolerance_minutes)
    ).time()
    
    late_limit = (
        datetime.combine(today, expected_break_time) + 
        timedelta(minutes=tolerance_minutes)
    ).time()
    
    # Si pause en avance
    if now < early_limit:
        minutes_early = int((datetime.combine(today, expected_break_time) - datetime.combine(today, now)).total_seconds() / 60)
        if 'reason' not in request.data or not request.data['reason']:
            return Response(
                {
                    'requires_justification': True,
                    'message': f'Vous commencez votre pause {minutes_early} minutes en avance. Veuillez indiquer la raison.',
                    'expected_time': expected_break_time.strftime('%H:%M'),
                    'actual_time': now.strftime('%H:%M'),
                    'minutes_difference': minutes_early,
                    'type': 'early'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        pointage.early_arrival_notes = f"Pause en avance: {request.data['reason']}"
    
    # Si pause en retard
    elif now > late_limit:
        minutes_late = int((datetime.combine(today, now) - datetime.combine(today, expected_break_time)).total_seconds() / 60)
        if 'reason' not in request.data or not request.data['reason']:
            return Response(
                {
                    'requires_justification': True,
                    'message': f'Vous commencez votre pause {minutes_late} minutes en retard. Veuillez indiquer la raison.',
                    'expected_time': expected_break_time.strftime('%H:%M'),
                    'actual_time': now.strftime('%H:%M'),
                    'minutes_difference': minutes_late,
                    'type': 'late'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if not pointage.late_reason:
            pointage.late_reason = f"Pause en retard: {request.data['reason']}"
        else:
            pointage.late_reason += f" | Pause en retard: {request.data['reason']}"
    
    pointage.break_start = now
    pointage.save()
    
    serializer = PointageSerializer(pointage)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def break_end(request):
    """Fin de pause avec gestion des retards/avances"""
    user = request.user
    if not user.is_developer():
        return Response(
            {'error': 'Seuls les développeurs peuvent pointer'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Utiliser l'heure locale de Madagascar
    madagascar_now = get_madagascar_time()
    today = madagascar_now.date()
    now = madagascar_now.time()
    
    try:
        pointage = Pointage.objects.get(employee=user, date=today)
    except Pointage.DoesNotExist:
        return Response(
            {'error': 'Veuillez d\'abord pointer votre arrivée'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not pointage.break_start:
        return Response(
            {'error': 'Vous devez d\'abord commencer votre pause'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if pointage.break_end:
        return Response(
            {'error': 'Vous avez déjà terminé votre pause aujourd\'hui'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Vérifier si le retour de pause est en retard ou en avance par rapport à 13h00
    settings = PointageSettings.get_settings()
    expected_return_time = time(13, 0)  # 13h00
    tolerance_minutes = settings.tolerance_minutes
    
    early_limit = (
        datetime.combine(today, expected_return_time) - 
        timedelta(minutes=tolerance_minutes)
    ).time()
    
    late_limit = (
        datetime.combine(today, expected_return_time) + 
        timedelta(minutes=tolerance_minutes)
    ).time()
    
    # Si retour en avance
    if now < early_limit:
        minutes_early = int((datetime.combine(today, expected_return_time) - datetime.combine(today, now)).total_seconds() / 60)
        if 'reason' not in request.data or not request.data['reason']:
            return Response(
                {
                    'requires_justification': True,
                    'message': f'Vous revenez de pause {minutes_early} minutes en avance. Veuillez indiquer la raison.',
                    'expected_time': expected_return_time.strftime('%H:%M'),
                    'actual_time': now.strftime('%H:%M'),
                    'minutes_difference': minutes_early,
                    'type': 'early'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if not pointage.early_arrival_notes:
            pointage.early_arrival_notes = f"Retour pause en avance: {request.data['reason']}"
        else:
            pointage.early_arrival_notes += f" | Retour pause en avance: {request.data['reason']}"
    
    # Si retour en retard
    elif now > late_limit:
        minutes_late = int((datetime.combine(today, now) - datetime.combine(today, expected_return_time)).total_seconds() / 60)
        if 'reason' not in request.data or not request.data['reason']:
            return Response(
                {
                    'requires_justification': True,
                    'message': f'Vous revenez de pause {minutes_late} minutes en retard. Veuillez indiquer la raison.',
                    'expected_time': expected_return_time.strftime('%H:%M'),
                    'actual_time': now.strftime('%H:%M'),
                    'minutes_difference': minutes_late,
                    'type': 'late'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if not pointage.late_reason:
            pointage.late_reason = f"Retour pause en retard: {request.data['reason']}"
        else:
            pointage.late_reason += f" | Retour pause en retard: {request.data['reason']}"
    
    pointage.break_end = now
    pointage.save()
    
    serializer = PointageSerializer(pointage)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def today_pointage(request):
    """Récupère le pointage du jour pour l'utilisateur connecté"""
    user = request.user
    if not user.is_developer():
        return Response(
            {'error': 'Seuls les développeurs ont accès au pointage'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Utiliser l'heure locale de Madagascar
    madagascar_now = get_madagascar_time()
    today = madagascar_now.date()
    
    try:
        pointage = Pointage.objects.get(employee=user, date=today)
        serializer = PointageSerializer(pointage)
        return Response(serializer.data)
    except Pointage.DoesNotExist:
        return Response({'message': 'Aucun pointage aujourd\'hui'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@transaction.atomic
def justify_pointage(request, pointage_id):
    """
    Permet à un administrateur de valider ou rejeter une justification
    de retard ou de départ anticipé
    """
    if not request.user.is_admin():
        return Response(
            {'error': 'Accès non autorisé'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        pointage = Pointage.objects.select_for_update().get(pk=pointage_id)
    except Pointage.DoesNotExist:
        return Response(
            {'error': 'Pointage non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Vérifier qu'il y a une raison de justifier (retard ou départ anticipé)
    if not pointage.late_reason and not pointage.early_departure_reason:
        return Response(
            {'error': 'Aucune justification à traiter pour ce pointage'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Vérifier que la justification n'a pas déjà été traitée
    if pointage.is_justified and pointage.justification_approved is not None:
        return Response(
            {'error': 'Cette justification a déjà été traitée'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Valider les données de la requête
    approved = request.data.get('approved')
    if approved is None:
        return Response(
            {'error': 'Le champ "approved" est requis (true/false)'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Mettre à jour le pointage
    pointage.is_justified = True
    pointage.justification_approved = bool(approved)
    pointage.approval_notes = request.data.get('notes', '')
    pointage.approved_by = request.user
    pointage.save()
    
    # Envoyer une notification à l'employé si nécessaire
    # (à implémenter avec un système de notifications)
    
    serializer = PointageSerializer(pointage)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_justifications(request):
    """
    Liste toutes les justifications en attente de validation par l'administrateur
    """
    if not request.user.is_admin():
        return Response(
            {'error': 'Accès non autorisé'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Récupérer les pointages avec justifications non traitées
    pending_pointages = Pointage.objects.filter(
        Q(late_reason__isnull=False) | Q(early_departure_reason__isnull=False),
        is_justified=False
    ).select_related('employee').order_by('date', 'employee__last_name')
    
    # Préparer les données de réponse
    data = []
    for pointage in pending_pointages:
        justification_type = []
        if pointage.late_reason:
            justification_type.append('retard')
        if pointage.early_departure_reason:
            justification_type.append('départ anticipé')
        
        data.append({
            'id': pointage.id,
            'date': pointage.date,
            'employee': {
                'id': pointage.employee.id,
                'full_name': f"{pointage.employee.first_name} {pointage.employee.last_name}",
                'email': pointage.employee.email
            },
            'justification_type': ', '.join(justification_type),
            'arrival_time': pointage.arrival_time.strftime('%H:%M') if pointage.arrival_time else None,
            'departure_time': pointage.departure_time.strftime('%H:%M') if pointage.departure_time else None,
            'late_minutes': pointage.late_minutes,
            'early_departure_minutes': pointage.early_departure_minutes,
            'late_reason': pointage.late_reason,
            'early_departure_reason': pointage.early_departure_reason,
            'created_at': pointage.created_at
        })
    
    return Response({
        'count': len(data),
        'results': data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pointage_stats(request):
    """Statistiques de pointage pour les admins avec détails sur les retards"""
    if not request.user.is_admin():
        return Response(
            {'error': 'Accès non autorisé'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Utiliser l'heure locale de Madagascar
    madagascar_now = get_madagascar_time()
    today = madagascar_now.date()
    
    # Récupérer les statistiques
    from django.contrib.auth import get_user_model
    User = get_user_model()
    total_employees = User.objects.filter(role='developer').count()
    
    # Pointages du jour avec statuts
    today_pointages = Pointage.objects.filter(date=today).select_related('employee')
    present_today = today_pointages.count()
    
    # Statistiques de retard
    late_today = today_pointages.filter(arrival_status=Pointage.STATUS_LATE).count()
    early_departures = today_pointages.filter(departure_status=Pointage.STATUS_EARLY).count()
    absent_today = total_employees - present_today
    
    # Calculer l'heure moyenne d'arrivée
    avg_arrival = today_pointages.aggregate(
        avg_arrival=Avg('arrival_time')
    )['avg_arrival']
    
    # Calculer le nombre total d'heures travaillées aujourd'hui
    total_hours = today_pointages.aggregate(
        total=Sum('total_work_hours')
    )['total'] or 0
    
    # Taux de présence
    attendance_rate = round((present_today / total_employees * 100) if total_employees > 0 else 0, 1)
    
    # Récupérer les employés en retard aujourd'hui avec détails
    late_employees = []
    for p in today_pointages.filter(arrival_status=Pointage.STATUS_LATE):
        late_employees.append({
            'id': p.employee.id,
            'full_name': f"{p.employee.first_name} {p.employee.last_name}",
            'arrival_time': p.arrival_time.strftime('%H:%M') if p.arrival_time else None,
            'late_minutes': p.late_minutes,
            'late_reason': p.late_reason,
            'is_justified': p.is_justified,
            'justification_approved': p.justification_approved
        })
    
    # Récupérer les départs anticipés
    early_departures_list = []
    for p in today_pointages.filter(departure_status=Pointage.STATUS_EARLY):
        early_departures_list.append({
            'id': p.employee.id,
            'full_name': f"{p.employee.first_name} {p.employee.last_name}",
            'departure_time': p.departure_time.strftime('%H:%M') if p.departure_time else None,
            'early_minutes': p.early_departure_minutes,
            'reason': p.early_departure_reason,
            'is_justified': p.is_justified,
            'justification_approved': p.justification_approved
        })
    
    # Préparer les données de réponse
    data = {
        'date': today,
        'total_employees': total_employees,
        'present_today': present_today,
        'late_today': late_today,
        'early_departures_today': early_departures,
        'absent_today': absent_today,
        'attendance_rate': attendance_rate,
        'average_arrival_time': format_timedelta_as_time(avg_arrival) if avg_arrival else None,
        'total_work_hours_today': round(total_hours, 2),
        'late_employees': late_employees,
        'early_departures': early_departures_list,
        'justification_stats': {
            'total_pending': today_pointages.filter(
                Q(late_reason__isnull=False) | Q(early_departure_reason__isnull=False),
                is_justified=False
            ).count(),
            'total_approved': today_pointages.filter(justification_approved=True).count(),
            'total_rejected': today_pointages.filter(justification_approved=False).count()
        }
    }
    
    serializer = PointageStatsSerializer(data)
    return Response(serializer.data)


class AbsenceRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = AbsenceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return AbsenceRequest.objects.all().select_related('employee', 'approved_by')
        else:
            return AbsenceRequest.objects.filter(employee=user)


class AbsenceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AbsenceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return AbsenceRequest.objects.all()
        else:
            return AbsenceRequest.objects.filter(employee=user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_absence(request, absence_id):
    """Approuver ou rejeter une demande d'absence"""
    if not request.user.is_admin():
        return Response(
            {'error': 'Seuls les admins peuvent approuver les demandes'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        absence = AbsenceRequest.objects.get(id=absence_id)
        action = request.data.get('action')  # 'approve' ou 'reject'
        approval_notes = request.data.get('approval_notes', '')
        
        if action not in ['approve', 'reject']:
            return Response(
                {'error': 'Action invalide. Utilisez "approve" ou "reject"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        absence.status = 'approved' if action == 'approve' else 'rejected'
        absence.approved_by = request.user
        absence.approval_notes = approval_notes
        absence.save()
        
        serializer = AbsenceRequestSerializer(absence)
        return Response(serializer.data)
        
    except AbsenceRequest.DoesNotExist:
        return Response(
            {'error': 'Demande d\'absence non trouvée'}, 
            status=status.HTTP_404_NOT_FOUND
        )
