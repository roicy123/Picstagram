from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from authy.views import UserProfile, EditProfile

urlpatterns = [
    # Profile Section
    path('profile/edit', EditProfile, name="editprofile"),

    # User Authentication
    path('sign-up/', views.register, name="sign-up"),
    path('sign-in/', auth_views.LoginView.as_view(template_name="sign-in.html", redirect_authenticated_user=True), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(), name='sign-out'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name="password_reset.html",
             email_template_name="password_reset_email.html",
             success_url=reverse_lazy('password_reset_done')
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), 
         name='password_reset_complete'),
]
