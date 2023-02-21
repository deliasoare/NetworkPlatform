import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import render_to_string
from .models import User, Post, Follow, Like
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def index(request, page=1):
    posts = Post.objects.all().order_by('-date')
    p = Paginator(posts, per_page=10)
    page_obj = p.get_page(page)
    next = 0
    previous = 0
    if page_obj.has_next():
        next = page_obj.next_page_number()

    if page_obj.has_previous():
        previous = page_obj.previous_page_number

    return render(request, "network/index.html", {
        "following_page": False,
        'posts':page_obj,
        "next":next,
        "previous":previous,
        "page":page,
        "behind":page-1,
        "ahead":page+1,
        "target":"index",
        "liked_by":liked_by
    })

@csrf_exempt
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index", args=[1]))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index", args=[1]))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        if username != username.lower():
            error="Username must be in lowercase."
            return render(request, "network/register.html", {
                "message": error
            })
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match.",
            })
        if not username or not password or not email or not confirmation:
            return render(request, "network/register.html", {
                "message": "You must fill out all fields!"
            })
            
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index", args=[1]))
    else:
        return render(request, "network/register.html")
        

def new_post(request):
    if request.method == "GET":
        return render(request, "network/new_post.html")
    else:
        text = request.POST.get('body')
        post = Post()
        post.body = text 
        post.user = request.user
        post.save()
        return HttpResponseRedirect(reverse("index", args=[1]))

def profile(request, username, page=1):
    if request.method == "GET":
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse("Not Good")

        posts = Post.objects.filter(user=user).order_by('-date')

        follows = Follow.objects.filter(user=user)

        followed = False

        for follow in follows:
            if follow.follower == request.user:
                followed = True 

        p = Paginator(posts, 10)

        page_obj = p.get_page(page)
        previous = 0
        next = 0
        if page_obj.has_previous():
            previous = page_obj.previous_page_number()
        if page_obj.has_next():
            next = page_obj.next_page_number()

        
        followings = []
        follows = Follow.objects.filter(follower=user)

        for follow in follows:
            followings.append(follow.user)

        follows = Follow.objects.filter(user=user)

        followers = []

        for follow in follows:
            followers.append(follow.follower)

            
        return render(request, "network/profile.html", {
            "profile": user,
            "posts":page_obj,
            "followed":followed,
            "follow_count":len(followers),
            "following_count":len(followings),
            "previous":previous,
            "next":next,
            "page":page,
            "behind":page-1,
            "ahead":page+1,
            "followings":followings,
            "followers":followers

        })

def follow(request, username):
    user = User.objects.get(username=username)
    follow = Follow()
    follow.follower = request.user
    follow.user = user
    follow.save()
    return HttpResponseRedirect(reverse("profile", args=[username, 1]))

def unfollow(request, username):
    user = User.objects.get(username=username)
    follow = Follow.objects.get(user=user, follower=request.user)
    follow.delete()
    return HttpResponseRedirect(reverse("profile", args=[username, 1]))

def get_date(post):
    return post.date

def following(request,  page=1):
    user = request.user
    followings = Follow.objects.filter(follower=user)
    posts =[]
    for following in followings:
        posts += Post.objects.filter(user=following.user)
    posts.sort(reverse=True, key=get_date)

    p = Paginator(posts, 10)

    page_obj = p.get_page(page)
    previous = 0
    next = 0
    if page_obj.has_previous():
        previous = page_obj.previous_page_number()
    if page_obj.has_next():
        next = page_obj.next_page_number()
    return render(request, "network/index.html", {
        "posts":page_obj, 
        "following_page": True,
        "previous":previous,
        "next":next,
        "page":page,
        "behind":page-1,
        "ahead":page+1,
        "target":"following"
    })

@csrf_exempt
def post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error":"Post not found."}, status = 404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data =json.loads(request.body)
        if data.get("content") is not None:
            post.body = data["content"]
        if data.get("likes") is not None:
            post.likes = data["likes"]
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({"error: GET or PUT request required."}, status=404)

@csrf_exempt
def like(request):
    if request.method != "POST":
        return JsonResponse({"error" : "POST request required."}, status = 400)

    data = json.loads(request.body)

    user = User.objects.get(username=data.get("liker"))

    post_id = data.get("post_id")

    post = Post.objects.get(pk=post_id)

    try:    
        like = Like.objects.get(user=user, post=post)
    except Like.DoesNotExist:
        like = Like()
        like.user = user
        like.post = post
        like.save()
        post.likers.add(user)
        post.save()
        return JsonResponse({"successfull" :"added"})
    
    like.delete()
    post.likers.remove(user)
    post.save()
    return JsonResponse({"successfull" : "removed"})

def liked_by(post, user):
    if (Like.objects.get(post=post, user=user)):
        return True 
    else:
        return False
    


    



