from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .forms import UserForm, ProfileForm, UserRegisterForm, UsernameForm


def signup(request):
    """
    View for signup
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Account created successfully")
            return redirect("profile")
        else:
            if User.objects.filter(username=request.POST["username"]).exists():
                messages.add_message(
                    request,
                    40,
                    "Username already exists! \n Woops look like someone have already taken your identity",
                    extra_tags="danger",
                )
                return redirect("signup")
            elif request.POST["password1"] != request.POST["password2"]:
                messages.add_message(
                    request,
                    40,
                    "Passwords do not match \n Please don't rush.",
                    extra_tags="danger",
                )
                return redirect("signup")
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
def profile_edit(request):
    """
    View for editing profile
    """
    if request.method == "POST":
        uform = UserForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "Profile Edited Successfully! \n You look nice!")
            return redirect("profile")
    else:
        uform = UserForm(instance=request.user)
        pform = ProfileForm(instance=request.user.profile)
        return render(
            request, "accounts/profile.html", {"uform": uform, "pform": pform}
        )


def profile(request, username):
    """
    View for profile
    """
    usr = get_object_or_404(User, username=username)
    vits = usr.vits.all()
    if request.user.is_authenticated and not request.user.profile.allow_nsfw:
        vits = vits.exclude(nsfw=True)
    paginator = Paginator(vits, 10)
    page = request.GET.get("page")
    vits = paginator.get_page(page)
    return render(
        request,
        "accounts/profile_view.html",
        {"usr": usr, "vits": vits, "onProfile": True},
    )


@login_required
def following(request):
    """
    View for getting the following users
    """
    usr = request.user
    followings = usr.profile.follows.all().order_by("-id")
    paginator = Paginator(followings, 5)
    page = request.GET.get("page")
    followings = paginator.get_page(page)
    return render(
        request, "accounts/following.html", {"usr": usr, "followings": followings}
    )


@login_required
def followers(request):
    """
    View for getting the followers
    """
    usr = request.user
    followers = usr.profile.followed_by.all().order_by("-followed_by")
    paginator = Paginator(followers, 5)
    page = request.GET.get("page")
    followers = paginator.get_page(page)
    return render(
        request, "accounts/followers.html", {"usr": usr, "followers": followers}
    )


def user_following(request, username):
    """
    View for getting the following users of a user
    """
    usr = get_object_or_404(User, username=username)
    followings = usr.profile.follows.all().order_by("-id")
    paginator = Paginator(followings, 5)
    page = request.GET.get("page")
    followings = paginator.get_page(page)
    if usr == request.user:
        return redirect("following")

    return render(
        request, "accounts/following.html", {"usr": usr, "followings": followings}
    )


def user_followers(request, username):
    """
    View for getting the followers of a user
    """
    usr = get_object_or_404(User, username=username)
    followers = usr.profile.followed_by.all().order_by("-id")
    paginator = Paginator(followers, 5)
    page = request.GET.get("page")
    followers = paginator.get_page(page)
    if usr == request.user:
        return redirect("followers")
    return render(
        request, "accounts/followers.html", {"usr": usr, "followers": followers}
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
    if request.method == "POST":
        user = request.user
        logout(request)
        user.is_active = False
        messages.success(request, "Account Deleted Successfully!")
        return redirect("home")
    else:
        return render(request, "accounts/delete_account.html")


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
            return redirect("profile")

    else:
        form = UsernameForm(initial={"username": request.user.username})
    return render(request, "accounts/change_username.html", {"form": form})


def user_image(request, username):
    """
    View for getting the image of a user
    """
    usr = get_object_or_404(User, username=username)
    return redirect(usr.profile.image.url)
