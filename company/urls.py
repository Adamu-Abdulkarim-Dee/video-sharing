from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),

    path('videos/api/', views.video),

    path('video/create/', views.create_video),

    path('comment/video/api/<slug:slug>/', views.comment_video),

    path('user_profile/api/', views.profile),

    path('public_user/profile/api/<slug:slug>', views.public_profile),

    path('update_user/profile/api/<slug:slug>', views.update_profile),

    path('notification/api/', views.notification),
]