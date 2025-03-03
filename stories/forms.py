# forms.py
from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['media', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Add a caption...'}),
        }

