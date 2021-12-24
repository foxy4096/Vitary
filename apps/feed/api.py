import json

from django.urls import reverse
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from apps.feed.models import Feed
from apps.notification.utilities import notify


@login_required
def add_like(request):
    if request.method == "POST":
        data = json.loads(request.body)
        feed_id = data['feed_id']
        feed = Feed.objects.get(id=feed_id)
        if feed.likes.filter(id=request.user.id).exists():
            feed.likes.remove(request.user)
            feed.like_count -= 1
            feed.save()
            return JsonResponse({'status': 'success', 'likes': feed.likes.count()})
        else:
            feed.likes.add(request.user)
            feed.like_count += 1
            feed.save()
            if feed.user != request.user:
                notify(message=f"{request.user.username.title()} liked your post - '{feed.body}'", notification_type="like", to_user=feed.user,
                    by_user=request.user, link=reverse('feed_detail', kwargs={'pk': feed.id}))
            return JsonResponse({'status': 'success', 'likes': feed.likes.count()})
    return JsonResponse({'success': False})
