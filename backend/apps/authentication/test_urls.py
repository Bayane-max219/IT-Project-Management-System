from django.urls import path
from . import test_login_view

urlpatterns = [
    path('test-login/', test_login_view.test_login, name='test_login'),
]
