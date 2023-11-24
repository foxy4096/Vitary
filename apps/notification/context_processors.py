from apps.notification.models import Notification


def get_notification_info(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(receiver=request.user, is_read=False).count()
        return {"notification_count": count}
    return {"notification_count": 0}
