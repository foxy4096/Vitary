from random import choice
from typing import List

from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from ninja import Form, NinjaAPI
from ninja.errors import HttpError
from ninja.pagination import paginate
from ninja.security import django_auth

from apps.developer.authenticate import BotApiKey, UserApiKey
from apps.developer.constants import ZEN
from apps.developer.schema import CommentSchema, UserSchema, VitSchema
from apps.notification.utilities import notify
from apps.vit.models import *

auth = [django_auth, UserApiKey(), BotApiKey()]

api = NinjaAPI(
    title="Vitary API",
    description="Vitary API",
    version="1.0",
    urls_namespace="api",
    auth=auth,
    csrf=True,
)


@api.get("/zen", auth=None, response=str)
def zen(request):
    """
    The Zen of Python, by Tim Peters
    """
    return choice(ZEN.replace("\n", "").split("."))


@api.post("/login/", auth=None)
@csrf_exempt
def login(request, username: str = Form(...), password: str = Form(...)):
    """
    Login to the API.
    """
    user = authenticate(request, username=username, password=password)
    if user is None:
        raise HttpError(401, "Invalid username or password.")
    return {"token": user.devprofile.token.token}


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
    return Vit.objects.filter(
        Q(user=request.auth)
        | Q(user__profile__in=request.auth.profile.follows.all())
        | Q(user__profile__in=request.auth.profile.followed_by.all())
    ).order_by("-date")


@api.get("/myself/vits", response=List[VitSchema])
@paginate
def my_vits(request):
    """
    Returns a list of the user's vits.
    """
    return get_list_or_404(Vit, user=request.auth)


# My comments
@api.get("/myself/comments", response=List[CommentSchema])
@paginate
def my_comments(request):
    """
    Returns a list of the user's comments.
    """
    return get_list_or_404(Comment, user=request.auth)


@api.get("/users", response=List[UserSchema])
@paginate
def user_list(request):
    """
    Return a list of users.
    """
    return User.objects.all()


@api.get("/users/{username}", response=UserSchema)
def user_detail(request, username):
    """
    Return a user.
    """
    return get_object_or_404(User, username=username)


@api.post("/create/vit/", response=VitSchema)
@csrf_exempt
def create_vit(request, body: str = Form(...)):
    """
    Creates a vit.
    """
    return Vit.objects.create(
        user=request.auth,
        body=body,
    )


@api.get("/like/{vit_id}", response=int)
def like(request, vit_id: int):
    """
    Likes a vit.
    """
    vit = get_object_or_404(Vit, id=vit_id)
    if vit.likes.filter(id=request.auth.id).exists():
        vit.likes.remove(request.auth)
        vit.like_count -= 1
        vit.save()
    else:
        vit.likes.add(request.auth)
        vit.like_count += 1
        vit.save()
        if vit.user != request.auth:
            notify(
                message=f"{request.auth.username.title()} liked your Vit - '{vit.body}'",
                notification_type="like",
                to_user=vit.user,
                by_user=request.auth,
                link=reverse("vit_detail", kwargs={"pk": vit.id}),
            )

    return vit.likes.count()


# follow_user
@api.get("/follow/{username}", response=str)
def follow_user(request, username: str):
    """
    Follows a user.
    """
    user = get_object_or_404(User, username=username)
    if user != request.auth:
        if user.profile.follows.filter(id=request.auth.id).exists():
            user.profile.follows.remove(request.auth.profile)
            user.profile.follower_count = user.profile.followed_by.count()
            request.auth.profile.follower_count = (
                request.auth.profile.followed_by.count()
            )
            request.auth.profile.save()
            user.profile.save()
            return "Follow"
        else:
            user.profile.follows.add(request.auth.profile)
            user.profile.follower_count = user.profile.followed_by.count()
            request.auth.profile.follower_count = (
                request.auth.profile.followed_by.count()
            )
            request.auth.profile.save()
            user.profile.save()
            notify(
                message=f"{request.auth.username.title()} Followed You",
                by_user=request.auth,
                to_user=user,
                notification_type="follow",
                link=reverse("user_detail", kwargs={"username": request.auth.username}),
            )
            return "Unfollow"
    return "Follow"


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


@api.get("/vits/{username}", response=List[VitSchema])
@paginate
def vit_list_by_user(request, username):
    """
    Returns a list of vits by a user.
    """
    return get_list_or_404(Vit, user__username=username)


@api.get("/vits/{vit_id}", response=VitSchema)
def vit_detail(request, vit_id):
    """
    Returns a single vit.
    """
    return get_object_or_404(
        Vit,
        id=vit_id,
    )


@api.delete("/vits/{vit_id}")
def delete_vit(request, vit_id):
    """
    Deletes a vit.
    """
    vit = get_object_or_404(Vit, id=vit_id, user=request.auth).delete()
    return {"details": "Vit deleted."}


@api.post("/create/comment/reply", response=CommentSchema)
@csrf_exempt
def create_comment_reply(
    request,
    body: str = Form(...),
    vit_id: int = Form(...),
    reply_to_id: int = Form(...),
):
    """
    Creates a comment reply.
    """
    return Comment.objects.create(
        user=request.auth,
        body=body,
        vit_id=vit_id,
        reply_to_id=reply_to_id,
    )


@api.post("/create/comment/", response=CommentSchema)
@csrf_exempt
def create_comment(
    request,
    body: str = Form(...),
    vit_id: int = Form(...),
):
    """
    Creates a comment.
    """
    return Comment.objects.create(
        user=request.auth,
        body=body,
        vit_id=vit_id,
    )


@api.get("/comments", response=List[CommentSchema])
@paginate
def comment_list(request):
    """
    Returns a list of comments.
    """
    return Comment.objects.all()


@api.get("/comments/{comment_id}", response=CommentSchema)
def comment_detail(request, comment_id):
    """
    Returns a single comment.
    """
    return get_object_or_404(Comment, id=comment_id)


@api.get("/comments/user/{username}", response=List[CommentSchema])
@paginate
def comment_list_by_user(request, username):
    """
    Returns a list of comments by a user.
    """
    return get_list_or_404(
        Comment,
        user__username=username,
    )


@api.delete("/comments/{comment_id}")
def delete_comment(request, comment_id):
    """
    Deletes a comment.
    """
    get_object_or_404(Comment, id=comment_id, user=request.auth).delete()
    return {"detail": "Comment deleted"}
