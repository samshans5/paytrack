from bills.models import Notification


def notification_context(request):
    if request.user.is_authenticated:
        unread = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        unread = 0
    return {"unread_notifications": unread}
