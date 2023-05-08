from django import forms
from .models import Video, ReportVideo, Comment, Profile, CustomUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.forms import FileField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email')

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", "username", "country", "created_for", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password")


class CommentForm(forms.ModelForm):
    comments = forms.CharField(label='Comments', max_length=50)

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
        fields = ['profile_photo', 'twitter', 'website']