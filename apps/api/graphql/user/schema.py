from graphene import relay, ObjectType

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from apps.account.models import User, UserProfile
import graphene


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            "username": ["exact", "icontains"],
            "first_name": ["exact", "icontains"],
            "last_name": ["exact", "icontains"],
            "is_staff": ["exact"],
            "is_superuser": ["exact"],
            "is_active": ["exact"],
        }
        interfaces = (relay.Node,)
        exclude = ["password", "email"]


class UserProfileSchema(DjangoObjectType):
    class Meta:
        model = UserProfile
        filter_fields = {
            "is_verified": ["exact"],
        }


class Query(ObjectType):
    users = DjangoFilterConnectionField(UserNode)
    user = relay.Node.Field(UserNode)
