from ninja import ModelSchema, Schema
from django.contrib.auth.models import User
from apps.accounts.models import Profile
from apps.core.models import Badge
from typing import List
from apps.vit.models import Vit, Comment


class BadgeSchema(ModelSchema):
    class Config:
        model = Badge
        model_fields = ['id', 'name', 'description']


class ProfileSchema(ModelSchema):
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
    profile: ProfileSchema

    class Config:
        model = User
        model_fields = [
            "id",
            "username",
            "first_name",
            "last_name",
        ]

class VitSchema(ModelSchema):
    user: UserSchema
    class Config:
        model = Vit
        model_fields = [
            'id',
            'body',
            'date',
            'like_count',
            'image',
            'video',
            'nsfw',
        ]
    
class CommentCreateSchema(Schema):
    body: str
    vit_body: int



class CommentSchema(ModelSchema):
    user: UserSchema
    vit: VitSchema
    class Config:
        model = Comment
        model_fields = ['id', 'body', 'vit', 'user', 'date']