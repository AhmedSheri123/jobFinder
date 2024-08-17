from django import template
from django.template.defaultfilters import stringfilter
from accounts.models import NotificationsModel
from messenger.views import get_user_img
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
@stringfilter
def get_notifications(user_id):
    notifications = NotificationsModel.objects.filter(receiver__id__in=[user_id]).order_by('-id')

    return notifications

@register.simple_tag
@stringfilter
def get_user_profile_img(user_id):
    user = User.objects.get(id=user_id)
    img = get_user_img(user)

    return img