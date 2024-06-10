from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from .utils import check_database_health, check_migrations

from apps.feed.models import Feed

from .graphql.query import schema
from apps.account.models import User
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "api/index.html")

@method_decorator(csrf_exempt, name="dispatch")
class VitaryGraphQLView(GraphQLView):
    graphiql = True
    pretty = True
    schema = schema


def health_check(request):
    database_check = check_database_health()
    migrations_check = check_migrations()
    return JsonResponse(
        {
            "database": database_check,
            "migrations": migrations_check,
            "status": "ok" if database_check and migrations_check else "error",
            "message": "Database and migrations are healthy"
            if database_check and migrations_check
            else "Database or migrations are not healthy",
            "version": "1.0.0",
        }
    )


def echo(request, *args, **kwargs):
    return JsonResponse(
        {
            **request.GET.dict(),
            **request.POST.dict(),
        }
    )


def signup_validate(request):
    """
    Check if the user can create an account with the provided credentials
    """

    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"}, status=400
        )

    if username := request.POST.get("username"):
        return (
            JsonResponse(
                {"status": "error", "message": "Username already exists"},
                status=400,
            )
            if User.objects.filter(username=username).exists()
            else JsonResponse({"status": "ok", "valid": True})
        )
    else:
        return JsonResponse(
            {"status": "error", "message": "Username is required"},
            status=400,
        )


@login_required
def like(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request method"})
    if feed_id := request.POST.get("feed_id"):
        feed = Feed.objects.get(id=feed_id)
        feed.like_feed(request.user)
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid feed id"})
