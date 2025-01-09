from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from mainapp import views


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
    path('subscribe/', views.subscribe, name='subscribe'),
    path('cancel/', views.cancel, name='cancel'),
    path('success/', views.success, name='success'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('direct-to-customer-portal/', views.direct_to_customer_portal, name='direct-to-customer-portal'),
    path('collect-stripe-webhook/', views.collect_stripe_webhook, name='collect-stripe-webhook'),


]