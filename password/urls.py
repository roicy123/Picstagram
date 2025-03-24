from django.urls import path
from .views import password_reset_request, validate_otp, reset_password

urlpatterns = [
    path('password-reset/', password_reset_request, name='password_reset_request'),
    path('validate-otp/<int:user_id>/', validate_otp, name='validate_otp'),
    path('reset-password/<int:user_id>/', reset_password, name='reset_password'),
]