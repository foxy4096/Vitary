from typing import List

from django.contrib.auth.models import User
from ninja import ModelSchema, Schema

from apps.accounts.models import Profile
from apps.core.models import Badge
from apps.notification.models import Notification
from apps.vit.models import Comment, Vit, Embed


class EmbedSchema(ModelSchema):
    """
    Schema for Embed model.
    """

    id: int
    title: str

    class Config:
        model = Embed
        model_fields = ["id", "url", "title", "description", "image_url"]


class BadgeSchema(ModelSchema):
    """
    Schema for Badge model.
    """

    class Config:
        model = Badge
        model_fields = ["id", "name", "description"]


class ProfileSchema(ModelSchema):
    """
    Schema for Profile model.
    """

    badges: List[BadgeSchema] = []

    class Config:
        model = Profile
        model_fields = [
            "avatar",
            "header_image",
            "follower_count",
            "following_count",
            "bio",
            "status",
            "verified",
            "allow_nsfw",
        ]


class UserSchema(ModelSchema):
    """
    Schema for User model.
    """

    profile: ProfileSchema

    class Config:
        model = User
        model_fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_superuser",
            "is_staff",
        ]


class VitSchema(ModelSchema):
    """
    Schema for Vit model.
    """

    user: UserSchema
    embeds: List[EmbedSchema] = []

    class Config:
        model = Vit
        model_fields = [
            "id",
            "body",
            "date",
            "like_count",
            "image",
            "video",
            "nsfw",
        ]


class CommentSchema(ModelSchema):
    """
    Schema for Comment model.
    """

    user: UserSchema
    vit: VitSchema

    class Config:
        model = Comment
        model_fields = [
            "id",
            "body",
            "vit",
            "user",
            "date",
            "reply_to",
        ]


class NotificationSchema(ModelSchema):
    """
    Schema for notifications
    """

    class Config:
        model = Notification
        model_fields = [
            "id",
            "message",
            "date",
            "is_read",
        ]
