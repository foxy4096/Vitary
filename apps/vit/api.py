from django.http import JsonResponse
from django.urls import reverse

from apps.vit.models import Vit
from apps.notification.utilities import notify

def add_like(request):
    if request.user.is_authenticated:
        vit = Vit.objects.get(id=request.GET.get('vit_pk'))
        if vit.likes.filter(id=request.user.id).exists():
            vit.likes.remove(request.user)
            vit.like_count -= 1
            vit.save()
            return JsonResponse({'status': 'success', 'likes': vit.likes.count()})
        else:
            vit.likes.add(request.user)
            vit.like_count += 1
            vit.save()
            if vit.user != request.user:
                notify(message=f"{request.user.username.title()} liked your Vit - '{vit.body}'", notification_type="like", to_user=vit.user,
                    by_user=request.user, link=reverse('vit_detail', kwargs={'pk': vit.id}))
            return JsonResponse({'status': 'success', 'likes': vit.likes.count()})
    else:
        return JsonResponse({'status': 'failure'})