from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from apps.vit.models import Vit
from apps.notification.utilities import notify

@login_required
def like(request):
    try:
        vit = Vit.objects.get(id=request.GET.get('vit_pk'))
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
    except Vit.DoesNotExist:
        return JsonResponse({'error': 'Vit not found'}, status=404)
