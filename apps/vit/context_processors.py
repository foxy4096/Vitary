from .models import Vit
from .forms import VitForm

def get_latest_vits(request):
    vits = Vit.latest_vits()
    return {'latest_vits': vits}

def vit_form(request):
    vit_form = VitForm()
    return {'vit_form': vit_form}