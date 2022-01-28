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
from apps.vit.api import add_like


urlpatterns = [
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
    path('api/v1/vit/add_like/', add_like),
    path('api/v1/chat/get_message/', get_message_api),
    path('api/v1/chat/send_message/', send_message_api),


    # Plustag
    path('p/<str:p>/', plustag_vits, name='plustag_vits'),
    

    # Blog
    path('blog/', include('apps.blog.urls')),


    # Chat
    path('c/', include('apps.chat.urls')),

    # Flatpages
    path('pages/', include('django.contrib.flatpages.urls')),
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
