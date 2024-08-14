from django import template
from django.template.defaultfilters import stringfilter
from messenger.models import MessagesModel, MessengerModel
from messenger.views import get_user_img
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
@stringfilter
def get_messengers(user_id):
    messengers = MessengerModel.objects.filter(messenger_users__id__in=[user_id])

    return messengers

@register.simple_tag
@stringfilter
def get_last_msg(messenger_id):
    messenger = MessengerModel.objects.get(id = messenger_id)
    messages = MessagesModel.objects.filter(messenger=messenger)
    if messages.exists():
        return messages.order_by('-id').first().msg.replace('\n', '')
    return ''

@register.simple_tag
@stringfilter
def get_user_profile_img(user_id):
    user = User.objects.get(id=user_id)
    img = get_user_img(user)

    return img

@register.simple_tag
@stringfilter
def get_receiver_user(sender_id, room_id):
    messenger = MessengerModel.objects.get(room_id=room_id)
    receiver = messenger.messenger_users.exclude(id=sender_id).first()

    return receiver