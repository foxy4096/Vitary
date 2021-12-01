from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm
from apps.notification.utilities import notify


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, "Account Created Successfully!, Please Complete Your Profile!")
            login(request, user)
            return redirect('profile')
    form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == "POST":
        uform = UserForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST, request.FILES,
                            instance=request.user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "Profile Edited Successfully!")
            return redirect('profile')
    else:
        uform = UserForm(instance=request.user)
        pform = ProfileForm(instance=request.user.profile)
        return render(request, 'accounts/profile.html', {'uform': uform, 'pform': pform})


def profile_view(request, username):
    usr = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile_view.html', {'usr': usr})


@login_required
def follow(request):
    if request.method == "POST":
        usr = get_object_or_404(User, username=request.POST['username'])
        if usr.profile in request.user.profile.follows.all():
            messages.error(request, "Already Followed!")
            return redirect('profile_view', username=usr.username)
        else:
            request.user.profile.follows.add(usr.profile)
            messages.success(request, "Followed Successfully!")
            notify(message=f"{request.user.username.title()} Followed You",
                   by_user=request.user.profile, to_user=usr.profile, notification_type="follow", link=reverse_lazy('profile_view', kwargs={'username': request.user.username}))
            return redirect('profile_view', username=usr.username)
    else:
        return redirect('home')


@login_required
def unfollow(request):
    if request.method == "POST":
        usr = get_object_or_404(User, username=request.POST['username'])
        if usr.profile in request.user.profile.follows.all():
            request.user.profile.follows.remove(usr.profile)
            messages.success(request, "Unfollowed Successfully!")
            return redirect('profile_view', username=usr.username)
        else:
            messages.error(request, "Already Unfollowed!")
            return redirect('profile_view', username=usr.username)
    else:
        return redirect('home')


def following(request):
    return render(request, 'accounts/following.html')


def followers(request):
    return render(request, 'accounts/followers.html')
