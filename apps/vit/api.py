from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django.urls import reverse
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.csrf import csrf_exempt


from apps.vit.utilities import find_mention, find_plustag
from django.urls import reverse_lazy

from apps.vit.models import Vit
from apps.notification.utilities import notify

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_like(request):
    vit = Vit.objects.get(id=request.GET.get('vit_pk'))
    if vit.likes.filter(id=request.user.id).exists():
        vit.likes.remove(request.user)
        vit.like_count -= 1
        vit.save()
        return Response({'status': 'success', 'likes': vit.likes.count()})
    else:
        vit.likes.add(request.user)
        vit.like_count += 1
        vit.save()
        if vit.user != request.user:
            notify(message=f"{request.user.username.title()} liked your Vit - '{vit.body}'", notification_type="like", to_user=vit.user,
                   by_user=request.user, link=reverse('vit_detail', kwargs={'pk': vit.id}))
        return Response({'status': 'success', 'likes': vit.likes.count()})

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vit_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 100
    vits = Vit.objects.all()
    vits = paginator.paginate_queryset(vits, request)
    serializer = serializers.VitSerializer(vits, many=True)
    return paginator.get_paginated_response(serializer.data)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vit(request, vit_pk):
    vit = get_object_or_404(Vit, id=vit_pk)
    serializer = serializers.VitSerializer(vit)
    return Response(serializer.data)

@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_vit(request, vit_pk):
    data = request.data
    vit = get_object_or_404(Vit, id=vit_pk)
    if vit.user != request.user:
        return Response({'status': 'error', 'message': 'Not authorized'})
    serializer = serializers.VitSerializer(vit, data=data, partial=True, many=False)
    if serializer.is_valid():
        find_mention(request=request, vit=vit)
        find_plustag(vit=vit)
        serializer.save()
        return Response(serializer.data)
    return Response({'status': 'error', 'message': serializer.errors})

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_vit(request):
    data = request.data
    files = request.FILES
    vit = Vit.objects.create(user=request.user, body=data.get('body'), image=files.get('image'), video=files.get('video'))
    if request.POST.get('reply_vit_pk', '') != '':
        reply_vit_pk = request.POST.get('reply_vit_pk', '')
        reply_vit = get_object_or_404(Vit, id=reply_vit_pk)
        vit.to_reply_vits = reply_vit
        reply_vit.save()
        vit.save()
        if reply_vit.user != request.user:
            notify(message=f"{request.user.username.title()} replied to your Vit - '{reply_vit.body}'", notification_type="reply", to_user=reply_vit.user,
                    by_user=request.user, link=reverse_lazy('vit_detail', kwargs={'pk': vit.id}))
    find_mention(request=request, vit=vit)
    find_plustag(vit=vit)
    serializer = serializers.VitSerializer(vit, many=False)
    return Response(serializer.data)


@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_vit(request, vit_pk):
    vit = get_object_or_404(Vit, id=vit_pk)
    if vit.user != request.user:
        return Response({'status': 'error', 'message': 'Not authorized'})
    else:
        vit.delete()
        return Response({'status': 'success'})

