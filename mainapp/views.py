from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from .models import adminPost, dkTopic, allReply, topicTheme
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



@login_required(login_url='login')
def feed(request):
    q = request.GET.get("q")
    posts = adminPost.objects.all()
    topics = topicTheme.objects.all()
    latest_post = adminPost.objects.latest("created_at") if adminPost.objects.exists() else None
    replies = latest_post.allreply_set.all().order_by("-created_on") if latest_post else []
    repliers = latest_post.repliers.all() if latest_post else []
    
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

def account(request):
    return render(request, "account_settings.html")


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
        
             
