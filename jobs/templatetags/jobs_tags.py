from django import template
from django.template.defaultfilters import stringfilter
from jobs.models import JobAppliersModel, JobsModel

register = template.Library()

@register.simple_tag
@stringfilter
def get_number_of_apllyers(job_id):
    count = JobAppliersModel.objects.filter(job__id=job_id).count()

    return count

@register.simple_tag
@stringfilter
def get_number_of_accepted_apllyers(job_id):
    count = JobAppliersModel.objects.filter(job__id=job_id, state='2').count()

    return count