from django.shortcuts import render
from messenger.views import get_user_img
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from accounts.models import NotificationsModel
from django.utils import timezone

# Create your views here.

def create_notifications(sender_id, receiver_ids=[], msg=''):

    sender = User.objects.get(id=sender_id)
    receivers = User.objects.filter(id__in=receiver_ids)

    sender_img_profile = get_user_img(sender)

    noti = NotificationsModel.objects.create(sender=sender, msg=msg)
    noti.creation_date = timezone.now()
    toastID = noti.id
    
    for receiver in receivers:
        noti.receiver.add(receiver)
        channel_layer = get_channel_layer()
        receiver_room_id = f'notifications_{str(receiver.id)}'

        async_to_sync(channel_layer.group_send)(
            receiver_room_id,
            {
                'type': 'showToast',
                'method':'showToast',
                'toastID':toastID,
                'username': sender.username,
                'message': msg,
                'img': sender_img_profile[0],

            }
        )

    noti = noti.save()
    return noti

