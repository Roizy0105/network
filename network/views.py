from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from django.core.paginator import Paginator
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import User, Posts


def index(request):
    post_list = Posts.objects.order_by("-created_at").all()
    paginator = Paginator(post_list, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {'page_obj': page_obj})


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


@csrf_exempt
def new_post(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    # Get contents of email
    content = data.get("content", "")

    post = Posts(user_id=User.objects.get(id=request.user.id), content=content)
    post.save()

    return JsonResponse({"message": "Post Added"}, status=201)


def posts(request):
    following = User.objects.filter(following=request.user.id)
    post_list = []

    for id in following:
        post = Posts.objects.filter(user_id = id.id)
        for item in post:
            post_list.insert(0, item)

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/posts.html", {'page_obj': page_obj})


def profile(request, userid):

    user = User.objects.get(id=userid)

    post_list = Posts.objects.filter(user_id=user).order_by("-created_at")
    paginator = Paginator(post_list, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html",{
        "user": user,
        "following": len(user.following.all()),
        "followers": len(user.followers.all()),
        "posts": post_list
    })

@csrf_exempt
def editing_post(request):
    if request.method == "POST":
        # Check recipient emails
        data = json.loads(request.body)
        # Get contents of email
        id = data.get("id", "")
        post = Posts.objects.get(id=id)

        return JsonResponse({
            "post_id": post.id,
            "content": post.content
        }, status=201)

@csrf_exempt
def edit_post(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)


    # Get contents of email
    content = data.get("content", "")
    id = data.get("id", "")

    edited_post = Posts.objects.filter(id=id).update(content=content)

    return JsonResponse({"message": "Post Edited"}, status=201)

def follow(request, user_id):
    # if the user who is logged in is visiting his/her own page then no button should appeare
    if request.user.id == user_id:
        return JsonResponse({"message": "remove button"}, status=201)

    user = User.objects.filter(id=user_id)
    list = user[0].following.all()
    # itarate through the people that are following this user
    for i in list:
        # if the current user is found in the list of users folling the user whos page where on then allow to unfollow
        if i.id == request.user.id:
            return JsonResponse({"message": "Unfollow"}, status=201)
    # else allow to follow
    return JsonResponse({"message": "follow"}, status=201)

@csrf_exempt
def follow_button(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)


    data = json.loads(request.body)

    button = data.get("button", "")
    user_id = data.get("user_id", "")
    # get thease users from the database
    loggedin_user = User.objects.get(id=request.user.id)
    user = User.objects.get(id=user_id)

    # if the button the user clicked on is to follow the user then
    if button == "Follow":
        # update the users followers
        user.followers.add(loggedin_user)
        user.save()
        # updated the logged in user followings
        loggedin_user.following.add(user)
        loggedin_user.save()
        return JsonResponse({"message": "added"}, status=201)

    # if the button the user click in is to unfollow the user
    if button == "Unfollow":
        # update the users followers
        user.followers.remove(loggedin_user)
        user.save()
        # updated the logged in user followings
        loggedin_user.following.remove(user)
        loggedin_user.save()
        return JsonResponse({"message": "removed"}, status=201)

    return JsonResponse({"message": "nothing"}, status=201)

@csrf_exempt
def like(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)


    data = json.loads(request.body)

    user_id = data.get("user_id", "")
    post_id = data.get("post_id", "")


    post = Posts.objects.get(id=post_id)
    user = User.objects.get(id=user_id)

    if user in post.likes.all():
        post.likes.remove(user)
        post.save()
        return JsonResponse({"message": "unlike"}, status=201)

    post.likes.add(user)
    post.save()
    return JsonResponse({"message": "liked"}, status=201)
