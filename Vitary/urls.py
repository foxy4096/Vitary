from apps.accounts.api import follow, user_search_api
from apps.accounts.views import profile, user_followers, user_following, user_image
from apps.chat.api import get_message_api, send_message_api
from apps.developer.api import api
from apps.vit.api import like
from apps.vit.views import plustag_vits
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", include("loginas.urls")),
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("auth/", include("apps.accounts.urls")),
    path("vit/", include("apps.vit.urls")),
    path(
        "u/<str:username>/",
        include(
            [
                path("", profile, name="user_detail"),
                path("following/", user_following, name="following"),
                path("followers/", user_followers, name="followers"),
                path("image/", user_image, name="image"),
            ]
        ),
    ),
    path("notification/", include("apps.notification.urls")),
    path("api/v1/vit/like/", like),
    path("api/v1/follow/", follow),
    path("api/v1/users/search/", user_search_api),
    path("api/v1/chat/get_message/", get_message_api),
    path("api/v1/chat/send_message/", send_message_api),
    path("developer/", include("apps.developer.urls")),
    path("plustag/<str:p>/", plustag_vits, name="plustag_vits"),
    path("blog/", include("apps.blog.urls")),
    path("chat/", include("apps.chat.urls")),
    path("api/", api.urls),
    path("pages/", include("django.contrib.flatpages.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
]
