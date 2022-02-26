import json
from django.http import JsonResponse
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt

from apps.vit.models import Vit
from apps.notification.utilities import notify
from apps.vit.utilities import find_mention, find_plustag
from .forms import VitForm

from apps.develop.backends import KeyBackend


def like(request):
    user = KeyBackend().authenticate(request)
    if request.user.is_authenticated:
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
    else:
        return JsonResponse({'status': 'failure'})


def get_vits(request):
    user = KeyBackend().authenticate(request)
    if request.user.is_authenticated:
        vits = Vit.objects.filter(user=request.user)
        return JsonResponse({'vits': [vit.to_json() for vit in vits]})
    else:
        return JsonResponse({'error': 'You must be logged in'})


def get_vit(request):
    user = KeyBackend().authenticate(request)
    if request.user.is_authenticated:
        print(request.GET.get('vit_pk'))
        try:
            vit = Vit.objects.get(id=request.GET.get('vit_pk'))
            return JsonResponse({'vit': vit.to_json()})
        except:
            return JsonResponse({'error': 'Vit not found'}, status=404)
    else:
        return JsonResponse({'error': 'You must be logged in'})


@csrf_exempt
def add_vit(request):
    user = KeyBackend().authenticate(request)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = VitForm(request.POST)
            if form.is_valid():
                vit = form.save(commit=False)
                vit.user = request.user
                vit.save()
                find_mention(vit=vit, request=request, ntype="vit")
                find_plustag(vit=vit)
                return JsonResponse({'status': 'success', 'vit': vit.to_json()}, status=201)
            else:
                print(form.errors)
                return JsonResponse({'error': 'No vit body provided'}, status=400)
        else:
            return JsonResponse({'error': 'You must be logged in'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
