from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


from apps.vit.models import Vit
from apps.notification.utilities import notify

@login_required
def like(request):
    vit = get_object_or_404(Vit, request.GET.get('vit_pk'))
    if vit.likes.filter(id=request.user.id).exists():
        vit.likes.remove(request.user)
        vit.like_count -= 1
        vit.save()
        return JsonResponse({'status': 'success', 'likes': vit.likes.count(), 'liked': False}, status=200)
    else:
        vit.likes.add(request.user)
        vit.like_count += 1
        vit.save()
        if vit.user != request.user:
            notify(message=f"{request.user.username.title()} liked your Vit - '{vit.body}'", notification_type="like", to_user=vit.user,
                    by_user=request.user, link=reverse('vit_detail', kwargs={'pk': vit.id}))
        return JsonResponse({'status': 'success', 'likes': vit.likes.count(), 'liked': True}, status=200)
