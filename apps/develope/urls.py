from django.urls import path

from . import views

urlpatterns = [
    path('', views.develope_home, name='develope_home'),
    path('join/', views.join_us, name='join_us'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.dev_profile, name='dev_profile'),

    # Documentation
    path('start/', views.get_started, name='get_started'),
    path('docs/', views.documentation, name='documentation'),
    path('docs/<slug:tag>/', views.documentation_tag, name='documentation_tag'),
    path('docs/<slug:tag>/<slug:title>/', views.documentation_detail, name='documentation_detail'),
]