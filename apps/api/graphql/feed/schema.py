from graphene import relay, ObjectType

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from apps.feed.models import Feed
import graphene


class FeedNode(DjangoObjectType):
    class Meta:
        model = Feed
        filter_fields = ("body",)
        interfaces = (relay.Node,)


class Query(ObjectType):
    feeds = DjangoFilterConnectionField(FeedNode)
    feed = relay.Node.Field(FeedNode)
