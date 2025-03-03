from django.db import models
from django.contrib.auth.models import User

class Reel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reels')
    video = models.FileField(upload_to='reels/')
    caption = models.TextField(max_length=300, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_reels', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.caption[:20]}"
