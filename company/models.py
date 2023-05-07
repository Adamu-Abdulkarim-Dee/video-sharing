from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils.text import slugify
from django.conf import settings
import random
import string
from django.urls import reverse
from .choices import *

class Video(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    video = models.FileField(upload_to='videos')
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True)


    def get_user_public_url(self):
        return reverse('Public-Profile', kwargs={'slug': self.user.profile.slug})

    def get_user_photo(self):
        return self.user.profile.profile_photo.url

    def save(self, *args, **kwargs):
        if not self.slug:
            # generate a random 6-character string
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            self.slug = f"{slugify(self.title)}-{random_string}"
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.video)





class ReportVideo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    COMPLAINT = (
        ('Pornography', 'Pornography'),
        ('Graphic Violence', 'Graphic Violence'),
        ('Predators Behavior', 'Predators Behavior'),
    )
    this_is = models.CharField(max_length=100, choices=COMPLAINT)
    more_information = models.TextField(max_length=400)
    post = models.ForeignKey(Video, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)








class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile-image', default='static/dafault.jpg')
    twitter = models.URLField(blank=True, null=True, unique=True)
    website = models.URLField(blank=True, null=True, unique=True)
    linkedln = models.URLField(blank=True, null=True, unique=True)
    country = models.CharField(max_length=70, blank=True, null=True,)
    about = models.TextField(max_length=700, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    comments = models.TextField(max_length=200)
    post = models.ForeignKey(Video, on_delete=models.CASCADE)

    def get_user_public_url(self):
        return reverse('Public-Profile', kwargs={'slug': self.user.profile.slug})

    def get_user_photo(self):
        return self.user.profile.profile_photo.url

    def __str__(self):
        return str(self.user)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField()
    read = models.BooleanField(default=False)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    country = models.CharField(choices=LIST_OF_COUNTRY, max_length=35)
    created_for = models.CharField(choices=CREATED_FOR, max_length=35)
    is_verified = models.BooleanField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return str(self.username)
