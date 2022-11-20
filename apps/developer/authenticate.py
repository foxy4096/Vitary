from ninja.security import APIKeyHeader

from .models import Token, Bot

class UserApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        try:
            return Token.objects.get(token=key).devprofile.user
        except:
            None


class BotApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        try:
            return Bot.objects.get(private_key=key).user
        except:
            None