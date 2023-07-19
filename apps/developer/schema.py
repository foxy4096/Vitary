from typing import List

from django.contrib.auth.models import User
from ninja import ModelSchema, Schema

from apps.accounts.models import Profile
from apps.core.models import Badge
from apps.vit.models import Comment, Vit


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
            "image",
            "header_image",
            "follower_count",
            "following_count",
            "bio",
            "status",
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