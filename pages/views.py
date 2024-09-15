from django.shortcuts import render, redirect
from accounts.models import UserProfile, EmployeeProfile, CountrysModel, SubscriptionsModel, AdminADSModel, NationalityModel, HealthStatusModel
from accounts.fields import CertTypeFields, GenderFields, StateFields, NationalityFields
from accounts.libs import filter_sub_price
from .models import ContactUsModel
from django.contrib import messages
from django.utils import timezone
from accounts.libs import add_get_user_ip
import random
import datetime, json
from django.conf import settings
# Create your views here.
BASE_DIR = settings.BASE_DIR

def index(request):
    user_ip = add_get_user_ip(request)
    nationalitys = NationalityModel.objects.all()
    countrys = CountrysModel.objects.all()
    userprofiles = UserProfile.objects.filter(is_employee=True, cv_signup_process='6')
    subscriptions = filter_sub_price(request, SubscriptionsModel.objects.all())

    # u = []
    # for i in userprofiles:
    #     u.append(i.user.id)
    # aa = create_notifications(request.user.id, receiver_ids=u, msg='sadas as daasd a dsa d')
    # print(aa)
    return render(request, 'pages/index.html', {'userprofiles':userprofiles, 'subscriptions':subscriptions, 'countrys':countrys, 'GenderFields':GenderFields, 'nationalitys':nationalitys, 'user_ip':user_ip})


def Subscriptions(request):
    subscriptions = filter_sub_price(request, SubscriptionsModel.objects.all())
    return render(request, 'Subscription/index.html', {'subscriptions':subscriptions})


def AdvancedSearch(request):
    healthes_status = HealthStatusModel.objects.all()
    nationalitys = NationalityModel.objects.all()
    userprofiles = UserProfile.objects.filter(is_employee=True, cv_signup_process='6')
    employee_profile = EmployeeProfile.objects.all()
    countrys = CountrysModel.objects.all()

    desires = request.GET.get('desires')
    cert_type = request.GET.get('cert_type')
    major = request.GET.get('major')
    nationality = request.GET.get('nationality')
    country = request.GET.get('country')
    employee_city = request.GET.get('employee_city')
    gender = request.GET.get('gender')
    marital_status = request.GET.get('marital_status')
    
    if desires:
        filtered = []
        for i in userprofiles:
            emp = i.employeeprofile
            if emp:
                field = emp.desires.get('desires')
                if field:
                    if desires in str(field):
                        filtered.append(i.id)
        userprofiles = userprofiles.filter(id__in=filtered)
    else:desires=''

    if major:userprofiles = userprofiles.filter(employeeprofile__major__contains=major)
    else:major=''

    if employee_city:userprofiles = userprofiles.filter(employeeprofile__employee_city__contains=employee_city)
    else:employee_city=''

    if cert_type:userprofiles = userprofiles.filter(employeeprofile__cert_type=cert_type)
    else:cert_type=''

    if country:userprofiles = userprofiles.filter(employeeprofile__country__id=country)
    else:country=''

    if nationality:userprofiles = userprofiles.filter(employeeprofile__nationality__id=nationality)
    else:nationality=''

    if gender:userprofiles = userprofiles.filter(employeeprofile__gender=gender)
    else:gender=''

    if marital_status:userprofiles = userprofiles.filter(employeeprofile__marital_status=marital_status)
    else:marital_status=''

    
    inputs = {
        'desires': desires,
        'cert_type': cert_type,
        'major': major,
        'nationality': nationality,
        'country': country,
        'employee_city': employee_city,
        'gender': gender,
        'marital_status': marital_status,
    }

    dic = {'userprofiles':userprofiles, 'CertTypeFields':CertTypeFields, 'GenderFields':GenderFields, 'StateFields':StateFields, 'nationalitys':nationalitys, 'countrys':countrys, 'healthes_status':healthes_status}
    objs = {}
    objs.update(dic)
    objs.update(inputs)

    return render(request, 'pages/AdvancedSearch.html', objs)


def PrivacyPolicy(request):
    path = str(BASE_DIR / 'accounts/jsons/terms_policy.json')
    file_reader = open(path, 'r', encoding='UTF-8')
    data = json.loads(file_reader.read())
    return render(request, 'pages/PrivacyPolicy.html', {'data':data})


def TermsConditions(request):
    path = str(BASE_DIR / 'accounts/jsons/terms_policy.json')
    file_reader = open(path, 'r', encoding='UTF-8')
    data = json.loads(file_reader.read())
    return render(request, 'pages/TermsConditions.html', {'data':data})


def ContactUs(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('msg')

        obj = ContactUsModel.objects.create(name=name, email=email, msg=msg, creation_date=timezone.now())
        obj.save()
        messages.success(request, 'شكرًا على تواصلك معنا سيتم الرد عليك في أقرب وقت')
    return redirect('index')

