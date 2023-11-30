from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Profile
from django.db import models
from django.contrib.auth.models import User
class UserRegisterForm(UserCreationForm):

	class Meta:
		model = User
		fields = ['first_name', 'username', 'email', 'password1', 'password2']



class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-100', 'id': 'contentsBox', 'rows': '3', 'placeholder': '¿Qué está pasando?'}))
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['text', 'image']

# Incluye el campo de imagen en los campos del formulario


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'username']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'bio']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.post}"

