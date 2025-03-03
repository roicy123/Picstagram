from django.urls import path
from post.views import index, NewPost, PostDetail, Tags, like, favourite, likes_list, followers, following
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('newpost', NewPost, name='newpost'),
    path('<uuid:post_id>', PostDetail, name='post-details'),
    path('tag/<slug:tag_slug>', Tags, name='tags'),
    path('<uuid:post_id>/like', like, name='like'),
    path('<uuid:post_id>/favourite', favourite, name='favourite'),
    path('post/<uuid:post_id>/likes/', likes_list, name='likes-list'),
    path('followers/', followers, name='followers'),
    path('following/', following, name='following'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
