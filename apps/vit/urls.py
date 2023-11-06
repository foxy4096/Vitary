from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_vit, name='add_vit'),
    path('<int:pk>/', views.vit_detail, name='vit_detail'),
    path('<int:pk>/edit/', views.edit_vit, name='edit_vit'),
    path('<int:pk>/delete/', views.delete_vit, name='delete_vit'),
    path('<int:vit_pk>/likes/', views.vit_liked_users, name='vit_liked_users'),
    path('<int:vit_pk>/comment/view/<int:pk>/', views.view_comment, name='view_comment'),
    path("comment/_form/", views._comment_form, name="_comment_form"),
    path("comment/_refresh/<int:pk>/", views._comment_refresh, name="_comment_refresh")
]
