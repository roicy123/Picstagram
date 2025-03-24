from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login


from post.models import Post, Follow, Stream
from django.contrib.auth.models import User
from authy.models import Profile
from .forms import EditProfileForm, UserRegisterForm
from django.urls import resolve
from comment.models import Comment

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.core.mail import send_mail
from .forms import PasswordResetForm

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.http import HttpResponse


def UserProfile(request, username):
    try:
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        messages.error(request, "The profile you're looking for does not exist.")
        return redirect('index')

    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

    if url_name != 'profile':
        posts = profile.favourite.all()

    # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # Pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'profile': profile,
        'posts_count': posts_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'posts_paginator': posts_paginator,
        'follow_status': follow_status,
    }
    return render(request, 'profile.html', context)
def EditProfile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, "Profile does not exist.")
        return redirect('index')

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile', profile.user.username)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(instance=profile)

    context = {
        'form': form,
    }
    return render(request, 'editprofile.html', context)


def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    if option not in ['0', '1']:
        messages.error(request, "Invalid option for follow action.")
        return HttpResponseRedirect(reverse('profile', args=[username]))

    try:
        f, created = Follow.objects.get_or_create(follower=user, following=following)
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=user).delete()
        else:
            posts = Post.objects.filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, date=post.posted, following=following)
                    stream.save()

        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return HttpResponseRedirect(reverse('profile', args=[username]))


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                new_user = form.save()
                messages.success(request, 'Hurray, your account was created!')
                # Automatically log in the user
                new_user = authenticate(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1')
                )
                if new_user:
                    login(request, new_user)
                    return redirect('index')
                else:
                    messages.error(request, "Authentication failed. Please log in manually.")
                    return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('sign-up')
        else:
            messages.error(request, "Invalid form submission. Please correct the errors below.")
    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'sign-up.html', context)
