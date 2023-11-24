from apps.feed.views import plustag_feeds
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path("admin/", include("loginas.urls")),
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("auth/", include("apps.account.urls")),
    path("feed/", include("apps.feed.urls")),
    path("u/<str:username>/", include("apps.account.user_urls")),
    path("notification/", include("apps.notification.urls")),
    path("plustag/<str:p>/", plustag_feeds, name="plustag_feeds"),
    path("blog/", include("apps.blog.urls")),
    path("chat/", include("apps.chat.urls")),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("api/", include("apps.api.urls")),
    path("api/v1/", include("apps.api.legacy_api_urls")),
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
