from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Video, Profile
from .serializers import VideoSerializer, ProfileSerializer, NotificationSerializer

@api_view(['GET'])
def video(request):
    videos = Video.objects.all()
    serialiazer = VideoSerializer(videos, many=True)
    return Response(serialiazer.data)

@api_view(['POST'])
def create_video(request):
    serialiazer = VideoSerializer(data=request.data)
    if serialiazer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HHTP_201_CREATED)
    return Response(serialiazer.erros, status=status.HTTP_400_BAD_REQEST)


@api_view(['POST'])
def comment_video(request, slug):
    video = Video.objects.get(slug=slug)
    comments = Comment.objects.create(
        user=request.user,
        post=video,
        comments=comments
    )
    serializer = CommentSerializer(comments, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def profile(request):
    profiles = Profile.objects.filter(user=request.user)
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def public_profile(request, slug):
    profile = Profile.objects.get(slug=slug)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def update_profile(request, slug):
    data = request.data
    profile = Profile.objects.get(slug=slug)
    serializer = ProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def notification(request):
    notifications = Notification.objects.filter(user=request.user)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)





def home(request):
    return render(request, 'home.html')
