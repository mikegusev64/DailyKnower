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
    path('delete-reply/<str:pk>/', views.deleteReply, name="delete-reply"),
    path('all-discussions', views.allDiscussions, name="all-discussions"),
    path('latest/', views.latest_post, name="latest_post"),
    
    path('fact-check/', views.fact_check, name='fact_check'),
    path('save-note/', views.save_note, name="save_note"),
    path('get-notes/<int:topic_id>/', views.get_notes, name='get_notes'),
    path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('account/', views.accountPage, name="account"),
]