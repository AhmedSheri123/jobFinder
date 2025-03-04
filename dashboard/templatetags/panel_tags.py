from django import template
# from accounts.models import CompanyCreateJobModel, EmployeeJobRequest
import json
from django.conf import settings
from dashboard.views import get_permission_state
from accounts.models import UserSubscriptionModel

register = template.Library()

@register.simple_tag
def temp_get_permission_state(user_id, url, method):
    p = get_permission_state(user_id, url, method)
    
    return p

@register.simple_tag
def json_to_html(json):
    # for el in json:
    p = ', '.join(json.get('desires', []))
    
    return p

@register.simple_tag
def get_user_subs(sub_id):
    s = UserSubscriptionModel.objects.filter(subscription__id=sub_id)
    for i in s:
        if not i.is_has_subscription:
            s = s.exclude(id=i.id)
    return s


# @register.simple_tag
# def NumberOfPresenters(job_id):
#     presenters = EmployeeJobRequest.objects.filter(company_job__id=job_id)
#     count = str(presenters.count())
#     return count

# @register.simple_tag
# def AcceptedOfPresenters(job_id):
#     presenters = EmployeeJobRequest.objects.filter(post_state='3', company_job__id=job_id)
#     count = str(presenters.count())
#     return count


# @register.simple_tag
# def GenFooter(job_id):
#     html = open(settings.BASE_DIR / 'media/footer.json', 'r', encoding='utf-8').read()
#     loaded = json.loads(html)
#     return loaded