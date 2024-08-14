from django.shortcuts import render
from accounts.models import UserProfile
# Create your views here.

def index(request):
    userprofiles = UserProfile.objects.filter(is_employee=True)

    return render(request, 'pages/index.html', {'userprofiles':userprofiles})