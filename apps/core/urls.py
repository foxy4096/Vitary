from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirect_to_home),
    path('home/', views.home, name='home'),
    path('peoples/', views.peoples, name='peoples'),
    path('explore/', views.explore, name='explore'),
    path('report/<int:pk>/', views.report_abuse, name='report_abuse'),
]
