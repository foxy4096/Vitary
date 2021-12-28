from .models import Vit

def get_latest_vits(request):
    vits = Vit.latest_vits()
    return {'latest_vits': vits}