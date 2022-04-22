import json

from django.http import JsonResponse
from .models import DevProfile

import secrets


def generate_api_key(request):
    if request.user.is_authenticated:
        if DevProfile.objects.filter(user=request.user).exists():
            devprofile = DevProfile.objects.get(user=request.user)
            if devprofile.public_key and devprofile.private_key:
                return JsonResponse(
                    {'public_key': str(devprofile.public_key), 'private_key': str(devprofile.private_key)})
            else:
                devprofile.public_key, devprofile.private_key = secrets.token_hex(16), secrets.token_hex(16)
                devprofile.save()
                return JsonResponse(
                    {'public_key': str(devprofile.public_key), 'private_key': str(devprofile.private_key)})
        else:
            return JsonResponse({'error': 'You don\'t have a Dev Profile'})
    else:
        return JsonResponse({'error': 'You must be logged in'})


def refresh_api_key(request):
    if request.user.is_authenticated:
        if DevProfile.objects.filter(user=request.user).exists():
            devprofile = DevProfile.objects.get(user=request.user)
            devprofile.public_key, devprofile.private_key = secrets.token_hex(16), secrets.token_hex(16)
            devprofile.save()
            return JsonResponse({'public_key': str(devprofile.public_key), 'private_key': str(devprofile.private_key)})
        else:
            return JsonResponse({'error': 'You don\'t have a Dev Profile'})
    else:
        return JsonResponse({'error': 'You must be logged in'})


def revoke_api_key(request):
    if request.user.is_authenticated:
        if DevProfile.objects.filter(user=request.user).exists():
            devprofile = DevProfile.objects.get(user=request.user)
            devprofile.public_key = None
            devprofile.private_key = None
            devprofile.save()
            return JsonResponse({'success': 'API Key deleted'})
        else:
            return JsonResponse({'error': 'You don\'t have a Dev Profile'})
    else:
        return JsonResponse({'error': 'You must be logged in'})


def edit_profile_api(request):
    if request.user.is_authenticated:
        if DevProfile.objects.filter(user=request.user).exists():
            devprofile = DevProfile.objects.get(user=request.user)
            devprofile.firstname = request.POST.get('firstname')
            devprofile.lastname = request.POST.get('lastname')
            devprofile.email = request.POST.get('email')
            devprofile.bio = request.POST.get('bio')
            devprofile.github_username = request.POST.get('github')
            devprofile.twitter_username = request.POST.get('twitter')
            devprofile.website = request.POST.get('website')
            devprofile.save()
            return JsonResponse({'success': 'Profile updated', 'profile': devprofile.to_json()})
        else:
            return JsonResponse({'error': 'You don\'t have a Dev Profile'})
    else:
        return JsonResponse({'error': 'You must be logged in'})
