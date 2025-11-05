from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'role', 'phone', 'profile_picture', 'is_active', 
                 'created_at', 'updated_at', 'full_name')
        read_only_fields = ('id', 'created_at', 'updated_at', 'full_name')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 
                 'role', 'phone', 'password', 'password_confirm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Email ou mot de passe incorrect.')
            if not user.is_active:
                raise serializers.ValidationError('Compte désactivé.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Email et mot de passe requis.')
        
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour des profils utilisateur"""
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    username = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 
                 'phone', 'profile_picture', 'current_password', 'new_password')
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone': {'required': False},
            'profile_picture': {'required': False}
        }
        
    def validate_email(self, value):
        """Vérifier que l'email n'est pas déjà utilisé par un autre utilisateur"""
        user = self.instance
        if user and User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value
    
    def validate_username(self, value):
        """Vérifier que le nom d'utilisateur n'est pas déjà utilisé"""
        user = self.instance
        if user and User.objects.filter(username=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return value
    
    def validate(self, attrs):
        """Valider le changement de mot de passe si fourni"""
        # Supprimer les champs vides de mot de passe
        if 'current_password' in attrs and not attrs['current_password']:
            attrs.pop('current_password')
        if 'new_password' in attrs and not attrs['new_password']:
            attrs.pop('new_password')
        
        # Vérifier uniquement si un nouveau mot de passe est fourni (non vide)
        if 'new_password' in attrs and attrs['new_password']:
            # Si un nouveau mot de passe est fourni, l'ancien est requis
            if 'current_password' not in attrs or not attrs['current_password']:
                raise serializers.ValidationError({
                    'current_password': ['Le mot de passe actuel est requis pour changer de mot de passe.']
                })
            
            # Vérifier que l'ancien mot de passe est correct
            user = self.instance
            if not user.check_password(attrs['current_password']):
                raise serializers.ValidationError({
                    'current_password': ['Le mot de passe actuel est incorrect. Vérifiez que vous utilisez le bon mot de passe.']
                })
            
            # Vérifier la longueur minimale
            if len(attrs['new_password']) < 6:
                raise serializers.ValidationError({
                    'new_password': ['Le nouveau mot de passe doit contenir au moins 6 caractères.']
                })
        
        return attrs
    
    def update(self, instance, validated_data):
        """Mettre à jour l'utilisateur et gérer le changement de mot de passe"""
        # Extraire les champs de mot de passe
        current_password = validated_data.pop('current_password', None)
        new_password = validated_data.pop('new_password', None)
        
        # Mettre à jour les autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Changer le mot de passe si fourni
        if new_password:
            instance.set_password(new_password)
        
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return attrs
