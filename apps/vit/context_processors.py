from .models import Vit
from .forms import VitForm

def get_latest_vits(request):
    vits = Vit.latest_vits()
    random_vit = Vit.objects.order_by("?").first()
    return {'latest_vits': vits, 'random_vit': random_vit}

def vit_form(request):
    vit_form = VitForm()
    return {'vit_form': vit_form}
