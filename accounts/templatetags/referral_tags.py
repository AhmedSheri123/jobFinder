from django import template
from accounts.models import UserProfile, ReferralLinkModel

register = template.Library()

@register.simple_tag
def get_referral_user_signin_count(referral_id):
      count = UserProfile.objects.filter(referral__id=referral_id).count()

      return count