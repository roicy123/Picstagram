from django import forms
from post.models import Post, Likes, Follow


class NewPostform(forms.ModelForm):
    # content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
    
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Caption'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tags | Seperate with comma'}), required=True)

    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tags']

class LikeForm(forms.ModelForm):
    class Meta:
        model = Likes
        fields = ['user', 'post']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'post': forms.Select(attrs={'class': 'form-control'}),
        }

class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ['follower', 'following']
        widgets = {
            'follower': forms.Select(attrs={'class': 'form-control'}),
            'following': forms.Select(attrs={'class': 'form-control'}),
        }
