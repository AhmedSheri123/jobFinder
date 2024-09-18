from django import template
from django.template.defaultfilters import stringfilter
from jobs.models import JobAppliersModel, JobsModel
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
@stringfilter
def get_number_of_apllyers(job_id):
    count = JobAppliersModel.objects.filter(job__id=job_id).count()

    return count

@register.simple_tag
@stringfilter
def is_user_apllied(job_id, user_id):
    user = User.objects.get(id=user_id)
    count = JobAppliersModel.objects.filter(job__id=job_id, user=user)

    return count.exists()

@register.simple_tag
@stringfilter
def get_number_of_accepted_apllyers(job_id):
    count = JobAppliersModel.objects.filter(job__id=job_id, state='2').count()

    return count