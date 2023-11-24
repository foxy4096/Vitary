from django.urls import path
from apps.account.api import follow, user_search_api
from apps.chat.api import get_message_api, send_message_api
from apps.feed.api import like

urlpatterns = [
    path("feed/like/", like),
    path("follow/", follow),
    path("users/search/", user_search_api),
    path("chat/get_message/", get_message_api),
    path("chat/send_message/", send_message_api),
]
