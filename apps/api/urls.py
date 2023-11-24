from django.urls import path
from . import views

urlpatterns = [
    path("graphql/", views.VitaryGraphQLView.as_view()),
]
