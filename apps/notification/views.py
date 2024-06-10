from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.account.models import User
from apps.feed.models import Comment

from .models import Notification
from django.core.paginator import Paginator


@login_required
def notification_page(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by(
        "-created_at"
    )
    paginator = Paginator(notifications, 10)
    page = request.GET.get("page")
    notifications = paginator.get_page(page)
    return render(
        request, "notification/notification.html", {"notifications": notifications}
    )


@login_required
def notification_redirect(request, pk):
    notification = get_object_or_404(Notification, id=pk)
    ntype = notification.object_type
    if notification.recipient != request.user:
        return redirect("notification_page")

    notification.is_read = True
    notification.save()
    if ntype == "chat":
        return redirect("message_user_id", notification.object_id)
    elif ntype in ["comment", "reply"]:
        comment = Comment.objects.only("feed__id", "id").get(id=notification.object_id)
        return redirect("view_comment", comment.feed.id, comment.id)
    elif ntype == "feed":
        return redirect("feed_detail", notification.object_id)
    elif ntype == "user":
        username = User.objects.only("username").get(id=notification.object_id).username
        return redirect("user_detail", username)
    return redirect("home")


@login_required
def mark_all_as_read(request):
    user_notifications = Notification.objects.filter(recipient=request.user)
    for user_notification in user_notifications:
        user_notification.is_read = True
        user_notification.save()

    messages.success(request, "All the notifications have been marked as read!")
    return redirect("notification_page")
