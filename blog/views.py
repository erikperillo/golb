from blog.models import Post, UserProfile, Category
from blog.forms import LoginForm, PostForm

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify
from django.contrib.auth import logout

LIMIT_RECENT_POSTS = 5

def index(request):
    return render(request, "index.html", context={
        "categories": Category.objects.all(),
        "posts": Post.objects.all()[:LIMIT_RECENT_POSTS],
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

@login_required
def new_post(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == "POST":
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        form = PostForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            author = request.user.userprofile
            post = Post(title=data["title"], body=data["body"],
                category=data["category"], author=author)
            post.save()

        return view_post(request, post.slug)
    else:
        form = PostForm()
        return render(request, "new_post.html", {"form": form})

@login_required
def del_post(request, id):
    if request.method == "POST":
        try:
            post = Post.objects.filter(pk=id).get()
        except:
            return render(request, "error.html",
                {"message": "Error getting post."})

        author = request.user.userprofile
        if author.pk == post.author.pk:
            post.delete()
            return render(request, "message.html", {"message": "Post deleted."})
        else:
            return render(request, "error.html",
                {"message": "Not authorized to do that."})
    else:
        return HttpResponseRedirect("/index")

@ensure_csrf_cookie
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data["user_name"],
                password=form.cleaned_data["password"])

            #if we have a User object, the details are correct.
            #if None (Python"s way of representing the absence of a value),
            #no user with matching credentials was found.
            if user:
                #is the account active? it could have been disabled.
                if user.is_active:
                    #if the account is valid and active, we can log the user in.
                    #we'll send the user back to the homepage.
                    login(request, user)
                    return HttpResponseRedirect("/index")
                else:
                    #an inactive account was used - no logging in!
                    return render(request, "error.html",
                        {"message": "Your account is inactive."})
            else:
                #bad login details were provided. So we can"t log the user in.
                return render(request, "error.html",
                    {"message": "Invalid login details."})
        else:
            return HttpResponse("Invalid form.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect("/index/")
