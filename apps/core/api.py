from django.http import JsonResponse

def not_authorized(request):
    return JsonResponse({'status':"Not Authorized"})