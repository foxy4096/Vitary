from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.notification.utilities import notify


@login_required
def user_search_api(request):
    """
    Returns the profiles of the users with the given username query.
    """
    try:
        query = request.GET.get("query")
        users = User.objects.filter(
            Q(username__icontains=query)
            | Q(email__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        return JsonResponse({"users": [user.profile.to_json() for user in users]})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


@login_required
def follow(request):
    """
    Follows the user with the given username in the request data.
    """
    to_follow = get_object_or_404(User, username=request.GET.get("username"))
    if to_follow.profile not in request.user.profile.follows.all():
        request.user.profile.follows.add(to_follow.profile)
        request.user.profile.following_count = request.user.profile.follows.count()
        to_follow.profile.follower_count = to_follow.profile.followed_by.count()
        request.user.profile.save()
        to_follow.profile.save()
        notify(
            message=f"{request.user.username.title()} Followed You",
            by_user=request.user,
            to_user=to_follow,
            notification_type="follow",
            link=reverse_lazy(
                "user_detail", kwargs={"username": request.user.username}
            ),
        )
        return JsonResponse({"success": "Followed Successfully", "follow": True})
    elif to_follow.profile in request.user.profile.follows.all():
        request.user.profile.follows.remove(to_follow.profile)
        request.user.profile.following_count = request.user.profile.follows.count()
        to_follow.profile.follower_count = to_follow.profile.followed_by.count()
        request.user.profile.save()
        to_follow.profile.save()
        return JsonResponse({"success": "Unfollowed Successfully", "follow": False})
