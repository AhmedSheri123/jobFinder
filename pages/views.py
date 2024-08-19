from django.shortcuts import render
from accounts.models import UserProfile
from notifications.views import create_notifications

# Create your views here.

def index(request):
    userprofiles = UserProfile.objects.filter(is_employee=True)
    # u = []
    # for i in userprofiles:
    #     u.append(i.user.id)
    # aa = create_notifications(request.user.id, receiver_ids=u, msg='sadas as daasd a dsa d')
    # print(aa)
    return render(request, 'pages/index.html', {'userprofiles':userprofiles})

def AdvancedSearch(request):
    userprofiles = UserProfile.objects.filter(is_employee=True)
    return render(request, 'pages/AdvancedSearch.html', {'userprofiles':userprofiles})