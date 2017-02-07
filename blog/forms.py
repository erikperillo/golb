from django import forms
from blog.models import Post

class LoginForm(forms.Form):
    user_name = forms.CharField(label="Username", widget=forms.TextInput())
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "category", "body")
