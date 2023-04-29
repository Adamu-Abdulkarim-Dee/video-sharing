from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, ReportVideo, Comment, Profile, Notification
from .forms import VideoForm, ReportVideoForm, CommentForm, ProfileForm
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from moviepy.video.io.VideoFileClip import VideoFileClip
from django.core.exceptions import ValidationError
import cv2
import numpy as np
import requests
from django.http import HttpResponseBadRequest

NUDE_URL = 'https://c1.ttcache.com/thumbnail/IgaD0XR4MSe/288x162/1160-wRj.jpg'


# Create your views here.
def videos(request):
    my_videos = Video.objects.all()
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    context = {
        'my_videos':my_videos,
        'unread_notifications':unread_notifications

    }
    return render(request, 'video/videos.html', context)

def play_video(request, slug):
    play = get_object_or_404(Video, slug=slug)
    public_comments = Comment.objects.filter(post_id=play)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comments = form.cleaned_data['comments']
            new_comment = Comment.objects.create(
                comments=comments, post=play, user=request.user
            )
            Notification.objects.create(
                user=request.user,
                url=play,
                message='someone commented on your post'
            )
            return redirect('Video')
    else:
        form = CommentForm()

    context = {
        'play':play,
        'public_comments':public_comments,
        'form':form,
    }
    return render(request, 'video/play_video.html', context)

class NotificationListView(ListView):
    model = Notification
    template_name = 'video/notification.html'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-timestmap")


def complaint_page(request):
    reports = ReportVideo.objects.all()

    context = {
        'reports':reports
    }
    return render(request, 'control/complaint_video.html', context)

class ComplainReport(CreateView):
    model = ReportVideo
    form_class = ReportVideoForm
    template_name = 'control/complaint_video_create.html'
    success_url = reverse_lazy('Video')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super(ComplainReport, self).form_valid(form)

class VideoComplainReport(CreateView):
    model = ReportVideo
    form_class = ReportVideoForm
    template_name = 'control/complaint_video_create.html'
    success_url = reverse_lazy('Video')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super(VideoComplainReport, self).form_valid(form)

def create_video(request):
    if request.method == 'POST':
        title = request.POST['title']
        video = request.FILES.get('video')
        banner = request.FILES.get('banner')

        cap = cv2.VideoCapture(str(video))

        while(cap.isOpened()):
            ret, frame = cap.read()

            # Resize the frame to the same size as the nudity image
            frame_resized = cv2.resize(frame, (640, 480))

            # Convert the nudity image to grayscale
            response = requests.get(NUDE_URL)
            img_array = np.array(bytearray(response.content), dtype=np.uint8)
            img_gray = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

            # Perform template matching
            result = cv2.matchTemplate(frame_resized, img_gray, cv2.TM_CCOEFF_NORMED)
            if np.max(result) > 0.9:
                return HttpResponseBadRequest('This video contains nudes, but nudes are not allowed')

        if video:
            video_type = video.content_type.split('/')[0]
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

            new_video = Video.objects.create(
                user=request.user,
                title=title,
                video=video,
                banner=banner
            )
            new_video.save()
            return redirect('Video')
        else:
            raise ValidationError('No video file uploaded')

    return render(request, 'video/create_video.html')




def profile(request):
    books = Video.objects.filter(user=request.user)
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'books': books,
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)

def public_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    videos = Video.objects.filter(user=profile.user)
    context = {
        'profile': profile,
        'videos':videos
    }
    return render(request, 'public_profile.html', context)

class EditProfile(UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('Dashboard')
    form_class = ProfileForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EditProfile, self).form_valid(form)