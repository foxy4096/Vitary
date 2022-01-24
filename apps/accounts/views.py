from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from .models import Profile
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
        pform = ProfileForm(instance=request.user.profile)
        return render(request, 'accounts/profile.html', {'uform': uform, 'pform': pform})


def profile_view(request, username):
    usr = get_object_or_404(User, username=username)
    vits = usr.vits.all()
    paginator = Paginator(vits, 5)
    page = request.GET.get('page')
    vits = paginator.get_page(page)
    return render(request, 'accounts/profile_view.html', {'usr': usr, 'vits': vits})


@login_required
def follow(request):
    usr = get_object_or_404(User, username=request.GET['username'])
    vit_id = request.GET.get('vit_id', '')
    if usr in request.user.profile.follows.all():
        messages.error(request, "Already Followed!")
        if vit_id == '':
            return redirect('profile_view', username=usr.username)
        else:
            return redirect('vit_detail', pk=vit_id)
    else:
        request.user.profile.follows.add(usr.profile)
        request.user.profile.following_count = request.user.profile.follows.count()
        usr.profile.follower_count = usr.profile.followed_by.count()
        request.user.profile.save()
        usr.profile.save()
        messages.success(request, "Followed Successfully!")
        notify(message=f"{request.user.username.title()} Followed You",
                by_user=request.user, to_user=usr, notification_type="follow", link=reverse_lazy('profile_view', kwargs={'username': request.user.username}))
        if vit_id == '':
            return redirect('profile_view', username=usr.username)
        else:
            return redirect('vit_detail', pk=vit_id)



@login_required
def unfollow(request):
    usr = get_object_or_404(User, username=request.GET['username'])
    vit_id = request.GET.get('vit_id', '')
    if not usr in request.user.profile.follows.all():
        request.user.profile.follows.remove(usr.profile)
        request.user.profile.following_count = request.user.profile.follows.count()
        usr.profile.follower_count = usr.profile.followed_by.count()
        request.user.profile.save()
        usr.profile.save()
        messages.success(request, "Unfollowed Successfully!")
        if vit_id == '':
            return redirect('profile_view', username=usr.username)
        else:
            return redirect('vit_detail', pk=vit_id)
    else:
        messages.error(request, "Already Unfollowed!")
        if vit_id == '':
            return redirect('profile_view', username=usr.username)
        else:
            return redirect('vit_detail', pk=vit_id)

@login_required
def following(request):
    usr = request.user
    followings = usr.profile.follows.all().order_by('-id')
    paginator = Paginator(followings, 5)
    page = request.GET.get('page')
    followings = paginator.get_page(page)
    return render(request, 'accounts/following.html', {'usr': usr, 'followings': followings})

@login_required
def followers(request):
    usr = request.user
    followers = usr.profile.followed_by.all().order_by('-id')
    paginator = Paginator(followers, 5)
    page = request.GET.get('page')
    followers = paginator.get_page(page)
    return render(request, 'accounts/followers.html', {'usr': usr, 'followers': followers})

def user_following(request, username):
    usr = get_object_or_404(User, username=username)
    followings = usr.profile.follows.all().order_by('-id')
    paginator = Paginator(followings, 5)
    page = request.GET.get('page')
    followings = paginator.get_page(page)
    if usr == request.user:
        return redirect('following')
        
    return render(request, 'accounts/following.html', {'usr': usr, 'followings': followings})


def user_followers(request, username):
    usr = get_object_or_404(User, username=username)
    followers = usr.profile.followed_by.all().order_by('-id')
    paginator = Paginator(followers, 5)
    page = request.GET.get('page')
    followers = paginator.get_page(page)
    if usr == request.user:
        return redirect('followers')
    return render(request, 'accounts/followers.html', {'usr': usr, 'followers': followers})


@login_required
def advanced_settings(request):
    return render(request, 'accounts/advance.html')