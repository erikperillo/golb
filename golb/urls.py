"""golb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r"^blog/", include("blog.urls"))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
import blog.views

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^$", blog.views.index, name="index"),
    url(r"^index/$", blog.views.index, name="index"),
    url(r"^blog/post/(?P<slug>[^\.]+).html",
        blog.views.view_post,
        name="view_blog_post"),
    url(r"^user/(?P<slug>[^\.]+)",
        blog.views.view_user,
        name="view_blog_user"),
    url(r"^blog/category/(?P<slug>[^\.]+).html",
        blog.views.view_category,
        name="view_blog_category"),
    url(r"^login/$", blog.views.user_login, name="login"),
    url(r"^logout/$", blog.views.user_logout, name="logout"),
    url(r"^new_post/$", blog.views.new_post, name="new_post"),
    url(r"^del_post/(?P<id>\d+)/$", blog.views.del_post, name="del_post"),
    url(r"^edit_post/(?P<id>\d+)/$", blog.views.edit_post, name="edit_post"),
]
