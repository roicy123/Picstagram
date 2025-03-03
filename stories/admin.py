from django.contrib import admin

from stories.models import Story, StoryView, StoryLike

# Register your models here.
admin.site.register(Story)

admin.site.register(StoryView)

admin.site.register(StoryLike)