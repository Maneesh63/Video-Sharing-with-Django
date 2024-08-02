from django.urls import path
from . import views

urlpatterns=[

     path('',views.home,name='home'),
    
     path('signup/',views.signup,name='signup'),

     path('login/',views.login,name='login'),

     path('logout/',views.logout,name='logout'),

     path('create/',views.video_create,name='create_video'),

     path('edit_video/<int:pk>/',views.edit_video,name='edit_video'),

     path('delete_video/<int:pk>/',views.delete_video,name='delete_video'),

     path('dashboard/<int:pk>/', views.dashboard, name='dashboard'),

     path('edit_dashboard/<int:pk>', views.edit_dashboard, name='edit_dashboard'),

     path('video_detail/<int:pk>/',views.video_detail,name='video_detail'),
      
        path('video/<int:pk>/like/', views.like_video, name='like_video'),
        path('video/<int:pk>/unlike/', views.unlike_video, name='unlike_video'),

    path('follow/<int:pk>/', views.follow, name='follow_user'),
    path('unfollow/<int:pk>/',views.unfollow_user, name='unfollow_user'),

     path('followers_list/<int:pk>/', views.followers_list, name='followers_list'),
    path('following_list/<int:pk>/', views.following_list, name='following_list'),

    path('createcomment/<int:pk>/',views.createcomment,name='createcomment'),

    path('listcomment/',views.listcomment,name='listcomment')
]       