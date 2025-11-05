from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('change-password/', views.change_password_view, name='change_password'),
    
    # Nouvelles routes pour la gestion professionnelle des comptes
    path('create-user-with-email/', views.create_user_with_email, name='create_user_with_email'),
    path('send-invitation/', views.send_registration_invitation, name='send_invitation'),
    path('register-with-key/', views.register_with_key, name='register_with_key'),
]
