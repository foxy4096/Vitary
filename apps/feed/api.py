from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.feed.models import Feed


from apps.notification.utilities import create_notification


# THIS API VIEW IS DEPRECATED!!

@login_required
def like(request):
    try:
        feed = Feed.objects.get(id=request.GET.get("feed_pk"))
        if feed.likes.filter(id=request.user.id).exists():
            feed.likes.remove(request.user)
            feed.like_count -= 1
            feed.save()
            return JsonResponse(
                {"status": "success", "likes": feed.likes.count(), "liked": False},
                status=200,
            )
        else:
            feed.likes.add(request.user)
            feed.like_count += 1
            feed.save()
            if feed.user != request.user:
                create_notification(
                    verb="like",
                    sender=feed.user,
                    receiver=request.user,
                    content_object=feed,
                )
            return JsonResponse(
                {"status": "success", "likes": feed.likes.count(), "liked": True},
                status=200,
            )
    except feed.DoesNotExist:
        return JsonResponse({"error": "feed not found"}, status=404)
