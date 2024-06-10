import graphene
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from django.urls import reverse
from apps.feed.forms import FeedForm
from django.conf import settings
from apps.feed.models import Feed


class FeedNode(DjangoObjectType):
    has_user_liked = graphene.Boolean()
    comments_count = graphene.Int()
    raw_id = graphene.Int(source="id")
    web_url = graphene.String()

    class Meta:
        model = Feed
        filter_fields = ("body", "id")
        interfaces = (graphene.relay.Node,)

    def resolve_raw_id(self, info):
        return self.raw_id


    def resolve_comments_count(self, info):
        return self.comment_set.count()


    def resolve_feed(self, info, raw_id):
        return Feed.objects.get(pk=raw_id)

    def resolve_web_url(self, info):
        return f"{settings.WEB_HOST}" + reverse("feed_detail", kwargs={"pk": self.id})

    def resolve_has_user_liked(self, info):
        # Access the authenticated user from info.context.user
        user = info.context.user

        # Check if the user has liked this feed
        return self.likes.filter(id=user.id).exists()


class LikeFeedMutation(graphene.Mutation):
    class Arguments:
        feed_id = graphene.ID(required=True)

    success = graphene.Boolean()
    feed = graphene.Field(FeedNode)

    def mutate(self, info, feed_id):
        # Access the authenticated user from info.context.user
        user = info.context.user

        try:
            # Get the feed by ID
            feed = Feed.objects.get(pk=feed_id)

            # Call the like_feed method to handle liking/unliking
            feed.like_feed(user)

            return LikeFeedMutation(success=True, feed=feed)
        except Feed.DoesNotExist:
            return LikeFeedMutation(success=False, feed=None)


class FeedMutation(DjangoModelFormMutation):
    feed = graphene.Field(FeedNode)

    class Meta:
        form_class = FeedForm

    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        # Access the authenticated user from info.context.user
        user = info.context.user

        # Set the user before saving the form
        form.instance.user = user

        if form.is_valid():
            # Save the form and return the created instance
            instance = form.save()
            return cls(feed=instance)
        else:
            raise graphene.GraphQLError("Form validation error")


class Query(graphene.ObjectType):
    feeds = DjangoFilterConnectionField(FeedNode)
    feed = graphene.relay.Node.Field(FeedNode)
