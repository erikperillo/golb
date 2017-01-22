from django.contrib import admin
from blog.models import Post, UserProfile, Category

class PostAdmin(admin.ModelAdmin):
    exclude = ["date_created"]
    prepopulated_fields = {"slug": ("title",)}

class UserProfileAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
