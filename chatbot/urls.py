# chatbot/urls.py
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
]