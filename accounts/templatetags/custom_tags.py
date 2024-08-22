from django import template
from django.template.defaultfilters import stringfilter
from accounts.models import UserProfile, EmployeeProfileImages
register = template.Library()

@register.simple_tag
@stringfilter
def get_cv_imgs(userprofile_id):
    userprofile = UserProfile.objects.get(id=userprofile_id)
    profile_images = EmployeeProfileImages.objects.filter(user=userprofile.user)

    return profile_images


@register.simple_tag
@stringfilter
def get_viewed_profile(user_id):
    # a = GetViewedProfileSubscriptionData(user_id)
    return 'a'


@register.simple_tag
@stringfilter
def get_sended_msg(user_id):
    # a = GetSendedMsgSubscriptionData(user_id)
    return 'a'

@register.simple_tag
@stringfilter
def get_received_msg(user_id):
    # a = GetReceivedMsgSubscriptionData(user_id)
    return 'a'