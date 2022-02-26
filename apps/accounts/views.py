from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from apps.notification.utilities import notify
from .forms import UserForm, ProfileForm
from .forms import UserRegisterForm, UsernameForm, GroupForm
from .models import Group, GroupInvitation


def signup(request):
    """
    View for signup
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully \n Now go to your profile and update your profile')
            return redirect('profile')
        else:
            if User.objects.filter(username=request.POST['username']).exists():
                messages.add_message(
                    request, 40, 'Username already exists! \n Woops look like someone have already taken your identity', extra_tags='danger')
                return redirect('signup')
            elif request.POST['password1'] != request.POST['password2']:
                messages.add_message(
                    request, 40, "Passwords do not match \n don't rush you dumbo", extra_tags='danger')
                return redirect('signup')
            else:
                messages.add_message(
                    request, 40, 'Unknown Error Occured \n Now go and fuck yourself!', extra_tags='danger')
                return redirect('signup')
    else:
        form = UserRegisterForm()
        return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_edit(request):
    """
    View for editing profile
    """
    if request.method == "POST":
        uform = UserForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST, request.FILES,
                            instance=request.user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "Profile Edited Successfully! \n You look awful!")
            return redirect('profile')
    else:
        uform = UserForm(instance=request.user)
        pform = ProfileForm(instance=request.user.profile)
        return render(request, 'accounts/profile.html', {'uform': uform, 'pform': pform})


def profile(request, username):
    """
    View for profile
    """
    usr = get_object_or_404(User, username=username)
    vits = usr.vits.all()
    paginator = Paginator(vits, 5)
    page = request.GET.get('page')
    vits = paginator.get_page(page)
    return render(request, 'accounts/profile_view.html', {'usr': usr, 'vits': vits, 'onProfile': True})


@login_required
def following(request):
    """
    View for getting the following users
    """
    usr = request.user
    followings = usr.profile.follows.all().order_by('-id')
    paginator = Paginator(followings, 5)
    page = request.GET.get('page')
    followings = paginator.get_page(page)
    return render(request, 'accounts/following.html', {'usr': usr, 'followings': followings})


@login_required
def followers(request):
    """
    View for getting the followers
    """
    usr = request.user
    followers = usr.profile.followed_by.all().order_by('-id')
    paginator = Paginator(followers, 5)
    page = request.GET.get('page')
    followers = paginator.get_page(page)
    return render(request, 'accounts/followers.html', {'usr': usr, 'followers': followers})


def user_following(request, username):
    """
    View for getting the following users of a user
    """
    usr = get_object_or_404(User, username=username)
    followings = usr.profile.follows.all().order_by('-id')
    paginator = Paginator(followings, 5)
    page = request.GET.get('page')
    followings = paginator.get_page(page)
    if usr == request.user:
        return redirect('following')

    return render(request, 'accounts/following.html', {'usr': usr, 'followings': followings})


def user_followers(request, username):
    """
    View for getting the followers of a user
    """
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
    """
    View for advanced settings
    """
    return render(request, 'accounts/advance.html')


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
        return redirect('home')
    else:
        return render(request, 'accounts/delete_account.html')


@login_required
def change_username(request):
    """
    View for changing username
    """
    if request.method == "POST":
        form = UsernameForm(request.POST)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data['username']
            user.save()
            messages.success(request, "Username Changed Successfully! \n Now nobody knows who are you dumbo!")
            return redirect('profile')

    else:
        form = UsernameForm(initial={'username': request.user.username})
    return render(request, 'accounts/change_username.html', {'form': form})


@login_required
def create_group(request):
    """
    View for creating a group
    """
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin.add(request.user)
            group.slug = slugify(group.name)
            group.save()
            group.members.add(request.user)
            messages.success(request, "Group Created Successfully!")
            return redirect('profile_view', username=request.user.username)
    else:
        form = GroupForm()
    return render(request, 'accounts/group/create_group.html', {'form': form})


def group_detail(request, group_slug):
    """
    View for group
    """
    group = get_object_or_404(Group, slug=group_slug)
    if group.is_public or request.user in group.members.all():
        return render(request, 'accounts/group/group_view.html', {'group': group})
    else:
        raise Http404


@login_required
def edit_group(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if request.user in group.admin.all():
        if request.method == "POST":
            form = GroupForm(request.POST, request.FILES, instance=group)
            if form.is_valid():
                form.save()
                messages.success(request, "Group Edited Successfully!")
                return redirect('group_detail', group_slug=group.slug)
        else:
            form = GroupForm(instance=group)
            return render(request, 'accounts/group/edit_group.html', {'group': group, 'form': form})
    else:
        messages.success(request, "You are not authorized to edit this group! \n who the fuck you think you are?")
        return redirect('group_detail', group_slug=group.slug)


@login_required
def delete_group(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if request.user in group.admin.all():
        if group.members.count() == 1:
            group.delete()
            messages.success(request, "Group Deleted Successfully!")
            return redirect('profile_view', username=request.user.username)
        else:
            messages.success(request, "You can't delete this group! \n Just Why?")
            return redirect('group_detail', group_slug=group.slug)
    else:
        messages.success(
            request, "You are not authorized to delete this group! \n I think you are a ⌐7¢C↑p┘─")
        return redirect('group_detail', group_slug=group.slug)


@login_required
def invite_member(request, group_slug, username):
    group = get_object_or_404(Group, slug=group_slug)
    if request.user in group.admin.all():
        user = get_object_or_404(User, username=username)
        if user not in group.members.all():
            GroupInvitation.objects.get_or_create(
                group=group, user=user, invited_by=request.user)
            notify(by_user=request.user, to_user=user, message=f'{ request.user.username } invited you to join group { group.name }', link=reverse(
                'group_detail', kwargs={'group_slug': group.slug}), notification_type='invitation')
            user.email_user(
                f'{ request.user.username } invited you to join group { group.name }', f'{ request.user.username } invited you to join group { group.name }')
            messages.success(request, "Invitation Sent Successfully!")
            return redirect('group_detail', group_slug=group.slug)
        else:
            messages.success(request, "Member Already Exists!")
            return redirect('group_detail', group_slug=group.slug)
    else:
        messages.success(request, "You are not authorized to add a member \n I am not sure why you are here")
        return redirect('group_detail', group.slug)


@login_required
def remove_member(request, group_slug, username):
    group = get_object_or_404(Group, slug=group_slug)
    if request.user in group.admin.all():
        user = get_object_or_404(User, username=username)
        if user in group.members.all():
            group.members.remove(user)
            messages.success(request, "Member Removed Successfully!")
            return redirect('group_detail', group_slug=group.slug)
        else:
            messages.success(request, "Member Doesn't Exist!")
            return redirect('group_detail', group_slug=group.slug)
    else:
        messages.success(request, "You are not authorized to remove a member \n I am not sure why you are here")
        return redirect('group_detail', group.slug)

@login_required
def accept_invitation(request, group_slug, invitation_id):
    group = get_object_or_404(Group, slug=group_slug)
    invitation = get_object_or_404(GroupInvitation, id=invitation_id)
    if invitation.user == request.user:
        if invitation.group == group:
            if request.user not in group.members.all():
                group.members.add(request.user)
                invitation.delete()
                messages.success(request, "Invitation Accepted Successfully!")
                return redirect('group_detail', group_slug=group.slug)
            else:
                messages.success(request, "You are already a member of this group! \n Why are you here?, you know it cost me processing power to process this response.")
                return redirect('group_detail', group_slug=group.slug)
        else:
            messages.success(request, "You are not authorized to accept this invitation \n who gave you this link?")
            return redirect('group_detail', group_slug=group.slug)

    else:
        messages.success(request, "You are not authorized to accept this invitation! \n don't snoop here and there and go on broken links!")
        return redirect('group_detail', group_slug=group.slug)

@login_required
def reject_invitation(request, group_slug, invitation_id):
    group = get_object_or_404(Group, slug=group_slug)
    invitation = get_object_or_404(GroupInvitation, id=invitation_id)
    if invitation.user == request.user:
        if invitation.group == group:
            invitation.delete()
            messages.success(request, "Invitation Rejected Successfully! \n See you sucker!")
            return redirect('group_detail', group_slug=group.slug)
        else:
            messages.success(request, "You are not authorized to reject this invitation \n You can only reject your own invitations")
            return redirect('group_detail', group_slug=group.slug)
    else:
        messages.success(request, "You are not authorized to reject this invitation! \n hey where did you get this invitation link from?")
        return redirect('group_detail', group_slug=group.slug)

@login_required
def leave_group(request, group_slug):
    group = get_object_or_404(Group, slug=group_slug)
    if request.user in group.members.all():
        group.members.remove(request.user)
        messages.success(request, "You have left the group! Well I don't know what to say!")
        return redirect('group_detail', group_slug=group.slug)
    elif request.user in group.admin.all() and group.members.count() == 1:
        group.delete()
        messages.success(request, "You have left the group! and as the only member of the group, the group has been deleted!")
        return redirect('profile_view', username=request.user.username)
    else:
        messages.success(request, "You are not a member of this group! so who the fuck are you?")
        return redirect('group_detail', group_slug=group.slug)