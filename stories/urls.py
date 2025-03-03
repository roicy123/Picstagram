# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('story/create/', views.create_story, name='create_story'),
    path('stories/', views.view_stories, name='view_stories'),
    path('story/<int:story_id>/', views.view_story, name='view_story'),
    path('story/<int:story_id>/like/', views.like_story, name='like_story'),
]