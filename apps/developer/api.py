from random import choice

from ninja import NinjaAPI, Form
from ninja.pagination import paginate
from apps.vit.models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from typing import List
from .constants import ZEN
from ninja.security import django_auth
from .authenticate import UserApiKey, BotApiKey
from .schema import UserSchema, VitSchema, CommentCreateSchema, CommentSchema

auth = [django_auth, UserApiKey(), BotApiKey()]

api = NinjaAPI(
    title="Vitary API",
    description="Vitary API",
    version="1.0",
    urls_namespace="api",
    auth=auth,
    csrf=True,
)


@api.get("/zen", auth=None)
def zen(request):
    """
    The Zen of Python, by Tim Peters
    """
    return choice(ZEN.replace("\n", "").split("."))


@api.get("/myself", response=UserSchema)
def myself(request):
    """
    Return the user's profile.
    """
    return request.auth


@api.get("/feed", response=List[VitSchema])
@paginate
def feed(request):
    """
    Returns a feed of the latest vits.
    """
    vits = Vit.objects.filter(
        Q(user=request.user)
        | Q(user__profile__in=request.auth.profile.follows.all())
        | Q(user__profile__in=request.auth.profile.followed_by.all())
    ).order_by("-date")
    if not request.auth.profile.allow_nsfw:
        vits = vits.exclude(nsfw=True)

    return vits


@api.get("/vits", response=List[VitSchema])
@paginate
def vit_list(request):
    """
    Returns a list of vits.
    """
    vits = Vit.objects.all().order_by("-date")
    if not request.auth.profile.allow_nsfw:
        vits = vits.exclude(nsfw=True)
    return vits


@api.get("/vits/{vit_id}", response=VitSchema)
def vit_detail(request, vit_id):
    """
    Returns a single vit.
    """
    return get_object_or_404(Vit, id=vit_id)


@api.post("/create/vit/", response=VitSchema)
@csrf_exempt
def create_vit(request, body: str = Form(...)):
    """
    Creates a vit.
    """
    vit = Vit.objects.create(user=request.auth, body=body)
    return vit


@api.post("/create/comment/", response=CommentSchema)
@csrf_exempt
def create_comment(request, body: str = Form(...), vit_id: int = Form(...)):
    """
    Creates a comment.
    """
    vit: Vit = get_object_or_404(Vit, id=vit_id)
    comment = Comment.objects.create(user=request.auth, vit=vit, body=body)
    return comment
