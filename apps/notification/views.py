from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Notification


@login_required
def notification_page(request):
    return render(request, 'notification/notification_page.html')


@login_required
def notification_redirect(request, pk):
    notification = Notification.objects.get(pk=pk)
    if notification.to_user == request.user.profile:
        notification.is_read = True
        notification.save()
        return redirect(notification.link)
    else:
        return redirect('notification_page')
