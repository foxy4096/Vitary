from django.contrib.auth.models import User
from .models import DevProfile
from django.contrib.auth import login


def get_authorization_key(request):
    """
    Get the Authorization Key from the request
    """
    auth = request.headers.get('Authorization')
    if auth:
        auth = auth.split()
        if len(auth) == 2:
            if auth[0].lower() == 'key':
                return auth[1]
    return None



class KeyBackend:
    """
    Simple Key Based authentication
    Authorization header should be in the format:
    Authorization: Key <private_key>
    """
   
    def authenticate(self, request, **kwargs):
        """
        Authenticate the user with the given key
        """
        key = get_authorization_key(request)

        if key:
            try:
                user = User.objects.get(devprofile__private_key=key) if User.objects.filter(devprofile__private_key=key).exists() else User.objects.get(bot__private_key=key)
                login(request, user)
                return user
            except User.DoesNotExist:
                return None
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
