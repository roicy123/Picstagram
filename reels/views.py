from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reel
from .forms import ReelForm

# Upload a Reel
@login_required
def upload_reel(request):
    if request.method == 'POST':
        form = ReelForm(request.POST, request.FILES)
        if form.is_valid():
            # Check for required fields and size constraints
            if not request.FILES.get('video'):
                messages.error(request, "A video file is required.")
                return render(request, 'upload_reel.html', {'form': form})

            if request.FILES['video'].size > 50 * 1024 * 1024:  # Limit to 50MB
                messages.error(request, "The video file size must be less than 50MB.")
                return render(request, 'upload_reel.html', {'form': form})

            reel = form.save(commit=False)
            reel.user = request.user
            reel.save()
            messages.success(request, "Reel uploaded successfully!")
            return redirect('reels-feed')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReelForm()

    return render(request, 'upload_reel.html', {'form': form})

# View the Reels Feed
def reels_feed(request):
    reels = Reel.objects.all().order_by('-created_at')

    if not reels.exists():
        messages.info(request, "No reels available yet. Be the first to upload!")

    return render(request, 'reels_feed.html', {'reels': reels})

# Like or Unlike a Reel
@login_required
def like_reel(request, reel_id):
    reel = get_object_or_404(Reel, id=reel_id)

    # Check if the user has already liked the reel
    if request.user in reel.likes.all():
        reel.likes.remove(request.user)
        messages.info(request, "You unliked the reel.")
    else:
        reel.likes.add(request.user)
        messages.success(request, "You liked the reel!")

    # Redirect back to the reels feed
    return redirect('reels-feed')
