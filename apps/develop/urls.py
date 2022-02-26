from django.urls import path

from . import api
from . import views

urlpatterns = [
    path('', views.home, name='develop_home'),
    path('dashboard/', views.dashboard, name='develop_dashboard'),
    path('join/', views.join, name='develop_join'),

    # Some API endpoints which are not for developers
    path('api/generate_api_key/', api.generate_api_key, name='develop_generate_api_key'),
    path('api/refresh_api_key/', api.refresh_api_key, name='develop_refresh_api_key'),
    path('api/revoke_api_key/', api.revoke_api_key, name='develop_revoke_api_key'),
    path('api/edit_profile/', api.edit_profile_api, name='develop_edit_profile'),

    # Documentation
    path('docs/', views.DocsIndexView.as_view(), name='develop_docs'),
    path('docs/<str:slug>/', views.DocsDetailView.as_view(), name='develop_docs_detail'),

]