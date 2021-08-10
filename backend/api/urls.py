from . import views_accounts
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('csrf', views_accounts.csrf_check, name='csrf'),

    path('users-list/',views_accounts.GetAllUsersAPIView.as_view(),name='allusers'),
    path('users/create/',views_accounts.CreateUserAPIView.as_view(),name='user-create'),
    path('users/update/<int:pk>',views_accounts.UpdateUsersAPIView.as_view(),name='user-update'),
    path('users/delete/<int:pk>',views_accounts.DeleteUsersAPIView.as_view(),name='user-delete'),
    path('users/<int:pk>/',views_accounts.GetUserAPIView.as_view(),name='user'),
    # path('users/<int:pk>/',views.GetUserAPIView.as_view(),name='user'),
    path('users/auth_user/',views.current_user,name='current_user'),
    path('users/profiles/',views.ProfileAPIView.as_view(),name='profiles'),
    path('users/profiles/user/<str:email>/',views.ProfileDetailAPIView.as_view(),name='user-profile'),
    path('users/profiles/update/',views.ProfileUpdateAPIView.as_view(),name='update-profile'),
    path('users/profiles/follow/<int:pk>/',views.FollowAPIView.as_view(),name='follow-unfollow'),
    path('users/profiles/<str:email>/followers/',views.FollowersListAPIView.as_view(),name='follower-list'),
    path('users/profiles/<str:email>/followings/',views.FollowingsListAPIView.as_view(),name='following-list'),

    path('posts/',views.AllPostsAPIView.as_view(),name='posts'),
    path('<int:pk>/',views.PostDetailAPIView.as_view(),name='post-details'),
    path('user_posts/',views.UserAllPostsAPIView.as_view(),name='user_posts'),
    path('upload/', views.UploadPostAPIView.as_view(), name='upload'),
    path('likes/',views.LikeAPIView.as_view(),name='likes'),
    path('rate/',views.RatingAPIView.as_view(),name='rate'),
    path('post-likes/<int:pk>/',views.PostLikerAPIView.as_view(),name='post-likes'),
    path('user/<str:email>/',views.UserPostsView.as_view(),name='user-posts'),
]