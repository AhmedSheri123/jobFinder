from celery import shared_task
from .models import SendNotifications, CountrysModel
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from .libs import send_msg_email_phone_noti

email_from = settings.EMAIL_HOST_USER
@shared_task
def send_noti_task(sender_id, title, msg, country, send_local, send_by_email, send_by_whatsapp):
    
    receivers = User.objects.filter()
    sender = User.objects.get(id=sender_id)
    
    noti = SendNotifications.objects.create()
    noti.title = title
    noti.msg = msg
    if country:
        noti.country = CountrysModel.objects.get(id=country)
        users = users.filter(Q(userprofile__employeeprofile__country=country) | Q(userprofile__companyprofile__country=country))
    noti.send_local = send_local
    noti.send_by_email = send_by_email
    noti.send_by_whatsapp = send_by_whatsapp
    noti.save()
    receivers_ids = [user.id for user in receivers]
    send_msg_email_phone_noti(title, msg, sender, receivers_ids, send_local, send_by_email, send_by_whatsapp, noti)
    return True