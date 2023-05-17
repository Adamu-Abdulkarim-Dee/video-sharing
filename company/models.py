from django.db import models
from .choices import *
from django.utils.text import slugify
from django.conf import settings
import random
import string
from django.urls import reverse

class Video(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    video = models.FileField(upload_to='videos')
    created_on = models.DateTimeField(auto_now_add=True)
    number_of_views = models.IntegerField(default=0)

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



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile-image', default='static/dafault.jpg')
    about = models.TextField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, choices=LIST_OF_COUNTRY, blank=True, null=True)
    created_for = models.CharField(max_length=50, choices=CREATED_FOR, blank=True, null=True)

    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    comments = models.CharField(max_length=50)
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

    def get_user_public_url(self):
        return reverse('Public-Profile', kwargs={'slug': self.user.profile.slug})

    def get_user_photo(self):
        return self.user.profile.profile_photo.url

    def __str__(self):
        return str(self.user)
