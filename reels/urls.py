from django.urls import path
from . import views

urlpatterns = [
    # Reels-related views
    path('reels/', views.reels_feed, name='reels-feed'),  # Display all reels
    path('reels/upload/', views.upload_reel, name='upload-reel'),  # Upload a new reel
    path('reels/like/<int:reel_id>/', views.like_reel, name='like-reel'),  # Like/unlike a reel
]
