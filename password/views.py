from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import PasswordResetOTP
from .forms import PasswordResetRequestForm, PasswordResetOTPForm, PasswordResetForm
from django.contrib import messages
from django.utils import timezone

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            otp = PasswordResetOTP(user=user)
            otp.save()

            # Send OTP via Email
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is: {otp.otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(request, 'An OTP has been sent to your email address.')
            return redirect('validate_otp', user.id)
    else:
        form = PasswordResetRequestForm()

    return render(request, 'password_reset_request.html', {'form': form})

def validate_otp(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = PasswordResetOTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            try:
                otp_record = PasswordResetOTP.objects.get(user=user, otp=otp)
                if otp_record.expires_at > timezone.now():
                    return redirect('reset_password', user.id)
                else:
                    messages.error(request, 'OTP has expired.')
            except PasswordResetOTP.DoesNotExist:
                messages.error(request, 'Invalid OTP.')
    else:
        form = PasswordResetOTPForm()

    return render(request, 'validate_otp.html', {'form': form})

def reset_password(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('sign-in')
    else:
        form = PasswordResetForm()

    return render(request, 'reset_password.html', {'form': form})