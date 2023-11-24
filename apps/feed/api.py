from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from apps.feed.models import Feed
from apps.notification.utilities import notify

@login_required
def like(request):
    try:
        feed = feed.objects.get(id=request.GET.get('feed_pk'))
        if feed.likes.filter(id=request.user.id).exists():
            feed.likes.remove(request.user)
            feed.like_count -= 1
            feed.save()
            return JsonResponse({'status': 'success', 'likes': feed.likes.count(), 'liked': False}, status=200)
        else:
            feed.likes.add(request.user)
            feed.like_count += 1
            feed.save()
            if feed.user != request.user:
                notify(message=f"{request.user.username.title()} liked your feed - '{feed.body}'", notification_type="like", to_user=feed.user,
                        by_user=request.user, link=reverse('feed_detail', kwargs={'pk': feed.id}))
            return JsonResponse({'status': 'success', 'likes': feed.likes.count(), 'liked': True}, status=200)
    except feed.DoesNotExist:
        return JsonResponse({'error': 'feed not found'}, status=404)
