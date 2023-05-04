from django import forms
from .models import Video, ReportVideo, Comment, Profile
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.forms import FileField


class CommentForm(forms.ModelForm):
    comments = forms.CharField(label='Comments', widget=forms.Textarea(attrs={'rows':'1'}), max_length=200)

    class Meta:
        model = Comment
        fields = ['comments']

class VideoForm(forms.ModelForm):
    video = FileField(validators=[FileExtensionValidator(allowed_extensions=['mp4'])])        
        
    class Meta:
        model = Video
        fields = ['title', 'video', 'banner']

class ReportVideoForm(forms.ModelForm):
    class Meta:
        model = ReportVideo
        fields = ['this_is', 'more_information', ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo', 'about', 'twitter', 'linkedln', 'website', 'country']