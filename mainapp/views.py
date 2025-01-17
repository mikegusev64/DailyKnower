from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from .models import adminPost, dkTopic, allReply, topicTheme, Notes
from django.contrib.auth.models import User
from django.views.generic import ListView
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import os
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from datetime import date


from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse

import stripe
from django.contrib.auth import login

from . import models
from django.contrib import admin
from django.urls import path, include
from mainapp import views
from django.core.paginator import Paginator
from .forms import UserForm






# Create your views here.


def loginPage(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        
        
        try:
            user = User.objects.get(username=username,)
        except:
            messages.error(request, "User does not exist.")
            
            
        user = authenticate(request, username=username, password=password)   
        
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, 'Username OR password does not exist.')
    
    context = {'page':page}
    return render(request, "mainapp/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def registerUser(request):
    form = UserCreationForm
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "There was an error creating your account.")
    
    return render(request, 'mainapp/login_register.html', {'form':form})


def index(request):
    posts = adminPost.objects.all()
    topics = topicTheme.objects.all()
    users = User.objects.all()
    latest_post = adminPost.objects.latest("created_at")
    context = {'posts': posts,
               'topics': topics,
               'latest_post': latest_post,
               'users': users,
            
               }
    return render(request, "mainapp/index.html", context)



def userFeed(request):
    posts = adminPost.objects.all()
    topics = topicTheme.objects.all()
    latest_post = adminPost.objects.latest("created_at")
    replies = latest_post.allreply_set.all().order_by("-created_on") if latest_post else []
    repliers = latest_post.repliers.all() if latest_post else []
    
    context = {'posts': posts,
               'topics': topics,
               'latest_post': latest_post,
               "replies": replies,
               'repliers': repliers,
               }
    return render(request, "mainapp/userfeed.html", context)



@login_required(login_url='login')
def feed(request):
    q = request.GET.get("q")
    posts = adminPost.objects.all()
    topics = topicTheme.objects.all()
    latest_post = adminPost.objects.latest("created_at") if adminPost.objects.exists() else None
    replies = latest_post.allreply_set.all().order_by("-created_on") if latest_post else []
    repliers = latest_post.repliers.all() if latest_post else []
    
    message_activity = allReply.objects.all
    
    reply_count = replies.count()
    
    if request.method == "POST" and latest_post:
        reply = allReply.objects.create(
            user = request.user,
            post = latest_post,
            body = request.POST.get("body"),
        )
        
        latest_post.repliers.add(request.user)
        return redirect('feed')
    
    
    context = {'posts':posts,
               'topics': topics,
               'latest_post': latest_post,
                "replies": replies,
               'repliers': repliers,
               'post': post,
               'message_activity': message_activity,
                'reply_count': reply_count,
               }
    return render(request, "mainapp/feed.html", context)




@login_required(login_url='login')
def post(request,pk):
    post = get_object_or_404(adminPost, id=pk)
    posts = adminPost.objects.all()
    topics = topicTheme.objects.all()
    other_posts = adminPost.objects.exclude(id=pk)
    home_posts = adminPost.objects.exclude(id=pk)
    dis_posts = adminPost.objects.exclude(id=pk)
    replies = post.allreply_set.all().order_by("-created_on")
    repliers = post.repliers.all()
    
    message_activity = allReply.objects.all
    reply_count = replies.count()
    
    if request.method == "POST":
        reply = allReply.objects.create(
            user = request.user,
            post = post,
            body = request.POST.get("body"),
        )
        
        post.repliers.add(request.user)
        return redirect('post', pk=post.id)
    
    context = {"post":post,
               "other_posts": other_posts,
               "home_posts": home_posts,
               "dis_posts": dis_posts,
               'topics':topics,
               "posts":posts,
               "replies": replies,
               'repliers': repliers,
               'message_activity': message_activity,
                'reply_count': reply_count,
               
    }
    return render(request, "mainapp/post.html", context)


@login_required(login_url='login')
def deleteReply(request, pk):
    reply = allReply.objects.get(id=pk)
    
    if request.user != reply.user:
        return HttpResponse("You cannot perform this action.")
        
    if request.method == "POST":
        reply.delete()
        return redirect('feed')
    return render(request, 'mainapp/delete.html', {'obj': reply})
    
    



def feedback(request):
    return render(request, "feedback.html")



