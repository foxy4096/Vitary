from django.urls import path
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from .models import Post

from . import views

info_dict = {
'queryset': Post.objects.all(),
'date_field': 'date',
}


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name="post_detail"),    
    # the sitemap
    path('sitemap.xml', sitemap,
    {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}},
    name='django.contrib.sitemaps.views.sitemap'),
]
