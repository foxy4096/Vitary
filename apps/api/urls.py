from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="api-index"),
    path("graphql/", views.VitaryGraphQLView.as_view()),
    path("health/", views.health_check),
    path("echo/", views.echo),
    path("action/signup/check/", views.signup_validate),
    path("action/like/", views.like),
]
