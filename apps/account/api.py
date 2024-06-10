from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from apps.notification.utilities import create_notification


@login_required
def user_search_api(request):
    """
    Returns the userprofiles of the users with the given username query.
    """
    try:
        query = request.GET.get("query")
        users = User.objects.filter(
            Q(username__icontains=query)
            | Q(email__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        return JsonResponse({"users": [user.userprofile.to_json() for user in users]})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


@login_required
def follow(request):
    """
    Follows the user with the given username in the request data.
    """
    to_follow = get_object_or_404(User, username=request.GET.get("username"))
    if to_follow.userprofile not in request.user.userprofile.follows.all():
        request.user.userprofile.follows.add(to_follow.userprofile)
        request.user.userprofile.following_count = (
            request.user.userprofile.follows.count()
        )
        to_follow.userprofile.follower_count = to_follow.userprofile.followed_by.count()
        request.user.userprofile.save()
        to_follow.userprofile.save()
        create_notification(
            actor=request.user,
            recipient=to_follow,
            verb="followed",
            object_id=request.user.id,
            object_type="user"
        )
        return JsonResponse({"success": "Followed Successfully", "follow": True})
    elif to_follow.userprofile in request.user.userprofile.follows.all():
        request.user.userprofile.follows.remove(to_follow.userprofile)
        request.user.userprofile.following_count = (
            request.user.userprofile.follows.count()
        )
        to_follow.userprofile.follower_count = to_follow.userprofile.followed_by.count()
        request.user.userprofile.save()
        to_follow.userprofile.save()
        return JsonResponse({"success": "Unfollowed Successfully", "follow": False})

def get_user_avatar(request, username):
    user = get_object_or_404(User, username=username)
    return redirect(f"{user.userprofile.avatar()}")