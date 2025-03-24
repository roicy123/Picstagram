from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from post.models import Post
from authy.models import Profile
from comment.models import Comment
from directs.models import Message
from notification.models import Notification 
from post.models import Tag
from post.models import Likes 
from post.models import Follow 
from post.models import Stream 
from reels.models import Reel
from django.db.models import Count
from django.contrib.auth import logout



def custom_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('custom_admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin user.')
    return render(request, 'custom_admin/login.html')

@login_required(login_url='custom_admin_login')
def custom_admin_dashboard(request):
    # Basic counts
    post_count = Post.objects.count()
    profile_count = Profile.objects.count()  # Use Profile instead of User
    comment_count = Comment.objects.count()

    # Posts over time (group by date)
    post_dates = Post.objects.values('posted').annotate(count=Count('id')).order_by('posted')
    post_counts = [item['count'] for item in post_dates]
    post_dates = [item['posted'].strftime('%Y-%m-%d') for item in post_dates]

    # User activity (example)
    activity_labels = ['Posts', 'Comments', 'Likes']
    activity_data = [post_count, comment_count, Likes.objects.count()]

    # Top liked posts
    top_liked_posts = Post.objects.order_by('-likes')[:5]

    # Most active profiles (instead of users)
    most_active_profiles = Profile.objects.annotate(post_count=Count('user__post')).order_by('-post_count')[:5]

    context = {
        'post_count': post_count,
        'profile_count': profile_count,  # Updated to profile_count
        'comment_count': comment_count,
        'post_dates': post_dates,
        'post_counts': post_counts,
        'activity_labels': activity_labels,
        'activity_data': activity_data,
        'top_liked_posts': top_liked_posts,
        'most_active_profiles': most_active_profiles,  # Updated to most_active_profiles
    }
    return render(request, 'custom_admin/dashboard.html', context)


@login_required(login_url='custom_admin_login')
def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'custom_admin/profile_list.html', {'profiles': profiles})

@login_required(login_url='custom_admin_login')
def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'custom_admin/comment_list.html', {'comments': comments})

@login_required(login_url='custom_admin_login')
def message_list(request):
    messages = Message.objects.all()
    return render(request, 'custom_admin/message_list.html', {'messages': messages})

@login_required(login_url='custom_admin_login')
def notification_list(request):
    notifications = Notification.objects.all()
    return render(request, 'custom_admin/notification_list.html', {'notifications': notifications})


@login_required(login_url='custom_admin_login')
def likes_list(request):
    likes = Likes.objects.all()
    return render(request, 'custom_admin/likes_list.html', {'likes': likes})

@login_required(login_url='custom_admin_login')
def follow_list(request):
    follows = Follow.objects.all()
    return render(request, 'custom_admin/follow_list.html', {'follows': follows})

@login_required(login_url='custom_admin_login')
def reel_list(request):
    reels = Reel.objects.all()
    return render(request, 'custom_admin/reel_list.html', {'reels': reels})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from authy.models import Profile
from authy.forms import EditProfileForm

@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'custom_admin/profile_detail.html', {'profile': profile})


