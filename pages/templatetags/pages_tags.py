from django import template
# from accounts.models import CompanyCreateJobModel, EmployeeJobRequest
import json
from django.conf import settings
from dashboard.views import get_permission_state
from dashboard.models import GeneralSettingsModel
register = template.Library()

@register.simple_tag
def get_general_setting():
    _settings = GeneralSettingsModel.objects.filter()
    if _settings.exists():
        return _settings.first()
    
    return ''