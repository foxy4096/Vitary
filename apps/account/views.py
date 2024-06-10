from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from apps.core.utilities import paginate

from .forms import UserForm, UserProfileForm, UsernameForm, DateOfBirthForm, UserProfileAvatarForm

class SignupView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, "Account created successfully")
        return response

    def get_success_url(self):
        return reverse_lazy("edit_userprofile")

class EditUserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "accounts/edit_userprofile.html"
    success_url = reverse_lazy("edit_userprofile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pform"] = UserProfileForm(instance=self.request.user.userprofile)
        context["aform"] = UserProfileAvatarForm(instance=self.request.user.userprofile)
        context["dform"] = DateOfBirthForm(instance=self.request.user.userprofile)
        return context

    def form_valid(self, form):
        pform = UserProfileForm(self.request.POST, instance=self.request.user.userprofile)
        aform = UserProfileAvatarForm(self.request.POST, self.request.FILES, instance=self.request.user.userprofile)
        dform = DateOfBirthForm(self.request.POST, instance=self.request.user.userprofile)

        if pform.is_valid() and dform.is_valid() and aform.is_valid():
            form.save()
            pform.save()
            dform.save()
            aform.save()
            messages.success(self.request, "UserProfile Edited Successfully! \n You look nice!")
        return super().form_valid(form)

class AdvancedSettingsView(LoginRequiredMixin, View):
    template_name = "accounts/advance.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class DeleteAccountView(LoginRequiredMixin, View):
    template_name = "accounts/delete_account.html"

    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.is_active = False
        messages.success(request, "Account Deleted Successfully!")
        return redirect("home")
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ChangeUsernameView(LoginRequiredMixin, View):
    template_name = "accounts/change_username.html"

    def get(self, request, *args, **kwargs):
        form = UsernameForm(initial={"username": request.user.username})
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = UsernameForm(request.POST)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data["username"]
            user.save()
            messages.success(request, "Username Changed Successfully!")
            return redirect("edit_userprofile")
        return render(request, self.template_name, {"form": form})


class UserDetailView(View):
    template_name = "accounts/user_detail.html"

    def get(self, request, username, *args, **kwargs):
        tuser = get_object_or_404(User, username__iexact=username)
        feeds = tuser.feeds.all()
        if request.user.is_authenticated and not request.user.userprofile.allow_nsfw:
            feeds = feeds.exclude(nsfw=True)
        return render(request, self.template_name, {"tuser": tuser, "feeds": paginate(request, feeds)})

class UserFollowingView(View):
    template_name = "accounts/following.html"

    def get(self, request, username, *args, **kwargs):
        tuser = get_object_or_404(User, username=username)
        followings = paginate(request, tuser.userprofile.follows.all().order_by("-id"))
        return render(request, self.template_name, {"tuser": tuser, "followings": followings})

class UserFollowersView(View):
    template_name = "accounts/followers.html"

    def get(self, request, username, *args, **kwargs):
        tuser = get_object_or_404(User, username=username)
        followers = paginate(request, tuser.userprofile.followed_by.all().order_by("-id"))
        return render(request, self.template_name, {"tuser": tuser, "followers": followers})