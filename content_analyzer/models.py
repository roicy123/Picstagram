# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ContentAnalysis(models.Model):
    POST_TYPES = (
        ('general', 'General Post'),
        ('photo', 'Photo Caption'),
        ('video', 'Video Description'),
        ('story', 'Story'),
        ('reel', 'Reel'),
    )

    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='general')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=20)
    engagement_score = models.FloatField()
    safety_score = models.FloatField()
    is_safe = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    improved_content = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Content Analyses'

class ContentKeyword(models.Model):
    analysis = models.ForeignKey(ContentAnalysis, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    score = models.FloatField()

class ContentHashtag(models.Model):
    analysis = models.ForeignKey(ContentAnalysis, on_delete=models.CASCADE)
    hashtag = models.CharField(max_length=100)
    is_suggested = models.BooleanField(default=False)