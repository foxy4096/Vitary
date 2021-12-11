from django.urls import path
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from .models import Feed

from . import views

info_dict = {
'queryset': Feed.objects.all(),
'date_field': 'created_on',
}

urlpatterns = [
    path('add/', views.add_feed, name='add_feed'),
    path('<int:pk>/', views.feed_detail, name='feed_detail'),
    path('<int:pk>/edit/', views.edit_feed, name='edit_feed'),
    path('<int:pk>/delete/', views.delete_feed, name='delete_feed'),
    path('add_comment/', views.add_comment, name='add_comment'),
    # the sitemap
    path('sitemap.xml', sitemap,
    {'sitemaps': {'feed': GenericSitemap(info_dict, priority=0.6)}},
    name='django.contrib.sitemaps.views.sitemap'),
]