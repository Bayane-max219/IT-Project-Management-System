from django.urls import path
from . import test_login_view
from . import test_api_views

urlpatterns = [
    # Auth endpoints
    path('test-login/', test_login_view.test_login, name='test_login'),
    path('users/', test_api_views.users_list, name='users_list'),
    path('profile/', test_api_views.profile_view, name='profile'),
    path('logout/', test_api_views.logout_view, name='logout'),
]
