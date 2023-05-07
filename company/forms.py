from django import forms
from .models import Video, ReportVideo, Comment, Profile, CustomUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.forms import FileField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", "username", "country", "created_for", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CommentForm(forms.ModelForm):
    comments = forms.CharField(label='Comments', widget=forms.Textarea(attrs={'rows':'1'}), max_length=200)

    class Meta:
        model = Comment
        fields = ['comments']

class ReportVideoForm(forms.ModelForm):
    class Meta:
        model = ReportVideo
        fields = ['this_is', 'more_information', ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo', 'about', 'twitter', 'linkedln', 'website', 'country']