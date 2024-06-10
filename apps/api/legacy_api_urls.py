from django.urls import path
from apps.account.api import follow, user_search_api, get_user_avatar
from apps.chat.api import get_message_api, send_message_api
from apps.feed.api import like

urlpatterns = [
    path("users/avatar/<str:username>", get_user_avatar),
    path("feed/like/", like),
    path("follow/", follow),
    path("users/search/", user_search_api),
    path("chat/get_message/", get_message_api),
    path("chat/send_message/", send_message_api),
]
