from blog.models import Post, UserProfile, Category
from blog.forms import LoginForm, PostForm
try:
    from blog.globals import blog_title
except ImportError:
    blog_title = "Welcome to Bolg"
try:
    from blog.globals import initial_category
except ImportError:
    initial_category = "Random"

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify
from django.contrib.auth import logout

LIMIT_RECENT_POSTS = 8

def _render(request, template, context, *args):
    context.update({"blog_title": blog_title})
    return render(request, template, context, *args)

def index(request):
    if len(Category.objects.all()) < 1:
        Category(title=initial_category).save()
    return _render(request, "index.html", context={
        "categories": Category.objects.all().order_by("title"),
        "posts": Post.objects.all().\
            order_by("-date_created")[:LIMIT_RECENT_POSTS],
        })

def view_post(request, slug):
    return _render(request, "view_post.html", context={
        "post": get_object_or_404(Post, slug=slug)
        })

def view_user(request, slug):
    user_profile = get_object_or_404(UserProfile, slug=slug)
    return _render(request, "view_user.html", context={
        "user": user_profile.user,
        "posts": Post.objects.filter(author=user_profile).\
            order_by("-date_created")[:LIMIT_RECENT_POSTS]
        })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return _render(request, "view_category.html", context={
        "category": category,
        "posts": Post.objects.filter(category=category).\
            order_by("-date_created")[:LIMIT_RECENT_POSTS]
        })

@login_required
#@ensure_csrf_cookie
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
            return _render(request, "error.html",
                {"message": "Invalid form."})
    else:
        form = PostForm()
        return _render(request, "new_post.html", {"form": form})

@login_required
def del_post(request, id):
    if request.method == "POST":
        try:
            post = Post.objects.filter(pk=id).get()
        except:
            return _render(request, "error.html",
                {"message": "Error getting post."})

        author = request.user.userprofile
        if author.pk == post.author.pk:
            post.delete()
            return _render(request, "message.html", {"message": "Post deleted."})
        else:
            return _render(request, "error.html",
                {"message": "Not authorized to do that."})
    else:
        return HttpResponseRedirect("/index")

@login_required
#@ensure_csrf_cookie
def edit_post(request, id):
    try:
        post = Post.objects.filter(pk=id).get()
    except:
        return _render(request, "error.html",
            {"message": "Error getting post."})

    author = request.user.userprofile
    if author.pk != post.author.pk:
        return _render(request, "error.html",
            {"message": "Not authorized to do that."})

    if request.method == "POST":
        post.delete()

        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_post = Post(title=data["title"], body=data["body"],
                category=data["category"], author=author)
            new_post.save()
            return view_post(request, new_post.slug)
        else:
            post.save()
            return _render(request, "error.html", {"message": "Invalid form."})
    else:
        data = {
            "title": post.title,
            "category": post.category,
            "body": post.body,
        }
        form = PostForm(initial=data)
        print("form:", form, "data:", data)
        return _render(request, "edit_post.html", {"form": form, "id": id})

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
                    return _render(request, "error.html",
                        {"message": "Your account is inactive."})
            else:
                #bad login details were provided. So we can"t log the user in.
                return _render(request, "error.html",
                    {"message": "Invalid login details."})
        else:
            return HttpResponse("Invalid form.")
    else:
        form = LoginForm()

    return _render(request, "login.html", {"form": form})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect("/index/")
