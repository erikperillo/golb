from blog.models import Post, UserProfile, Category
from blog.forms import UserForm, UserProfileForm 

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout


LIMIT_RECENT_POSTS = 5

def index(request):
    if request.user.is_authenticated():
        usr = request.user
    else:
        usr = None

    return render(request, "index.html", context={
        "categories": Category.objects.all(),
        "posts": Post.objects.all()[:LIMIT_RECENT_POSTS],
        "user": usr,
        })

def view_post(request, slug):
    return render(request, "view_post.html", context={
        "post": get_object_or_404(Post, slug=slug)
        })

def view_user(request, slug):
    user = get_object_or_404(UserProfile, slug=slug)
    return render(request, "view_user.html", context={
        "user": user,
        "posts": Post.objects.filter(author=user)[:LIMIT_RECENT_POSTS]
        })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, "view_category.html", context={
        "category": category,
        "posts": Post.objects.filter(category=category)[:LIMIT_RECENT_POSTS]
        })

@ensure_csrf_cookie
def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == "POST":
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST["username"]
        password = request.POST["password"]

        # Use Django"s machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python"s way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We"ll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect("/index")
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can"t log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, "login.html", context={})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect("/index/")
