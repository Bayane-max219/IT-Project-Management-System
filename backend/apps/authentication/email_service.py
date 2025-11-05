from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import secrets
import string

def generate_password(length=12):
    """Générer un mot de passe sécurisé"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def generate_registration_key():
    """Générer une clé d'inscription unique"""
    return secrets.token_urlsafe(32)

def send_account_creation_email(user, password, created_by_admin=True):
    """Envoyer un email avec les identifiants du nouveau compte"""
    
    if created_by_admin:
        subject = f"🚀 Votre compte {user.get_role_display()} - IT Project Manager"
        
        # Template HTML professionnel
        try:
            html_message = render_to_string('emails/account_creation.html', {
                'user': user,
                'password': password,
                'login_url': 'http://localhost:3000/login'
            })
        except:
            # Fallback si le template n'existe pas
            html_message = None
        
        # Message texte de secours
        message = f"""
🚀 IT Project Manager - Bienvenue !

Bonjour {user.first_name} {user.last_name},

Félicitations ! Votre compte {user.get_role_display()} a été créé avec succès.

🔐 VOS IDENTIFIANTS DE CONNEXION :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email : {user.email}
🔑 Mot de passe : {password}
👤 Rôle : {user.get_role_display()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 Lien de connexion : http://localhost:3000/login

⚠️ IMPORTANT : Veuillez changer votre mot de passe lors de votre première connexion.

Cordialement,
L'équipe IT Project Manager
Plateforme de Gestion de Projets IT
        """
    else:
        subject = "Bienvenue sur IT Project Manager"
        message = f"""
Bonjour {user.first_name} {user.last_name},

Votre inscription sur IT Project Manager a été validée.

Vos identifiants de connexion :
- Email : {user.email}
- Mot de passe : {password}
- Rôle : {user.get_role_display()}

Lien de connexion : http://localhost:3000/login

Cordialement,
L'équipe IT Project Manager
        """
    
    try:
        from django.core.mail import EmailMultiAlternatives
        
        # Créer l'email avec version HTML et texte
        email = EmailMultiAlternatives(
            subject,
            message,  # Version texte
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        
        # Ajouter la version HTML si disponible
        if html_message:
            email.attach_alternative(html_message, "text/html")
        
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False

def send_registration_key_email(email, registration_key, role):
    """Envoyer une clé d'inscription à un futur utilisateur"""
    
    subject = "Invitation à rejoindre IT Project Manager"
    
    message = f"""
Bonjour,

Vous êtes invité(e) à rejoindre la plateforme IT Project Manager en tant que {role}.

Votre clé d'inscription : {registration_key}

Lien d'inscription : http://localhost:3000/register?key={registration_key}

Cette clé est valable 7 jours.

Cordialement,
L'équipe IT Project Manager
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False
