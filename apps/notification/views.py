from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Notification
from django.core.paginator import Paginator



@login_required
def notification_page(request):
    notifications = Notification.objects.filter(receiver=request.user)
    paginator = Paginator(notifications, 10)
    page = request.GET.get('page')
    notifications = paginator.get_page(page)
    return render(request, 'notification/notification.html', {'notifications': notifications})


@login_required
def notification_redirect(request, pk):
    notification = get_object_or_404(Notification, id=pk)
    if notification.to_user != request.user:
        return redirect('notification_page')
    notification.is_read = True
    notification.save()
    return redirect(notification.link)

@login_required
def mark_all_as_read(request):
    user_notifications = Notification.objects.filter(to_user=request.user)
    for user_notification in user_notifications:
        user_notification.is_read = True
        user_notification.save()

    messages.success(request, 'All the notifications have been marked as read!')
    return redirect('notification_page')