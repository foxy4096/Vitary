from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from apps.core.utilities import paginate

from .forms import (
    UserForm,
    UserProfileForm,
    UserRegisterForm,
    UsernameForm,
    DateOfBirthForm,
    UserProfileAvatarForm,
)


def signup(request):
    """
    View for signup
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully")
            return redirect("edit_userprofile")
        else:
            if User.objects.filter(username=request.POST["username"]).exists():
                messages.add_message(
                    request,
                    40,
                    "Username already exists! \n Woops look like someone have already taken your identity",
                    extra_tags="danger",
                )
            elif request.POST["password1"] != request.POST["password2"]:
                messages.add_message(
                    request,
                    40,
                    "Passwords do not match \n Please don't rush.",
                    extra_tags="danger",
                )
            else:
                messages.add_message(
                    request,
                    40,
                    "Unknown Error Occured! \n It means that we are fu**** up",
                    extra_tags="danger",
                )
            return redirect("signup")
    else:
        form = UserRegisterForm()
        return render(request, "accounts/signup.html", {"form": form})


@login_required
def edit_userprofile(request):
    """
    View for editing userprofile
    """
    if request.method == "POST":
        uform = UserForm(request.POST, instance=request.user)
        pform = UserProfileForm(request.POST, instance=request.user.userprofile)
        aform = UserProfileAvatarForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        dform = DateOfBirthForm(request.POST, instance=request.user.userprofile)
        if (
            uform.is_valid()
            and pform.is_valid()
            and dform.is_valid()
            and aform.is_valid()
        ):
            uform.save()
            pform.save()
            dform.save()
            aform.save()
            messages.success(request, "UserProfile Edited Successfully! \n You look nice!")
            return redirect("edit_userprofile")
    else:
        uform = UserForm(instance=request.user)
        pform = UserProfileForm(instance=request.user.userprofile)
        aform = UserProfileAvatarForm(instance=request.user.userprofile)
        dform = DateOfBirthForm(instance=request.user.userprofile)
        return render(
            request,
            "accounts/edit_userprofile.html",
            {"uform": uform, "pform": pform, "dform": dform, "aform": aform},
        )


def user_detail(request, username):
    tuser = get_object_or_404(User, username__iexact=username)
    feeds = tuser.feeds.all()
    if request.user.is_authenticated and not request.user.userprofile.allow_nsfw:
        feeds = feeds.exclude(nsfw=True)
    return render(
        request,
        "accounts/user_detail.html",
        {"tuser": tuser, "feeds": paginate},
    )


def user_following(request, username):
    """
    View for getting the following users of a user
    """
    tuser = get_object_or_404(User, username=username)
    followings = paginate(request, tuser.userprofile.follows.all().order_by("-id"))
    return render(
        request, "accounts/following.html", {"tuser": tuser, "followings": followings}
    )


def user_followers(request, username):
    """
    View for getting the followers of a user
    """
    tuser = get_object_or_404(User, username=username)
    followers = paginate(request, tuser.userprofile.followed_by.all().order_by("-id"))
    return render(
        request, "accounts/followers.html", {"tuser": tuser, "followers": followers}
    )


@login_required
def advanced_settings(request):
    """
    View for advanced settings
    """
    return render(request, "accounts/advance.html")


@login_required
def delete_account(request):
    """
    View for deleting account
    """
    if request.method != "POST":
        return render(request, "accounts/delete_account.html")
    user = request.user
    logout(request)
    user.is_active = False
    messages.success(request, "Account Deleted Successfully!")
    return redirect("home")


@login_required
def change_username(request):
    """
    View for changing username
    """
    if request.method == "POST":
        form = UsernameForm(request.POST)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data["username"]
            user.save()
            messages.success(request, "Username Changed Successfully!")
            return redirect("edit_userprofile")

    else:
        form = UsernameForm(initial={"username": request.user.username})
    return render(request, "accounts/change_username.html", {"form": form})

