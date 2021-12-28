from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_vit, name='add_vit'),
    path('<int:pk>/', views.vit_detail, name='vit_detail'),
    path('<int:pk>/edit/', views.edit_vit, name='edit_vit'),
    path('<int:pk>/delete/', views.delete_vit, name='delete_vit'),
]
