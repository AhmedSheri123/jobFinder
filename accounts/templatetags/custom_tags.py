from django import template
from django.template.defaultfilters import stringfilter
from accounts.models import UserProfile, EmployeeProfileImages, UserLikeModel, UserViewedProfileModel, AdminADSModel
from django.conf import settings
import random, json

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

@register.simple_tag
@stringfilter
def get_user_likes(user_id):
    a = UserLikeModel.objects.filter(liked__id=user_id).count()
    return a

@register.simple_tag
@stringfilter
def get_user_views(user_id):
    a = UserViewedProfileModel.objects.filter(profile_viewed__id=user_id).count()
    return a

@register.simple_tag
@stringfilter
def get_ws_type(ss):
    a = settings.WS_TYPE
    return a

@register.simple_tag
@stringfilter
def get_sub_price(req):
    print(req)

@register.simple_tag
@stringfilter
def get_random_ad_cv(ip_info):
    if ip_info:
        ip_info = json.loads(ip_info)
        ads = AdminADSModel.objects.filter(is_enabled=True, show_in_cv=True)
        for ad in ads:
            if ad.reminding_days() <= 0:
                ads = ads.exclude(id=ad.id)

            elif not ad.show_on_all_countrys:
                if ad.country!=ip_info.get('isocode'):
                    ads = ads.exclude(id=ad.id)
        if ads:
            ad = random.choice(ads)
            return ad
    return {}

@register.simple_tag
@stringfilter
def get_random_ad_main(ip_info):
    if ip_info:
        ip_info = json.loads(ip_info)
        ads = AdminADSModel.objects.filter(is_enabled=True, is_main_ad=True)
        for ad in ads:

            if ad.reminding_days() <= 0:
                ads = ads.exclude(id=ad.id)
            elif not ad.show_on_all_countrys:
                

                if ad.country!=ip_info.get('isocode'):
                    ads = ads.exclude(id=ad.id)
        if ads:
            ad = random.choice(ads)
            return ad
    return {}

@register.simple_tag
@stringfilter
def get_random_ad_others(ip_info):
    if ip_info:
        ip_info = json.loads(ip_info)
        ads = AdminADSModel.objects.filter(is_enabled=True, show_in_others=True)
        for ad in ads:
            if ad.reminding_days() <= 0:
                ads = ads.exclude(id=ad.id)
            elif not ad.show_on_all_countrys:
                if ad.country!=ip_info.get('isocode'):
                    ads = ads.exclude(id=ad.id)
        if ads:
            ad = random.choice(ads)
            return ad
    return {}