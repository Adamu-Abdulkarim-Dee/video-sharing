from django.contrib import admin
from .models import Profile, Video, ReportVideo, Comment, Notification

admin.site.register(Profile)
admin.site.register(Video)
admin.site.register(ReportVideo)
admin.site.register(Comment)
admin.site.register(Notification)