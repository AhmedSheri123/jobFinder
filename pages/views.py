from django.shortcuts import render
from accounts.models import UserProfile, EmployeeProfile, CountrysModel, SubscriptionsModel
from accounts.fields import CertTypeFields, GenderFields, StateFields, NationalityFields
from notifications.views import create_notifications

# Create your views here.

def index(request):
    countrys = CountrysModel.objects.all()
    userprofiles = UserProfile.objects.filter(is_employee=True)
    subscriptions = SubscriptionsModel.objects.all()
    # u = []
    # for i in userprofiles:
    #     u.append(i.user.id)
    # aa = create_notifications(request.user.id, receiver_ids=u, msg='sadas as daasd a dsa d')
    # print(aa)
    return render(request, 'pages/index.html', {'userprofiles':userprofiles, 'subscriptions':subscriptions, 'countrys':countrys, 'GenderFields':GenderFields, 'NationalityFields':NationalityFields})


def AdvancedSearch(request):
    userprofiles = UserProfile.objects.filter(is_employee=True)
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

    if nationality:userprofiles = userprofiles.filter(employeeprofile__nationality=nationality)
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

    dic = {'userprofiles':userprofiles, 'CertTypeFields':CertTypeFields, 'GenderFields':GenderFields, 'StateFields':StateFields, 'NationalityFields':NationalityFields, 'countrys':countrys}
    objs = {}
    objs.update(dic)
    objs.update(inputs)

    return render(request, 'pages/AdvancedSearch.html', objs)