from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from moviepy.video.io.VideoFileClip import VideoFileClip
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

def dashboard(request):
    my_videos = Video.objects.all()
    context = {
        'my_videos':my_videos,
    }
    return render(request, 'dashboard.html', context)

def videos(request):
    unread_notifications = Notification.objects.filter(user=request.user, read=False).count()
    my_videos = Video.objects.all()
    context = {
        'my_videos':my_videos,
        'unread_notifications': unread_notifications
    }
    return render(request, 'video/videos.html', context)

def play_video(request, slug):
    post = get_object_or_404(Video, slug=slug)
    public_comments = Comment.objects.filter(post_id=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comments = form.cleaned_data['comments']
            new_comment = Comment.objects.create(
                comments=comments, post=post, user=request.user
            )
            return redirect('Video')
    else:
        form = CommentForm()

    context = {
        'post':post,
        'public_comments':public_comments,
        'form':form,
    }
    return render(request, 'video/play_video.html', context)

def notification(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-id')
    return render(request, 'video/notification.html', {'notifications':notifications})






def all_users(request):
    users = CustomUser.objects.all()
    context = {
        'users': users
    }
    return render(request, 'control/user.html', context)

class Delete_users(DeleteView):
    model = CustomUser
    

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
            )
            new_video.save()
            return redirect('Video')
        else:
            raise ValidationError('No video file uploaded')

    return render(request, 'video/create_video.html')







def profile(request):
    user_profile = Profile.objects.filter(user=request.user)
    videos = Video.objects.filter(user=request.user)
    context = {
        'videos': videos,
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


'''
for registration and login system
'''

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form':form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('Video')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})
