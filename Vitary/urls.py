from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve


from django.contrib import admin
from django.urls import path, include

from apps.accounts.views import profile_view, user_following, user_followers
from apps.vit.views import plustag_vits

# APIs
from apps.chat.api import get_message_api, send_message_api
from apps.core.api import not_authorized, get_routes
from apps.vit.api import add_like, vit_list, get_vit, edit_vit, add_vit, delete_vit
from apps.accounts.api import get_user_info, get_users
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # PWA
    path('', include('pwa.urls')),


    # Admin
    path('admin/', admin.site.urls),


    # Home
    path('', include('apps.core.urls')),


    # Accounts
    path('accounts/', include('apps.accounts.urls')),


    # Vit
    path('vit/', include('apps.vit.urls')),


    # User
    path('u/<str:username>/', include([
        path('', profile_view, name='profile_view'),
        path('following/', user_following, name='following'),
        path('followers/', user_followers, name='followers')
    ])),


    # Notification
    path('notification/', include('apps.notification.urls')),

    # API
    path('api/v1/', include([
        path('', get_routes),
        path('chat/', include([
            path('get_message/', get_message_api),
            path('send_message/', send_message_api),
        ])),
        path('vit/', include([
            path('', vit_list),
            path('add_like/', add_like),
            path('<int:vit_pk>/', get_vit),
            path('add/', add_vit),
            path('<int:vit_pk>/edit/', edit_vit),
            path('<int:vit_pk>/delete/', delete_vit),
        ])),
        path('u/', include([
            path('', get_users, name='get_users'),
            path('<str:username>/', get_user_info, name='get_user_info'),
        ])),
        path('not_authorized/', not_authorized, name='not_authorized'),
        path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    ])),

    # Plustag
    path('p/<str:p>/', plustag_vits, name='plustag_vits'),
    

    # Blog
    path('blog/', include('apps.blog.urls')),

    # Flatpages
    path('pages/', include('django.contrib.flatpages.urls')),

    # Chat
    path('chat/', include('apps.chat.urls')),

    # Developer
    path('develope/', include('apps.develope.urls')),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# I am poor so I can afford a media server like Amazon S3 Bucket
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
            }),
]

admin.site.site_header = 'Vitary Admin'
admin.site.site_title = 'Vitary Admin'
admin.site.index_title = 'Vitary Admin'
