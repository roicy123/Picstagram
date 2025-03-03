from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['post', 'sender', 'user', 'notification_types', 'text_preview', 'is_seen']
        widgets = {
            'post': forms.Select(attrs={'class': 'form-control'}),
            'sender': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'notification_types': forms.Select(attrs={'class': 'form-control'}),
            'text_preview': forms.TextInput(attrs={'class': 'form-control'}),
            'is_seen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }