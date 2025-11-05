from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, RegistrationKey
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, LoginSerializer, ChangePasswordSerializer
try:
    from .email_service import (
        send_account_creation_email, send_registration_key_email, 
        generate_password, generate_registration_key
    )
except ImportError:
    # Fallback si le service email n'est pas disponible
    def send_account_creation_email(*args, **kwargs):
        return False
    def send_registration_key_email(*args, **kwargs):
        return False
    def generate_password():
        return "TempPassword123!"
    def generate_registration_key():
        return "temp_key_123"


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=email, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    return Response({'error': 'Identifiants invalides'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Déconnexion réussie'})
    except Exception as e:
        return Response({'error': 'Token invalide'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile_view(request):
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(UserSerializer(request.user).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_user_with_email(request):
    """Créer un utilisateur et envoyer les identifiants par email"""
    if not request.user.is_admin():
        return Response({'error': 'Permission refusée'}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data.copy()
    
    # Générer un mot de passe sécurisé
    password = generate_password()
    data['password'] = password
    
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(password)
        user.save()
        
        # Envoyer l'email avec les identifiants
        email_sent = send_account_creation_email(user, password, created_by_admin=True)
        
        response_data = serializer.data
        response_data['email_sent'] = email_sent
        response_data['temporary_password'] = password  # Pour affichage admin
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_registration_invitation(request):
    """Envoyer une invitation avec clé d'inscription"""
    if not request.user.is_admin():
        return Response({'error': 'Permission refusée'}, status=status.HTTP_403_FORBIDDEN)
    
    email = request.data.get('email')
    role = request.data.get('role', 'developer')
    
    if not email:
        return Response({'error': 'Email requis'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Vérifier si l'email existe déjà
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Un utilisateur avec cet email existe déjà'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Générer une clé d'inscription
    registration_key = generate_registration_key()
    
    # Créer l'enregistrement de la clé
    reg_key = RegistrationKey.objects.create(
        key=registration_key,
        email=email,
        role=role,
        created_by=request.user
    )
    
    # Envoyer l'email d'invitation
    email_sent = send_registration_key_email(email, registration_key, role)
    
    return Response({
        'message': 'Invitation envoyée',
        'registration_key': registration_key,
        'email_sent': email_sent,
        'expires_at': reg_key.expires_at
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_with_key(request):
    """Inscription avec clé d'invitation"""
    registration_key = request.data.get('registration_key')
    
    if not registration_key:
        return Response({'error': 'Clé d\'inscription requise'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        reg_key = RegistrationKey.objects.get(key=registration_key)
        
        if not reg_key.is_valid():
            return Response({'error': 'Clé d\'inscription expirée ou déjà utilisée'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Créer l'utilisateur
        data = request.data.copy()
        data['email'] = reg_key.email
        data['role'] = reg_key.role
        
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Marquer la clé comme utilisée
            reg_key.is_used = True
            reg_key.used_at = timezone.now()
            reg_key.save()
            
            return Response({
                'message': 'Compte créé avec succès',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except RegistrationKey.DoesNotExist:
        return Response({'error': 'Clé d\'inscription invalide'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Ancien mot de passe incorrect'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Mot de passe modifié avec succès'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    def perform_create(self, serializer):
        if not self.request.user.is_admin():
            raise permissions.PermissionDenied("Seuls les admins peuvent créer des utilisateurs.")
        serializer.save()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
    
    def perform_update(self, serializer):
        if not self.request.user.is_admin() and self.get_object() != self.request.user:
            raise permissions.PermissionDenied("Vous ne pouvez modifier que votre propre profil.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if not self.request.user.is_admin():
            raise permissions.PermissionDenied("Seuls les admins peuvent supprimer des utilisateurs.")
        if instance == self.request.user:
            raise permissions.PermissionDenied("Vous ne pouvez pas supprimer votre propre compte.")
        instance.delete()