@login_required
def profile_create(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = EditProfileForm()
    return render(request, 'custom_admin/profile_form.html', {'form': form})

@login_required
def profile_update(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'custom_admin/profile_form.html', {'form': form})

@login_required
def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        profile.delete()
        return redirect('profile_list')
    return render(request, 'custom_admin/profile_confirm_delete.html', {'profile': profile})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from comment.models import Comment 
from directs.models import Message 
from notification.models import Notification 
from post.models import Tag
from comment.forms import NewCommentForm 
from directs.forms import MessageForm
from notification.forms import NotificationForm

@login_required(login_url='custom_admin_login')
def comment_add(request):
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Comment added successfully!')
            return redirect('comment_list')
    else:
        form = NewCommentForm()
    return render(request, 'custom_admin/comment_form.html', {'form': form, 'action': 'Add'})

@login_required(login_url='custom_admin_login')
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = NewCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Comment updated successfully!')
            return redirect('comment_list')
    else:
        form = NewCommentForm(instance=comment)
    return render(request, 'custom_admin/comment_form.html', {'form': form, 'action': 'Edit'})

@login_required(login_url='custom_admin_login')
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        django_messages.success(request, 'Comment deleted successfully!')
        return redirect('comment_list')
    return render(request, 'custom_admin/delete_confirmation.html', {'object': comment, 'type': 'Comment'})

@login_required(login_url='custom_admin_login')
def message_add(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Message added successfully!')
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'custom_admin/message_form.html', {'form': form, 'action': 'Add'})

@login_required(login_url='custom_admin_login')
def message_edit(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Message updated successfully!')
            return redirect('message_list')
    else:
        form = MessageForm(instance=message)
    return render(request, 'custom_admin/message_form.html', {'form': form, 'action': 'Edit'})

@login_required(login_url='custom_admin_login')
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        django_messages.success(request, 'Message deleted successfully!')
        return redirect('message_list')
    return render(request, 'custom_admin/message_delete.html', {'object': message, 'type': 'Message'})


@login_required(login_url='custom_admin_login')
def notification_add(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Notification added successfully!')
            return redirect('notification_list')
    else:
        form = NotificationForm()
    return render(request, 'custom_admin/notification_form.html', {'form': form, 'action': 'Add'})

@login_required(login_url='custom_admin_login')
def notification_edit(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Notification updated successfully!')
            return redirect('notification_list')
    else:
        form = NotificationForm(instance=notification)
    return render(request, 'custom_admin/notification_form.html', {'form': form, 'action': 'Edit'})

@login_required(login_url='custom_admin_login')
def notification_delete(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':
        notification.delete()
        django_messages.success(request, 'Notification deleted successfully!')
        return redirect('notification_list')
    return render(request, 'custom_admin/notification_delete.html.html', {'object': notification, 'type': 'Notification'})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from post.models import Likes
from post.models import Follow
from reels.models import Reel
from post.forms import LikeForm
from post.forms import FollowForm 
from reels.forms import ReelForm

# Likes CRUD operations
@login_required(login_url='custom_admin_login')
def likes_list(request):
    likes = Likes.objects.all()
    return render(request, 'custom_admin/likes_list.html', {'likes': likes})

@login_required(login_url='custom_admin_login')
def likes_add(request):
    if request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Like added successfully!')
            return redirect('likes_list')
    else:
        form = LikeForm()
    return render(request, 'custom_admin/likes_form.html', {'form': form, 'action': 'Add'})

@login_required(login_url='custom_admin_login')
def likes_edit(request, pk):
    like = get_object_or_404(Likes, pk=pk)
    if request.method == 'POST':
        form = LikeForm(request.POST, instance=like)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Like updated successfully!')
            return redirect('likes_list')
    else:
        form = LikeForm(instance=like)
    return render(request, 'custom_admin/likes_form.html', {'form': form, 'action': 'Edit'})

@login_required(login_url='custom_admin_login')
def likes_delete(request, pk):
    like = get_object_or_404(Likes, pk=pk)
    if request.method == 'POST':
        like.delete()
        django_messages.success(request, 'Like deleted successfully!')
        return redirect('likes_list')
    return render(request, 'custom_admin/likes_delete.html', {'object': like})


# Follow CRUD operations
@login_required(login_url='custom_admin_login')
def follow_list(request):
    follows = Follow.objects.all()
    return render(request, 'custom_admin/follow_list.html', {'follows': follows})

@login_required(login_url='custom_admin_login')
def follow_add(request):
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Follow relationship added successfully!')
            return redirect('follow_list')
    else:
        form = FollowForm()
    return render(request, 'custom_admin/follow_form.html', {'form': form, 'action': 'Add'})

@login_required(login_url='custom_admin_login')
def follow_edit(request, pk):
    follow = get_object_or_404(Follow, pk=pk)
    if request.method == 'POST':
        form = FollowForm(request.POST, instance=follow)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Follow relationship updated successfully!')
            return redirect('follow_list')
    else:
        form = FollowForm(instance=follow)
    return render(request, 'custom_admin/follow_form.html', {'form': form, 'action': 'Edit'})

@login_required(login_url='custom_admin_login')
def follow_delete(request, pk):
    follow = get_object_or_404(Follow, pk=pk)
    if request.method == 'POST':
        follow.delete()
        django_messages.success(request, 'Follow relationship deleted successfully!')
        return redirect('follow_list')
    return render(request, 'custom_admin/follow_delete.html', {'object': follow})

# Reel CRUD operations
@login_required(login_url='custom_admin_login')
def reel_list(request):
    reels = Reel.objects.all()
    return render(request, 'custom_admin/reel_list.html', {'reels': reels})

@login_required(login_url='custom_admin_login')
def reel_add(request):
    if request.method == 'POST':
        form = ReelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Reel added successfully!')
            return redirect('reel_list')
    else:
        form = ReelForm()
    return render(request, 'custom_admin/reel_form.html', {'form': form, 'action': 'Add'})

@login_required(login_url='custom_admin_login')
def reel_edit(request, pk):
    reel = get_object_or_404(Reel, pk=pk)
    if request.method == 'POST':
        form = ReelForm(request.POST, request.FILES, instance=reel)
        if form.is_valid():
            form.save()
            django_messages.success(request, 'Reel updated successfully!')
            return redirect('reel_list')
    else:
        form = ReelForm(instance=reel)
    return render(request, 'custom_admin/reel_form.html', {'form': form, 'action': 'Edit'})

@login_required(login_url='custom_admin_login')
def reel_delete(request, pk):
    reel = get_object_or_404(Reel, pk=pk)
    if request.method == 'POST':
        reel.delete()
        django_messages.success(request, 'Reel deleted successfully!')
        return redirect('reel_list')
    return render(request, 'custom_admin/reel_delete.html', {'object': reel})

@login_required(login_url='custom_admin_login')
def custom_admin_logout(request):
    logout(request)
    return redirect('custom_admin_login')