@login_required(login_url='login')
def accountPage(request, username):
    user = get_object_or_404(User, username=username)

    user_replies = allReply.objects.filter(user=user)
    topics = dkTopic.objects.all()
    themes = topicTheme.objects.all()
    user_replies_count = user_replies.count()
    
    paginator = Paginator(user_replies, 5)  # Show 10 replies per page
    page_number = request.GET.get('page')
    user_replies = paginator.get_page(page_number)
    
    context = {'user': user,
               
               'user_replies': user_replies,
               'topics': topics,
               'themes': themes,
               'user_replies_count': user_replies_count,
               }
    
    
    return render(request, "mainapp/account_page.html", context)







@login_required(login_url='login')
def allDiscussions(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    posts = adminPost.objects.filter(
        
        Q(topicTheme__name__icontains=q) |
        Q(name__icontains=q) |
        Q(dkTopic__name__icontains=q) |
        Q(created__icontains=q)
        
        
        )
    
    post_count = posts.count()
    
    
    topics = dkTopic.objects.all()
    themes = topicTheme.objects.all()
    
    context = {'posts': posts, 'topics': topics, 'themes': themes, "post_count":post_count}
    
    return render(request, 'mainapp/alldiscussions.html', context)


def latest_post(request):
    try:
        latest_post = adminPost.objects.latest("created_at")
    except adminPost.DoesNotExist:
        latest_post = None
        
    context = {"latest_post": latest_post,}
    return render(request, 'mainapp/feed.html', 'maiapp/index.html', context)






        
@csrf_exempt     
def fact_check(request):
    api_key = os.getenv("API_KEY")
    if not api_key:
        return JsonResponse({"error": "API key not found"}, status=500)
      
    try:  
        
        user_query = request.POST.get("query")
        if not user_query:
            return JsonResponse({"error": "No query provided"}, status=400)
          
        data = {
            "messages": [
                {"role": "system", "content": "You are an unbiased fact-checking assistant, providing factual information with data, and links to sources."},
                {"role": "user", "content": user_query}
            ],
            "model": "grok-beta",
            "stream": False,
            "temperature": 0
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        response = requests.post("https://api.x.ai/v1/chat/completions", json=data, headers=headers)
        print(response.content)
        if response.status_code == 200:
            assistant_message = response.json()["choices"][0]["message"]["content"]
            return JsonResponse(response.json())
            
        else:
            try:
                error_details = response.json()
            except ValueError:
                error_details = {"message": "Invalid Json response from Grok API"}
                
            return JsonResponse({"error": f"Grok API error: {response.json()}"}, status = response.status_code)  
            
                    
    except Exception as e:
            return JsonResponse({"error": F"An error occurred: {str(e)}"}, status=500)
        
             

@login_required(login_url="login")
def save_note(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            topic_id = data.get('noteTopic')
            theme_id = data.get('noteTheme')
            content = data.get('noteContent')

            if not topic_id or not theme_id or not content:
                return JsonResponse({'status': 'error', 'message': 'Topic, theme, or content is missing.'}, status=400)

            # Fetch today's topic, theme, and post
            note_topic = get_object_or_404(dkTopic, id=topic_id)
            note_theme = get_object_or_404(topicTheme, id=theme_id)
            related_post = adminPost.objects.filter(dkTopic=note_topic).order_by('-created_at').first()

            if not related_post:
                return JsonResponse({'status': 'error', 'message': 'No admin post found for today\'s topic and theme.'}, status=404)

            # Save the note associated with the current user, topic, theme, and post
            Notes.objects.create(
                user=request.user,
                noteTopic=note_topic,
                noteTheme=note_theme,
                relatedAdminPost=related_post,
                noteContent=content,
                noteTopic_id = topic_id,
            )

            return JsonResponse({'status': 'success', 'message': 'Note saved successfully.'})

        except Exception as e:
            logging.error(f"Error in save_note: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Internal server error.'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@login_required
def get_notes(request, topic_id):
    notes = Notes.objects.filter(noteTopic_id=topic_id, user=request.user).select_related('relatedAdminPost')
    notes_data = [
        {
            'id': note.id,
            'content': note.noteContent,
            
        }
        for note in notes
    ]
    return JsonResponse({'status': 'success', 'notes': notes_data})

    
    
@login_required
def delete_note(request, note_id):
    if request.method == "DELETE":
        note = get_object_or_404(Notes, id=note_id, user= request.user)
        note.delete()
        return JsonResponse({'status': 'success', 'message': 'Note Deleted.'})
    return JsonResponse({'status': 'error', 'message': 'Failed to Delete Note.'})



DOMAIN = "http://localhost:8000"  # Move this to your settings file or environment variable for production.
stripe.api_key = os.environ['STRIPE_SECRET_KEY']


def subscribe(request) -> HttpResponse:
    return render(request, 'mainapp/subscribe.html')


def cancel(request) -> HttpResponse:
    return render(request, 'mainapp/cancel.html')


def success(request) -> HttpResponse:

    print(f'{request.session = }')

    stripe_checkout_session_id = request.GET['session_id']

    return render(request, 'mainapp/success.html')


def create_checkout_session(request) -> HttpResponse:
    price_lookup_key = request.POST['price_lookup_key']
    try:
        prices = stripe.Price.list(lookup_keys=[price_lookup_key], expand=['data.product'])
        price_item = prices.data[0]

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {'price': price_item.id, 'quantity': 1},
                # You could add differently priced services here, e.g., standard, business, first-class.
            ],
            mode='subscription',
            success_url=DOMAIN + reverse('success') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=DOMAIN + reverse('cancel')
        )

        # We connect the checkout session to the user who initiated the checkout.
        models.CheckoutSessionRecord.objects.create(
            user=request.user,
            stripe_checkout_session_id=checkout_session.id,
            stripe_price_id=price_item.id,
        )

        return redirect(
            checkout_session.url,  # Either the success or cancel url.
            code=303
        )
    except Exception as e:
        print(e)
        return HttpResponse("Server error", status=500)


def direct_to_customer_portal(request) -> HttpResponse:
    """
    Creates a customer portal for the user to manage their subscription.
    """
    checkout_record = models.CheckoutSessionRecord.objects.filter(
        user=request.user
    ).last()  # For demo purposes, we get the last checkout session record the user created.

    checkout_session = stripe.checkout.Session.retrieve(checkout_record.stripe_checkout_session_id)

    portal_session = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=DOMAIN + reverse('subscribe')  # Send the user here from the portal.
    )
    return redirect(portal_session.url, code=303)


@csrf_exempt
def collect_stripe_webhook(request) -> JsonResponse:
    """
    Stripe sends webhook events to this endpoint.
    We verify the webhook signature and updates the database record.
    """
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    signature = request.META["HTTP_STRIPE_SIGNATURE"]
    payload = request.body

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=signature, secret=webhook_secret
        )
    except ValueError as e:  # Invalid payload.
        raise ValueError(e)
    except stripe.error.SignatureVerificationError as e:  # Invalid signature
        raise stripe.error.SignatureVerificationError(e)

    _update_record(event)

    return JsonResponse({'status': 'success'})


