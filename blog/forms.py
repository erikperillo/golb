from django import forms
from blog.models import Post

class LoginForm(forms.Form):
    user_name = forms.CharField(label="Username", widget=forms.TextInput())
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs={"class": "col-xs-12", "rows": 20, "style": "font-size: 80%;"}))
    class Meta:
        model = Post
        fields = ("title", "category", "body")
