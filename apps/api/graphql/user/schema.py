from graphene import relay, ObjectType
from graphql_jwt.decorators import login_required

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from apps.account.models import User, UserProfile
import graphene


class UserNode(DjangoObjectType):
    avatar = graphene.String()

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
    avatar = graphene.String()

    class Meta:
        model = UserProfile
        filter_fields = {
            "is_verified": ["exact"],
        }

    def resolve_avatar(self, info):
        return self.avatar()


class Query(ObjectType):
    users = DjangoFilterConnectionField(UserNode)
    user = relay.Node.Field(UserNode)
    me = graphene.Field(UserNode)
    user_by_username = graphene.Field(UserNode, username=graphene.String())

    def resolve_user_by_username(self, info, username):
        try:
            return User.objects.get(username=username)
        # sourcery skip: raise-specific-error
        except User.DoesNotExist as e:
            raise Exception("User not found") from e

    @login_required
    def resolve_me(self, info):
        return info.context.user