def _update_record(webhook_event) -> None:
    """
    We update our database record based on the webhook event.

    Use these events to update your database records.
    You could extend this to send emails, update user records, set up different access levels, etc.
    """
    data_object = webhook_event['data']['object']
    event_type = webhook_event['type']

    if event_type == 'checkout.session.completed':
        checkout_record = models.CheckoutSessionRecord.objects.get(
            stripe_checkout_session_id=data_object['id']
        )
        checkout_record.stripe_customer_id = data_object['customer']
        checkout_record.has_access = True
        checkout_record.save()
        print('🔔 Payment succeeded!')
    elif event_type == 'customer.subscription.created':
        print('🎟️ Subscription created')
    elif event_type == 'customer.subscription.updated':
        print('✍️ Subscription updated')
    elif event_type == 'customer.subscription.deleted':
        checkout_record = models.CheckoutSessionRecord.objects.get(
            stripe_customer_id=data_object['customer']
        )
        checkout_record.has_access = False
        checkout_record.save()
        print('✋ Subscription canceled: %s', data_object.id)
        

@login_required(login_url='login')
def user_feed(request):
    q = request.GET.get("q")
    posts = adminPost.objects.all()
    topics = topicTheme.objects.all()
    latest_post = adminPost.objects.latest("created_at") if adminPost.objects.exists() else None
    replies = latest_post.allreply_set.all().order_by("-created_on") if latest_post else []
    repliers = latest_post.repliers.all() if latest_post else []
    
    message_activity = allReply.objects.all
    
    reply_count = replies.count()
    
    if request.method == "POST" and latest_post:
        reply = allReply.objects.create(
            user = request.user,
            post = latest_post,
            body = request.POST.get("body"),
        )
        
        latest_post.repliers.add(request.user)
        return redirect('feed')
    
    
    context = {'posts':posts,
               'topics': topics,
               'latest_post': latest_post,
                "replies": replies,
               'repliers': repliers,
               'post': post,
               'message_activity': message_activity,
                'reply_count': reply_count,
               }
    
    return render(request, 'mainapp/user_feed.html', context)

def privacy_policy(request):
    return render(request, 'mainapp/privacypolicy.html')


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account', username=user.username)
    return render (request, 'mainapp/update-user.html', {'form': form})