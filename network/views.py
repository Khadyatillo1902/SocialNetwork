from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
import json



from .models import User, Post, Follow, Comment

def index(request):
    allPosts = Post.objects.all().order_by('id').reverse()

    
    
    #creating a pagination
    
    paginator = Paginator(allPosts, 3)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)



    return render(request, "network/index.html", {
        "allPosts": allPosts,
        "posts_of_the_page": posts_of_the_page,
    })

def edit_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id, user=request.user)
    except Post.DoesNotExist:
        return JsonResponse({'error':'Post not found'}, status=400)
    
    data = json.loads(request.body)
    new_content = data.get('content', "")
    
    if new_content.strip() == '':
        return JsonResponse({'error':'Content cannot be empty'}, status=400)
    
    post.content = new_content
    
    post.save()

    return JsonResponse({'message':'Post updated successfully', 'new_content': new_content})

def newPost(request):
    if request.method == "POST":
        content = request.POST['content-body']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    allPosts = Post.objects.filter(user=user).order_by('id').reverse()

    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_follower=user)

    isFollowing = False

    try:
        checkFollow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(checkFollow) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False

    #creating a pagination
    
    paginator = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "allPosts": allPosts,
        "posts_of_the_page": posts_of_the_page,
        "username": user.username,
        'following': following,
        'followers': followers,
        'isFollowing': isFollowing,
        'user_profile': user
    })

def follow(request, user_id):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    f = Follow(user=currentUser, user_follower=userfollowData)
    f.save()
    user_id = userfollowData.id 
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def unfollow(request, user_id):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    f = Follow.objects.get(user=currentUser, user_follower=userfollowData)
    f.delete()
    user_id = userfollowData.id 
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    followingPeople = Follow.objects.filter(user=currentUser)
    allPosts = Post.objects.all().order_by('-id').reverse()

    followingPosts = []

    for post in allPosts:
        for person in followingPeople:
            if person.user_follower == post.user:
                followingPosts.append(post)
    #pagination
    paginator = Paginator(followingPosts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number) 

    return render(request, 'network/following.html', {
        "posts_of_the_page": posts_of_the_page
    })

@login_required
@require_http_methods(["PUT"])
def like_post(request, post_id):
    
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    like_count = post.total_likes()

    return JsonResponse({
        'like_count': like_count,
        'liked': liked
    })


def comment(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(pk=post_id)
            content = json.loads(request.body).get('content', '')
            
            if not content:
                return JsonResponse({"error": "Comment content cannot be empty"}, status=400)
            
            comment = Comment(user=request.user, post=post, content=content)
            comment.save()

            return JsonResponse({
                'user': request.user.username,
                'content': comment.content,
                'date': comment.date.strftime("%Y-%m-%d %H:%M:%S")
            })
        except Post.DoesNotExist:
            return JsonResponse({'error':'Post not found'}, status=404)
    else:
        return JsonResponse({'error':'Invalid request'}, status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
