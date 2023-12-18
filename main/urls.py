from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/<slug:user_slug>', views.dashboard, name='dashboard'),
    path('dashboard/<slug:user_slug>/posts', views.posts, name='posts'),
    path('follow', views.follow, name='follow'),
    path('comment', views.comment, name='comment'),
    path('search', views.search, name='search'),
    path('upload', views.upload, name='upload'),
    path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.Logout, name='logout'),
]

