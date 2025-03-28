"""ig_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from elements import views as e_views
# from authusers import views as auth_views
from authy.views import UserProfile, follow
from marketplace import views as marketplace


urlpatterns = [
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path('users/', include('authy.urls')),
    path('', include('post.urls')),
    path('message/', include('directs.urls')),
    path('notifications/', include('notification.urls')),
    path('reels', include('reels.urls')),
    path('custom-admin/', include('custom_admin.urls')),
    path('/chatbot', include('chatbot.urls')),
    path('stories/', include('stories.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('password/', include('password.urls')),

    path('payment-success/', marketplace.payment_success, name='payment_success'),

    # profile
    path('<username>/', UserProfile, name='profile'),
    path('<username>/saved/', UserProfile, name='profilefavourite'),
    path('<username>/follow/<option>/', follow, name='follow'),

]

# This is used for
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
