"""Vitary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
from django.urls import path, include

from apps.accounts.views import profile_view, user_following, user_followers
from apps.feed import api

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),


    # Home
    path('', include('apps.core.urls')),


    # Accounts
    path('accounts/', include('apps.accounts.urls')),


    # Feed
    path('feed/', include('apps.feed.urls')),


    # User
    path('u/<str:username>/', include([
        path('', profile_view, name='profile_view'),
        path('following/', user_following, name='following'),
        path('followers/', user_followers, name='followers')
    ])),


    # Notification
    path('notification/', include('apps.notification.urls')),

    # API
    path('api/v1/like/', api.add_like, name='like_feed'),

    # Blog
    path('blog/', include('apps.blog.urls')),

    # Flatpages
    path('pages/', include('django.contrib.flatpages.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



admin.site.site_header = 'Vitary Admin'
admin.site.site_title = 'Vitary Admin'
admin.site.index_title = 'Vitary Admin'
