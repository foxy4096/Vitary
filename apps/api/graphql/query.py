import graphene

from .user.schema import Query as UserQuery
from .feed.schema import Query as FeedQuery


class Query(UserQuery, FeedQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
