from django.utils import timezone
import math, requests, json
from django.contrib.auth.models import User
from django.conf import settings
from .whatsapp import wa_send_msg
from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.utils import timezone
from .fields import dialCode
import re, string

email_from = settings.EMAIL_HOST_USER

def phoneCleaner(phone=''):
    if phone:
        phone = ''.join([n for n in phone if n.isdigit()])
        if phone:
            phone = str(int(phone))
            return phone
    else:return ''

def DatetimeNow(user):
    datetime_now = timezone.now()
    return datetime_now


def when_published(creation_date):
    if not creation_date:
        return ''

    now = timezone.now()
    
    diff= now - creation_date

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        seconds= diff.seconds
        
        if seconds == 1:
            return str(seconds) + " ثانية"
        
        else:
            return str(seconds) + " ثواني"

        

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        minutes= math.floor(diff.seconds/60)

        if minutes == 1:
            return str(minutes)  + " دقيقة"
        
        else:
            return str(minutes)  + " دقيقة"



    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        hours= math.floor(diff.seconds/3600)

        if hours == 1:
            return str(hours) + " ساعة"

        else:
            return str(hours) + " ساعات"

    # 1 day to 30 days
    if diff.days >= 1 and diff.days < 30:
        days= diff.days
    
        if days == 1:
            return str(days) + " يوم"

        else:
            return str(days) + " ايام"

    if diff.days >= 30 and diff.days < 365:
        months= math.floor(diff.days/30)
        

        if months == 1:
            return str(months) + " شهر"

        else:
            return str(months) + " اشهر"


    if diff.days >= 365:
        years= math.floor(diff.days/365)

        if years == 1:
            return str(years) + " سنة"

        else:
            return str(years) + " سنوات"


def get_ip_info(ip):
    if ip == '127.0.0.1':
        ip = '185.255.46.235'
        
    u = f'https://proxycheck.io/v2/{ip}?vpn=1&asn=1'
    r = requests.get(u)
    j = r.json()
    jj = j.get(ip)

    
    if j.get('status'):
        proxy = False
        
        if jj.get('proxy') != 'no':
            proxy = True
        obj = {
            'ip':ip,
            'country':jj.get('country'),
            'isocode':jj.get('isocode'),
            'country':jj.get('country'),
            'continent':jj.get('continent'),
            'continentcode':jj.get('continentcode'),
            'vpn': proxy,
        }

        return obj
    else:
        return {}


def add_get_user_ip(request):
    ip = request.META.get('REMOTE_ADDR')
    ip_info = None
    str_ip_info = request.session.get('ip_info')
    if str_ip_info:
        ip_info = json.loads(str_ip_info)

    if not ip_info:
        ip_info = get_ip_info(ip)
        if ip_info:
            request.session['ip_info'] = json.dumps(ip_info)
    else:
        if ip_info.get('vpn'):
                ip_info = get_ip_info(ip)
    return ip_info

def filter_sub_price(request, subs):
    from .models import SubscriptionPriceByCountry as SubsPriceByCountry

    user = request.user
    phone_country_code = None

    if user.is_authenticated:

        userprofile = user.userprofile
        if userprofile.is_employee:phone_country_code=userprofile.employeeprofile.phone_country_code
        else:phone_country_code=userprofile.companyprofile.phone_country_code
        
    else:
        ip_info = add_get_user_ip(request)
        if ip_info:
            phone_country_code = ip_info.get('isocode')

    if phone_country_code:
        

        phone_country_code = phone_country_code.upper()
        subsc = SubsPriceByCountry.objects.filter(country__name = phone_country_code)

        for sub in subs:
            sub_subsc = subsc.filter(subscription=sub)
            if not sub_subsc.exists():
                if not sub.is_default_Subscription:
                    subs = subs.exclude(set_defult_price=False, id=sub.id)

        for sub in subs:
            sub_subsc = subsc.filter(subscription=sub)
            if sub_subsc.exists():
                subc = sub_subsc.first()
                sub.price = subc.price
                sub.currency = subc.currency
                
    return subs



def create_notifications(sender_id, receiver_ids=[], msg=''):
    from accounts.models import NotificationsModel

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


def get_user_img(user):
    from accounts.models import EmployeeProfileImages

    employee_images = EmployeeProfileImages.objects.filter(user=user)
    employee_image = ''
    if employee_images.exists():
        employee_image = employee_images.first().img_base64

    img = []
    if user.userprofile.is_employee:
        if employee_image:
            img = [employee_image, 0]
        else:
            img = ['', 1]
    elif user.userprofile.is_company:
        if user.userprofile.companyprofile.img_base64:
            img = [user.userprofile.companyprofile.img_base64, 0]
        else:
            img = ['', 1]
    else:
        img = ['', 1]
    return img


def send_msg_email_phone_noti(subject, msg, sender_id, receiver_ids):
    if not msg:return
    receivers = User.objects.filter(id__in=receiver_ids)
    for receiver in receivers:
        userprofile = receiver.userprofile
        email = receiver.email
        phone = None
        dial_code = None
        if userprofile.is_employee:phone=userprofile.employeeprofile.phone;dial_code=get_dial_code_by_country_code(userprofile.employeeprofile.phone_country_code)
        else:phone=userprofile.companyprofile.phone;dial_code=get_dial_code_by_country_code(userprofile.companyprofile.phone_country_code)
        send_mail(subject, msg, email_from, [email] )
        wa_send_msg(msg, phone, dial_code)
    create_notifications(sender_id, receiver_ids, msg)


def get_dial_code_by_country_code(country_code='', without_plus=False):
    if country_code:
        country_code = country_code.upper()
        for dial in dialCode:
            if dial['code'] == country_code:
                dial_code = dial['dial_code']
                if without_plus:
                    dial_code = dial_code.replace('+', '')
                return dial_code
    return ''


def extract_urls(text):
    pattern = r"((((https?|ftps?|gopher|telnet|nntp)://)|(mailto:|news:))([-%()_.!~*';/?:@&=+$,A-Za-z0-9])+)"
    regex = re.compile(pattern)
    matches = regex.findall(text)
    return matches

def extract_soshial_profile_url(user_or_url='', type=''):
    result = ''
    if user_or_url:
        user_or_url = user_or_url.replace('@', '')

        matches = extract_urls(user_or_url)
        if not matches:
            urls = {
                'snapchat': 'https://www.snapchat.com/add/{username}',
                'tiktok': 'https://www.tiktok.com/@{username}',
                'instgram': 'https://www.instagram.com/{username}',
                'facebook': 'https://www.facebook.com/{username}',
                'linkedin': 'https://www.linkedin.com/in/{username}',
            }
            if type in urls:
                result = urls[type].format(username=user_or_url)
            elif type == 'whatsapp':
                result = 'https://wa.me/{phone}'.format(phone=phoneCleaner(user_or_url))
        else:result=user_or_url
    
    return result


def filter_job_msg(msg=''):
    if msg:
        words = ['واحد', 'اثنان', 'ثلاثة', 'اربعة', 'خمسة', 'ستة', 'سبعة', 'ثمانية', 'تسعة', 'صفر']
        urls = extract_urls(msg)
        digits = [i for i in string.digits]

        for ban in words:
            ban_msg = ''.join(['*' for i in range(0, len(ban))])
            msg = msg.replace(ban, f' "{ban_msg}" ')

        for ban in urls:
            url = ban[0]
            print(url)
            msg = msg.replace(url, ' "حذفت الرابط من قبل النظام" ')

        for ban in digits:
            msg = msg.replace(ban, '*')
    
        return msg
    
    return ''