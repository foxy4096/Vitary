from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from .graphql.query import schema


@method_decorator(csrf_exempt, name="dispatch")
class VitaryGraphQLView(GraphQLView):
    graphiql = True
    schema = schema
