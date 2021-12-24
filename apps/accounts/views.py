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
from .forms import UserRegisterForm


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully')
                return redirect('profile')
        else:
            if User.objects.filter(username=request.POST['username']).exists():
                messages.add_message(request, 40, 'Username already exists', extra_tags='danger')
                return redirect('signup')
            elif request.POST['password1'] != request.POST['password2']:
                messages.add_message(request, 40, 'Passwords do not match', extra_tags='danger')
                return redirect('signup')
            else:
                messages.add_message(request, 40, 'Unknown Error Occured', extra_tags='danger')
                return redirect('signup')
    else:
        form = UserRegisterForm()
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
        pform = ProfileForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'uform': uform, 'pform': pform})


def profile_view(request, username):
    usr = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile_view.html', {'usr': usr})


@login_required
def follow(request):
    if request.method == "POST":
        usr = get_object_or_404(User, username=request.POST['username'])
        if usr in request.user.profile.follows.all():
            messages.error(request, "Already Followed!")
            return redirect('profile_view', username=usr.username)
        else:
            request.user.profile.follows.add(usr.profile)
            messages.success(request, "Followed Successfully!")
            notify(message=f"{request.user.username.title()} Followed You",
                   by_user=request.user, to_user=usr, notification_type="follow", link=reverse_lazy('profile_view', kwargs={'username': request.user.username}))
            return redirect('profile_view', username=usr.username)
    else:
        return redirect('home')


@login_required
def unfollow(request):
    if request.method == "POST":
        usr = get_object_or_404(User, username=request.POST['username'])
        if not usr in request.user.profile.follows.all():
            request.user.profile.follows.remove(usr.profile)
            messages.success(request, "Unfollowed Successfully!")
            return redirect('profile_view', username=usr.username)
        else:
            messages.error(request, "Already Unfollowed!")
            return redirect('profile_view', username=usr.username)
    else:
        return redirect('home')

@login_required
def following(request):
    usr = request.user
    return render(request, 'accounts/following.html', {'usr': usr})

@login_required
def followers(request):
    usr = request.user
    return render(request, 'accounts/followers.html', {'usr': usr})

def user_following(request, username):
    usr = get_object_or_404(User, username=username)
    if usr == request.user:
        return redirect('following')
    return render(request, 'accounts/following.html', {'usr': usr})


def user_followers(request, username):
    usr = get_object_or_404(User, username=username)
    if usr == request.user:
        return redirect('followers')
    return render(request, 'accounts/followers.html', {'usr': usr})