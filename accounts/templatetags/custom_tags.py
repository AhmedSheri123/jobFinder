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