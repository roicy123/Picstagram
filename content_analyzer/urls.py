# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('analyze/', views.analyze_content, name='analyze'),
    path('history/', views.analysis_history, name='history'),
]