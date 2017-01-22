from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from uuid import uuid1

class Post(models.Model):
    title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    body = models.TextField()
    date_created = models.DateField(db_index=True, auto_now_add=True)
    category = models.ForeignKey("blog.Category")
    author = models.ForeignKey("blog.UserProfile")

    def __str__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ("view_blog_post", None, {"slug": self.slug})

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(**kwargs)

class UserProfile(models.Model):
    #this line is required. links User to a UserProfile model instance
    user = models.OneToOneField(User)
    slug = models.SlugField(max_length=150, unique=True, default=uuid1)
    website = models.URLField(blank=True)

    def __str__(self):
        #return self.user.get_username()
        return self.user.username

    @permalink
    def get_absolute_url(self):
        return ("view_blog_user", None, {"slug": self.slug})

    def save(self, **kwargs):
        #self.slug = slugify(self.user.get_username())
        super(UserProfile, self).save(**kwargs)

class Category(models.Model):
    title = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=128, db_index=True)

    def __str__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ("view_blog_category", None, {"slug": self.slug})

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(**kwargs)
