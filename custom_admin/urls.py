from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_admin_login, name='custom_admin_login'),
    path('dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('comments/', views.comment_list, name='comment_list'),
    path('messages/', views.message_list, name='message_list'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('likes/', views.likes_list, name='likes_list'),
    path('follows/', views.follow_list, name='follow_list'),
    path('reels/', views.reel_list, name='reel_list'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('profiles/new/', views.profile_create, name='profile_create'),
    path('profiles/<int:pk>/edit/', views.profile_update, name='profile_update'),
    path('profiles/<int:pk>/delete/', views.profile_delete, name='profile_delete'),

    path('comments/add/', views.comment_add, name='comment_add'),
    path('comments/edit/<int:pk>/', views.comment_edit, name='comment_edit'),
    path('comments/delete/<int:pk>/', views.comment_delete, name='comment_delete'),
    
    # Message URLs
    path('messages/add/', views.message_add, name='message_add'),
    path('messages/edit/<int:pk>/', views.message_edit, name='message_edit'),
    path('messages/delete/<int:pk>/', views.message_delete, name='message_delete'),
    
    # Notification URLs
    path('notifications/add/', views.notification_add, name='notification_add'),
    path('notifications/edit/<int:pk>/', views.notification_edit, name='notification_edit'),
    path('notifications/delete/<int:pk>/', views.notification_delete, name='notification_delete'),

    # Like URLs
    path('likes/add/', views.likes_add, name='likes_add'),
    path('likes/edit/<int:pk>/', views.likes_edit, name='likes_edit'),
    path('likes/delete/<int:pk>/', views.likes_delete, name='likes_delete'),
    
    # Follow URLs
    path('follows/add/', views.follow_add, name='follow_add'),
    path('follows/edit/<int:pk>/', views.follow_edit, name='follow_edit'),
    path('follows/delete/<int:pk>/', views.follow_delete, name='follow_delete'),
    
    # Reel URLs
    path('reels/add/', views.reel_add, name='reel_add'),
    path('reels/edit/<int:pk>/', views.reel_edit, name='reel_edit'),
    path('reels/delete/<int:pk>/', views.reel_delete, name='reel_delete'),
    
    # Logout URL
    path('logout/', views.custom_admin_logout, name='custom_admin_logout'),
]