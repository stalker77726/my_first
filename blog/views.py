import json
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})
def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.info(request, 'You are now logged in')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Invalid login details')
            return render(request, 'blog/login.html', {})
    else:
        return render(request, 'blog/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You are now logged out')
    return HttpResponseRedirect(reverse('post_list'))
def register(request):
    print("Im in register")
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm()

        if user_form.is_valid() and user_form.cleaned_data['password'] == user_form.cleaned_data['password_confirmation']:
            print("OK! REGISTER")
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.balance = 5
            profile.save()

            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'],
                                   )

            login(request, new_user)
            print("OK! LOGIN")
            return HttpResponseRedirect('/')
        elif user_form.data['password'] != user_form.data['password_confirmation']:
            user_form.add_error('password_confirmation', 'The passwords do not match')
            print("Password do not match")
        else:
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                  'blog/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})