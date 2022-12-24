from ninja.security import APIKeyHeader

from apps.developer.models import Bot, Token


class UserApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        try:
            return Token.objects.get(token=key).devprofile.user
        except Exception:
            None


class BotApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        try:
            return Bot.objects.get(private_key=key).user
        except Exception:
            None
