# Some thingies for media and static files
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

# Some thingies for admin
from django.contrib import admin

# Some thingies for urls
from django.urls import path, include


from apps.accounts.views import profile, user_following, user_followers, user_image
from apps.vit.views import plustag_vits

# APIs
from apps.chat.api import get_message_api, send_message_api
from apps.accounts.api import follow, user_search_api
from apps.vit.api import like

from apps.developer.api import api

urlpatterns = [
    # Admin
    path('admin/', include('loginas.urls')),
    path('admin/', admin.site.urls),



    # Home
    path('', include('apps.core.urls')),


    # Accounts
    path('auth/', include('apps.accounts.urls')),


    # Vit
    path('vit/', include('apps.vit.urls')),


    # User
    path('u/<str:username>/', include([
        path('', profile, name='profile_view'),
        path('following/', user_following, name='following'),
        path('followers/', user_followers, name='followers'),
        path('image/', user_image, name='image'),       
    ])),


    # Notification
    path('notification/', include('apps.notification.urls')),


    path('api/v1/vit/like/', like),
    path('api/v1/follow/', follow),
    path('api/v1/users/search/', user_search_api),
    path('api/v1/chat/get_message/', get_message_api),
    path('api/v1/chat/send_message/', send_message_api),


    # Developer
    path('developer/', include('apps.developer.urls')),

    # Plustag
    path('plustag/<str:p>/', plustag_vits, name='plustag_vits'),


    # Blog
    path('blog/', include('apps.blog.urls')),


    # Chat
    path('chat/', include('apps.chat.urls')),

    # API
    path('api/', api.urls),

    # Flatpages
    path('pages/', include('django.contrib.flatpages.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# I am poor so I can afford a media server like Amazon S3 Bucket
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
            }),
            
]

admin.site.site_header = 'Vitary Administrative Dashboard'
admin.site.site_title = 'Vitary Administrative Dashboard'
admin.site.index_title = 'Vitary Administrative Dashboard'
