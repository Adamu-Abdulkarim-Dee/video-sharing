from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='Dashboard'),
    path('home', views.videos, name='Video'),
    path('video-play/<slug:slug>/', views.play_video, name='Play-Video'),
    path('notification/', views.notification, name='Notification'),

    path('delete-user', views.all_users, name='users'),
    path('delete<slug:slug>', views.Delete_users.as_view(), name='Delete-user'),
    path('compaint-super-user', views.complaint_page, name='Complain'),

    path('CreateVideo', views.create_video, name='Create-Video'),
    path('videos-play/<int:pk>/', views.ComplainReport.as_view(), name='Complain-Video'),

    path('videos-play-complaint/<int:pk>', views.VideoComplainReport.as_view(), name='Complain-Video'),

    path('my-profile', views.profile, name='Profile'),
    path('profile/<slug:slug>/', views.public_profile, name='Public-Profile'),

    path('register', views.register, name='Register'),
    path('login', views.login, name='Login'),

    path('edit-profile/<slug:slug>/', views.EditProfile.as_view(), name='Edit-Profile'),
]