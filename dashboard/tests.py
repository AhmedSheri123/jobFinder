from django.test import TestCase
import re
# Create your tests here.

def extract_soshial_profile_url(user_or_url='', type=''):
    result = ''
    if user_or_url:
        user_or_url = user_or_url.replace('@', '')
        pattern = r"((((https?|ftps?|gopher|telnet|nntp)://)|(mailto:|news:))([-%()_.!~*';/?:@&=+$,A-Za-z0-9])+)"
        regex = re.compile(pattern)

        matches = regex.findall(user_or_url)
        if not matches:
            urls = {
                'snapchat': 'https://www.snapchat.com/add/{username}',
                'tiktok': 'https://www.tiktok.com/@{username}',
                'instgram': 'https://www.instagram.com/{username}/',
                'facebook': 'https://www.facebook.com/{username}/',
                'linkedin': 'https://www.linkedin.com/in/{username}/',
            }
            if type in urls:
                result = urls[type].format(username=user_or_url)
        else:result=user_or_url
    
    return result
print(extract_soshial_profile_url('adsdd', 'facebook'))

