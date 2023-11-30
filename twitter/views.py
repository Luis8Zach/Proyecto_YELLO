from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic.base import View  # Agrega esta línea
from .models import Profile, Post, Relationship
from .forms import UserRegisterForm, PostForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse


# Resto del código...


@login_required
def home(request):
    posts = Post.objects.all()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    # Agrega esta línea para obtener la cantidad de likes de cada post
    post_likes = [post.Cantidad_likes() for post in posts]

    context = {'posts': posts, 'form': form, 'post_likes': post_likes}
    return render(request, 'twitter/newsfeed.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario
            profile = Profile(user=user)  # Crea un perfil relacionado con el usuario
            profile.save()  # Guarda el perfil
            login(request, user)  # Autentica al usuario
            messages.success(request, "¡Felicitaciones! Te has registrado con éxito.")
            return redirect('home')
        else:
            messages.error(request, "Error: Datos incorrectos. Por favor, inténtalo de nuevo.")
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'twitter/register.html', context)



def delete(request, post_id):
	post = Post.objects.get(id=post_id)
	post.delete()
	return redirect('home')




def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    return render(request, 'twitter/profile.html', {'user': user, 'posts': posts})

@login_required
def editar(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '¡Tus datos se han editado correctamente!')
            return redirect('home')
        else:
            messages.error(request, 'Error: Por favor, verifica los datos e inténtalo de nuevo.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'twitter/editar.html', context)

@login_required
def follow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user, to_user=to_user_id)
	rel.save()
	return redirect('home')

@login_required
def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.get(from_user=current_user.id, to_user=to_user_id)
	rel.delete()
	return redirect('home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    post.save()
    return redirect('home')

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.dislikes += 1
    post.save()
    return redirect('/newsfeed.htm/ + user.id')













