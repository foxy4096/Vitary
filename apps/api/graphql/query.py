import graphene
from graphene_django.debug import DjangoDebug
import graphql_jwt


from .user.schema import Query as UserQuery
from .feed.schema import Query as FeedQuery
from .feed.schema import FeedMutation, LikeFeedMutation


class Query(UserQuery, FeedQuery, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')
    feed_mutation = FeedMutation.Field()
    like_feed = LikeFeedMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
