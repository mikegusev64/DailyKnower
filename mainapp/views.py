from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from .models import adminPost, dkTopic, allReply, topicTheme
from django.views.generic import ListView
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import os




# Create your views here.


def index(request):
    posts = adminPost.objects.all()
    topics = topicTheme.objects.all()
    context = {'posts': posts,
               'topics': topics,
               }
    return render(request, "mainapp/index.html", context)

def feed(request):
    q = request.GET.get("q")
    posts = adminPost.objects.all()
    topics = topicTheme.objects.all()
    latest_post = adminPost.objects.latest("created_at")
    context = {'posts':posts,
               'topics': topics,
               'latest_post': latest_post,
               }
    return render(request, "mainapp/feed.html", context)


def post(request,pk):
    post = get_object_or_404(adminPost, id=pk)
    topics = topicTheme.objects.all()
    other_posts = adminPost.objects.exclude(id=pk)
    home_posts = adminPost.objects.exclude(id=pk)
    dis_posts = adminPost.objects.exclude(id=pk)
    context = {"post":post,
               "other_posts": other_posts,
               "home_posts": home_posts,
               "dis_posts": dis_posts,
               'topics':topics,
               
    }
    return render(request, "mainapp/post.html", context)



def feedback(request):
    return render(request, "feedback.html")

def account(request):
    return render(request, "account_settings.html")

def deleteMessage(request, pk):
    reply = allReply.objects.get(id=pk)
    if request.method == "POST":
        reply.delete()
        return redirect('home')
    return render(request, 'mainapp/delete.html', {'obj': allReply})

def allDiscussions(request):
    posts = adminPost.objects.all()
    topics = dkTopic.objects.all()
    themes = topicTheme.objects.all()
    
    context = {'posts': posts, 'topics': topics, 'themes': themes}
    
    return render(request, 'mainapp/alldiscussions.html', context)

def latest_post(request):
    try:
        latest_post = adminPost.objects.latest("created_at")
    except adminPost.DoesNotExist:
        latest_post = None
        
    context = {"latest_post": latest_post,}
    return render(request, 'mainapp/feed.html', context)






        
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
            return JsonResponse({"error": F"An error ocurred: {str(e)}"}, status=500)
        
             
