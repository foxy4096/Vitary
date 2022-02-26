import json
import os
from django.http import JsonResponse

def zen(request):
    module_dir = os.path.dirname(__file__)
    zen_txt = open(os.path.join(module_dir, 'zen.txt')).read()
    return JsonResponse({'zen': zen_txt})