from django.utils import timezone
import math, requests, json


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
    
    ip_info = add_get_user_ip(request)


    if not ip_info:
        return subs
    
    subsc = SubsPriceByCountry.objects.all()

    for sub in subs:
        for subc in subsc:
            if sub == subc.subscription:
                if subc.country.name == ip_info.get('isocode'):
                    sub.price = subc.price
                    sub.currency = subc.currency
    return subs