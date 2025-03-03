# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Story, StoryView, StoryLike
from .forms import StoryForm

@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            
            # Check if uploaded file is video
            file_extension = story.media.name.split('.')[-1].lower()
            if file_extension in ['mp4', 'mov', 'avi']:
                story.is_video = True
                
            story.save()
            return redirect('index')
    else:
        form = StoryForm()
    
    return render(request, 'create_story.html', {'form': form})


@login_required
def view_stories(request):
    # Get users the current user follows
    following_users = request.user.profile.following.all()
    
    # Get active stories from users the current user follows and the user themselves
    active_stories = Story.objects.filter(
        expires_at__gt=timezone.now(),
        user__in=list(following_users) + [request.user]
    ).select_related('user').prefetch_related('views', 'likes')
    
    # Group stories by user
    stories_by_user = {}
    for story in active_stories:
        if story.user not in stories_by_user:
            stories_by_user[story.user] = []
        stories_by_user[story.user].append(story)
    
    context = {
        'stories_by_user': stories_by_user,
    }
    
    return render(request, 'view_stories.html', context)


@login_required
def view_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, expires_at__gt=timezone.now())
    
    # Record that user has viewed this story
    StoryView.objects.get_or_create(story=story, user=request.user)
    
    # Get all stories from this user that are active
    user_stories = Story.objects.filter(
        user=story.user,
        expires_at__gt=timezone.now()
    ).order_by('created_at')
    
    # Get indices for navigation
    story_ids = list(user_stories.values_list('id', flat=True))
    current_index = story_ids.index(story.id)
    prev_id = story_ids[current_index - 1] if current_index > 0 else None
    next_id = story_ids[current_index + 1] if current_index < len(story_ids) - 1 else None
    
    # Check if current user has liked this story
    has_liked = StoryLike.objects.filter(story=story, user=request.user).exists()
    
    context = {
        'story': story,
        'prev_id': prev_id,
        'next_id': next_id,
        'has_liked': has_liked,
        'likes_count': story.likes.count(),
        'views_count': story.views.count(),
    }
    
    return render(request, 'story_detail.html', context)


@login_required
def like_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, expires_at__gt=timezone.now())
    
    like, created = StoryLike.objects.get_or_create(story=story, user=request.user)
    
    if request.is_ajax():
        return JsonResponse({
            'status': 'success',
            'liked': created,
            'likes_count': story.likes.count()
        })
    
    return HttpResponseRedirect(reverse('view_story', args=[story_id]))
