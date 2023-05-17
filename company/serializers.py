from rest_framework import serializers
from .models import Video, Profile, Notification, Comment
from moviepy.video.io.VideoFileClip import VideoFileClip
from django.core.exceptions import ValidationError

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['user', 'video', 'title', 'number_of_views']
        

    def validate_video(self, value):
        video_type = value.content_type.split('/')[0]
        if video_type != 'video':
            raise ValidationError('File is not a video')

        video_ext = video.name.split('.')[-1]
        if video_ext not in ['mp4', 'avi', 'mov']:
            raise ValidationError('Unsupported video format')
                    
        video_clip = VideoFileClip(video.temporary_file_path())
        duration = video_clip.duration
        video_clip.close()
        if duration > 600: # 10 minute in seconds
            raise ValidationError('the video cannot be longer than 10 minute')
        return value

class CommentSerializer(serializers.ModelSerializer):
    post = VideoSerializer()
    class Meta:
        model = Comment
        fields = ['user', 'post', 'comments']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo', 'user', 'about', 'created_for', 'country', 'slug']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['link', 'user', 'message', 'read']