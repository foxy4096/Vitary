import json
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse_lazy

from apps.develop.backends import KeyBackend

from apps.notification.utilities import notify


def user_view_api(request, username):
    """
    Returns the profile of the user with the given username.
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'user': user.profile.to_json()})


def user_search_api(request):
    """
    Returns the profiles of the users with the given username query.
    """
    user = KeyBackend().authenticate(request)
    if request.user.is_authenticated:
        try:
            username = request.GET.get('username')
            users = User.objects.filter(Q(username__icontains=username) | Q(email__icontains=username) | Q(first_name__icontains=username) | Q(last_name__icontains=username))
            return JsonResponse({'users': [user.profile.to_json() for user in users]})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'You must be logged in'}, status=401)

   
    
def follow(request):
    """
    Follows the user with the given username in the request data.
    """
    user = KeyBackend().authenticate(request)
    if request.user.is_authenticated:
        try:
            to_follow = User.objects.get(username=request.GET.get('username'))
        except:
            return JsonResponse({'error': "No User Provided"})
        if to_follow.profile not in request.user.profile.follows.all():
            request.user.profile.follows.add(to_follow.profile)
            request.user.profile.following_count = request.user.profile.follows.count()
            to_follow.profile.follower_count = to_follow.profile.followed_by.count()
            request.user.profile.save()
            to_follow.profile.save()
            notify(message=f"{request.user.username.title()} Followed You",
                by_user=request.user, to_user=to_follow, notification_type="follow", link=reverse_lazy('profile_view', kwargs={'username': request.user.username}))
            return JsonResponse({'success': "Followed Successfully", 'follow': True})
        elif to_follow.profile in request.user.profile.follows.all():
            request.user.profile.follows.remove(to_follow.profile)
            request.user.profile.following_count = request.user.profile.follows.count()
            to_follow.profile.follower_count = to_follow.profile.followed_by.count()
            request.user.profile.save()
            to_follow.profile.save()
            return JsonResponse({'success': "Unfollowed Successfully", 'follow': False})
    else:
        return JsonResponse({'error': 'You must be logged in'}, status=401)

