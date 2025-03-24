from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404

from post.models import Post, Tag, Follow, Stream, Likes
from django.contrib.auth.models import User
from post.forms import NewPostform
from authy.models import Profile
from comment.models import Comment
from comment.forms import NewCommentForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from stories.models import Story
from .content_analyzer import validate_content
import json

@login_required
def index(request):
    user = request.user
    if not user.is_authenticated:
        raise Http404("User not authenticated")

    # Get all users the current user is following
    following_users_ids = Follow.objects.filter(follower=user).values_list('following__id', flat=True)

    # Exclude the current user, users they are already following, and the user with username 'admin'
    all_users = User.objects.exclude(id=user.id).exclude(id__in=following_users_ids).exclude(username='admin')

    # Fetch posts for the user's feed
    posts = Stream.objects.filter(user=user)
    group_ids = [post.post_id for post in posts]
    post_items = Post.objects.filter(id__in=group_ids).order_by('-posted')

    # Add stories data
    # Get the users the current user is following using the Follow model
    following_users = [follow.following for follow in Follow.objects.filter(follower=request.user)]
    active_stories = Story.objects.filter(
        expires_at__gt=timezone.now(),
        user__in= following_users + [request.user] #Include current user to see their own active stories
    ).select_related('user')

    # Group stories by user
    stories_by_user = {}
    viewed_profiles = set()

    for story in active_stories:
        if story.user not in stories_by_user:
            stories_by_user[story.user] = []
        stories_by_user[story.user].append(story)

        # Check if user has viewed this story
        if story.views.filter(user=request.user).exists():
            viewed_profiles.add(story.user.profile) # Use .profile to access profile

    query = request.GET.get('q')
    users_paginator = None
    if query:
        users = User.objects.filter(Q(username__icontains=query)).exclude(id=user.id).exclude(username='admin')
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

    context = {
        'post_items': post_items,
        'profile': Profile.objects.all(), #Fixed.  Iterate over profiles, not a single profile object.
        'all_users': all_users,  # Filtered suggestion list
        'users_paginator': users_paginator,
        'stories_by_user': stories_by_user,
        'viewed_profiles': viewed_profiles,
    }
    return render(request, 'index.html', context)

class ContentAnalyzedPostForm(NewPostform):
    """Extended post form with content analysis"""
    
    def clean(self):
        cleaned_data = super().clean()
        caption = cleaned_data.get('caption', '')
        picture = cleaned_data.get('picture')
        
        # Analyze content
        results = validate_content(caption, picture)
        
        # Store recommendations for view to display
        self.content_analysis_results = results
        
        return cleaned_data

@login_required
def NewPost(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    content_analysis_results = None

    if request.method == "POST":
        form = ContentAnalyzedPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags', '')
            
            # Get analysis results
            content_analysis_results = getattr(form, 'content_analysis_results', None)
            
            # Check if user wants to proceed despite recommendations
            if 'ignore_recommendations' not in request.POST and content_analysis_results and content_analysis_results['recommendations']:
                # Show recommendations before posting
                context = {
                    'form': form,
                    'analysis_results': content_analysis_results,
                    'show_recommendations': True
                }
                return render(request, 'newpost.html', context)
            
            # Process tags
            tag_list = [tag.strip() for tag in tag_form.split(',') if tag.strip()]
            
            # Add suggested hashtags if enabled
            if 'use_suggested_hashtags' in request.POST and content_analysis_results and content_analysis_results.get('text_analysis', {}).get('suggested_hashtags'):
                for tag in content_analysis_results['text_analysis']['suggested_hashtags'][:5]:  # Limit to 5 suggestions
                    if tag not in tag_list:
                        tag_list.append(tag)
            
            tags_obj = [Tag.objects.get_or_create(title=tag)[0] for tag in tag_list]

            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tags.set(tags_obj)
            
            # Store reach score and analysis metadata
            if content_analysis_results:
                p.reach_score = content_analysis_results.get('reach_score', 0)
                p.content_analysis = json.dumps(content_analysis_results)
            
            p.save()
            return redirect('profile', request.user.username)
    else:
        form = ContentAnalyzedPostForm()
    
    context = {
        'form': form,
        'analysis_results': content_analysis_results
    }
    return render(request, 'newpost.html', context)

@login_required
def PostDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not post:
        raise Http404("Post does not exist")

    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('post-details', args=[post.id]))
    else:
        form = NewCommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'postdetail.html', context)

@login_required
def Tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    if not posts.exists():
        raise Http404("No posts found for this tag")

    context = {
        'posts': posts,
        'tag': tag
    }
    return render(request, 'tag.html', context)

@login_required
def like(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    if post.user == user:
        raise Http404("You cannot like your own post")

    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).exists()

    if not liked:
        Likes.objects.create(user=user, post=post)
        post.likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        post.likes = current_likes - 1

    post.save()
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))

@login_required
def favourite(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))

@login_required
def likes_list(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likes = Likes.objects.filter(post=post).select_related('user')

    if not likes.exists():
        raise Http404("No likes found for this post")

    context = {
        'post': post,
        'likes': likes,
    }
    return render(request, 'likes_list.html', context)

@login_required
def followers(request):
    user = request.user
    followers = Follow.objects.filter(following=user).select_related('follower')

    if not followers.exists():
        raise Http404("You have no followers")

    context = {
        'followers': followers,
    }
    return render(request, 'followers.html', context)

@login_required
def following(request):
    user = request.user
    following = Follow.objects.filter(follower=user).select_related('following')

    if not following.exists():
        raise Http404("You are not following anyone")

    context = {
        'following': following,
    }
    return render(request, 'following.html', context)
