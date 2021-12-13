from .models import Notification


def notification(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            to_user=request.user, is_read=False)
        notifications = Notification.objects.filter(
            to_user=request.user).order_by('is_read', '-date')
        return {'unread_notifications': unread_notifications, 'notifications': notifications}
    else:
        return {}
