from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('feed/', views.feed, name="feed"),
    path('post/<str:pk>/', views.post, name="post"),
    path('feedback', views.feedback, name="feedback"),
    path('account', views.account, name="account"),
    path('delete-reply/<str:pk>/', views.deleteReply, name="delete-reply"),
    path('all-discussions', views.allDiscussions, name="all-discussions"),
    path('latest/', views.latest_post, name="latest_post"),
    
    path('fact-check/', views.fact_check, name='fact_check'),
]