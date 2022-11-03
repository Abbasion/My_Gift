from my_Gift_app.Models.Nitifications.notifications import Notifications


def get_notification_by_Id(Id):
    try:

        noti = Notifications.objects.select_related("notification_by").get(pk=Id,isDeleted=False)
        return noti
    except:
        return None

def get_notification_by_User_Id(notification_by):
    try:
        noti=Notifications.objects.select_related("notification_by").filter(isDeleted=False,notification_by=notification_by)
        print(noti)
        return noti
    except:
        return None