from django.shortcuts import render, redirect
from accounts.models import UserProfile, ViewersCounterByIPADDR, CountrysModel, CVSignupProcessChoices, CompanySignupProcessChoices, EmployeeProfile, SubscriptionsModel, UserSubscriptionModel, SubscriptionPriceByCountry, AdminADSModel, NationalityModel, AdminPermissionModel, HealthStatusModel, Withdraw, withdrawal_method_list, usdt_network_choices, ReferralLinkModel
from accounts.fields import GenderFields
from calendar import monthrange
from django.contrib.auth.models import User
from django.contrib import messages
from messenger.models import MessengerModel
from jobs.models import JobAppliersModel, JobsModel, JobStateChoices
from jobs.forms import JobsModelForm
from accounts.froms import SubscriptionModelForm, SubscriptionPriceByCountryModelForm, AdminADSModelForm, CountrysModelForm, NationalityModelForm, AdminPermissionModelForm, HealthStatusModelForm
from pages.models import ContactUsModel
from django.utils import timezone
from accounts.libs import send_msg_email_phone_noti, get_user_img, create_notifications
from django.conf import settings
from django.core.mail import send_mail
import datetime, json
from decimal import Decimal
from django.urls import reverse

BASE_DIR = settings.BASE_DIR
email_from = settings.EMAIL_HOST_USER

# Create your views here.
def has_perm(user):
    is_staff = False
    pers = AdminPermissionModel.objects.filter(user=user, is_enabled=True)

    if pers.exists() or user.is_superuser:
        is_staff = True
    
    return is_staff

def PanelHome(request):
    if request.user.is_superuser or has_perm(request.user):
            
        userprofile = UserProfile.objects.filter()
        companys = userprofile.filter(is_company = True)
        users = userprofile.filter(is_employee = True)
        employee_job_request = users
        company_job_posts = companys
        date_time_now = datetime.datetime.now()
        
        #------by month------>
        companys_creation_count_by_month = []
        users_creation_count_by_month = []
        for i in range(1, 13):
            companys_count = companys.filter(creation_date__month=i).count()
            users_count = users.filter(creation_date__month=i).count()
            companys_creation_count_by_month.append((i, companys_count))
            users_creation_count_by_month.append((i, users_count))
        #----end-----|


        #------by day------>
        companys_creation_count_by_day = []
        users_creation_count_by_day = []
        count_days_of_month = monthrange(date_time_now.year, date_time_now.month)

        for i in range(1, (count_days_of_month[1]+1)):
            companys_count = companys.filter(creation_date__year=date_time_now.year, creation_date__month=date_time_now.month, creation_date__day=i).count()
            users_count = users.filter(creation_date__year=date_time_now.year, creation_date__month=date_time_now.month, creation_date__day=i).count()
            companys_creation_count_by_day.append((i, companys_count))
            users_creation_count_by_day.append((i, users_count))
        #----end-----|




        #------by day------>
        
        viewsers_count_days = request.GET.get('viewsers_count_days')
        if viewsers_count_days:
            viewsers_count_days = int(viewsers_count_days)
        else: viewsers_count_days = 7

        viewsers_count_by_day = []

        for i in range(0, viewsers_count_days):
            i = datetime.datetime.now() + datetime.timedelta(days=-i)
            companys_count = ViewersCounterByIPADDR.objects.filter(creation_date__year=i.year, creation_date__month=i.month, creation_date__day=i.day).count()
            viewsers_count_by_day.append((i.date, companys_count))
        #----end-----|
            


        #------by day------>
        
        announced_count_days = request.GET.get('announced_count_days')
        if announced_count_days:
            announced_count_days = int(announced_count_days)
        else: announced_count_days = 7

        announced_count_by_day = []
        presenters_count_by_day = []

        for i in range(0, announced_count_days):
            i = datetime.datetime.now() + datetime.timedelta(days=-i)
            companys_count = company_job_posts.filter(creation_date__year=i.year, creation_date__month=i.month, creation_date__day=i.day).count()
            companys_count2 = employee_job_request.filter(creation_date__year=i.year, creation_date__month=i.month, creation_date__day=i.day).count()

            announced_count_by_day.append((i.date, companys_count))
            presenters_count_by_day.append((i.date, companys_count2))
        #----end-----|



        all_companys_count = companys.count()
        all_users_count = users.count()
        
        accepted_employee = employee_job_request.filter(cv_signup_process='6')
        accepted_employee_count = accepted_employee.count()
        accepted_employee_male_count = accepted_employee.filter(employeeprofile__gender = '1').count()
        accepted_employee_female_count = accepted_employee.filter(employeeprofile__gender = '2').count()

        accepted_employee_married_count = accepted_employee.filter(employeeprofile__marital_status = '1').count()
        accepted_employee_unmarried_count = accepted_employee.filter(employeeprofile__marital_status = '0').count()

        


        accepted_companys = company_job_posts.filter(company_signup_process='5').count()
        completed_companys = company_job_posts.filter(company_signup_process='4').count()
        all_announced = company_job_posts.filter().count()
        all_accepted_jobs = employee_job_request.filter(cv_signup_process='6').count()
        all_under_review_jobs = employee_job_request.filter(cv_signup_process='5').count()
        all_canseled_jobs = employee_job_request.filter(cv_signup_process='0').count()

        company_want_publish_job = 0
        for i in companys:
            if company_job_posts.filter(id=i.id).exists():
                company_want_publish_job+=1

        # wanted_male_gender = company_job_posts.filter(companyprofile__gender='1').count()
        # wanted_female_gender = company_job_posts.filter(companyprofile__gender='2').count()
        # wanted_no_preference_gender = company_job_posts.filter(gender='3').count()
        all_employee_male_count = users.filter(employeeprofile__gender='1').count()
        all_employee_female_count = users.filter(employeeprofile__gender='2').count()
        all_companys = companys.count()

        unaccepted_employee = employee_job_request.filter(cv_signup_process='0').count()
        
        all_dicts = {
            'companys_creation_count_by_month':companys_creation_count_by_month,
            'users_creation_count_by_month':users_creation_count_by_month,
            'companys_creation_count_by_day':companys_creation_count_by_day,
            'users_creation_count_by_day':users_creation_count_by_day,
            'all_companys_count':all_companys_count,
            'all_users_count':all_users_count,
            'accepted_employee_count':accepted_employee_count,
            'accepted_employee_male_count':accepted_employee_male_count,
            'accepted_employee_female_count':accepted_employee_female_count,
            'accepted_employee_married_count':accepted_employee_married_count,
            'accepted_employee_unmarried_count':accepted_employee_unmarried_count,
            # 'wanted_male_gender':wanted_male_gender,
            # 'wanted_female_gender':wanted_female_gender,
            # 'wanted_no_preference_gender':wanted_no_preference_gender,
            'unaccepted_employee':unaccepted_employee,

            'viewsers_count_by_day':viewsers_count_by_day,
            'viewsers_count_days':viewsers_count_days,

            'announced_count_by_day':announced_count_by_day,
            'presenters_count_by_day':presenters_count_by_day,
            'announced_count_days':announced_count_days,


            'all_announced':all_announced,
            'all_accepted_jobs':all_accepted_jobs,
            'all_under_review_jobs':all_under_review_jobs,
            'all_canseled_jobs':all_canseled_jobs,
            'all_employee_male_count' : all_employee_male_count,
            'all_employee_female_count' : all_employee_female_count,
            'all_companys':all_companys,
            'company_want_publish_job':company_want_publish_job,
            'completed_companys':completed_companys,
            'accepted_companys':accepted_companys
            }
        return render(request, 'panel/panel.html', all_dicts)






def PanelShowEmployees(request):
    if request.user.is_superuser or has_perm(request.user):
        countrys = CountrysModel.objects.all()
        jobs = UserProfile.objects.filter(is_employee=True).order_by('-id')
        
        country = request.GET.get('country')
        if country:jobs = jobs.filter(employeeprofile__country=country)

        gender = request.GET.get('gender')
        if gender:jobs = jobs.filter(employeeprofile__gender=gender)

        state = request.GET.get('state')
        if state:jobs = jobs.filter(company_signup_process=state)

        search = request.GET.get('search')
        if search:jobs = jobs.filter(employeeprofile__name__contains=search)
        else:search=''

        post_state = request.GET.get('post_state')
        if post_state:jobs = jobs.filter(cv_signup_process=post_state)

        id_code = request.GET.get('id_code')
        if id_code:jobs = jobs.filter(alt_id=id_code)
        else:id_code=''

        search_email = request.GET.get('search_email')
        if search_email:jobs = jobs.filter(user__email=search_email)
        else:search_email=''

        search_phone = request.GET.get('search_phone')
        if search_phone:jobs = jobs.filter(employeeprofile__phone=search_phone)
        else:search_phone=''

        publish_date = request.GET.get('publish_date')
        if publish_date:jobs = jobs.filter(creation_date__date=datetime.datetime.strptime(publish_date, '%Y-%m-%d'))
        else:publish_date=''



        fields = {
            'CVSignupProcessChoices':CVSignupProcessChoices,
            'GenderFields':GenderFields,
            'countrys':countrys,
            'country_id':country,
            'id_code':id_code,
            'state':state,
            'search':search,
            'gender':gender,
            'publish_date':publish_date,
            'search_email':search_email,
            'search_phone':search_phone,
            
        }
        obj = {'jobs':jobs}

        obj.update(fields)
        

        return render(request, 'panel/employee/PanelShowEmployees.html', obj)



def PanelShowEmployee(request, id):

    if request.user.is_superuser or has_perm(request.user):
        employee = EmployeeProfile.objects.get(id=id)
        userprofile = UserProfile.objects.get(employeeprofile=employee)
        if request.method == 'POST':
            state = request.POST.get('state')
            msg = request.POST.get('msg')
            subject = request.POST.get('subject')
            
            userprofile.cv_signup_process = state
            userprofile.save()

            send_msg_email_phone_noti(subject, msg, request.user.id, [userprofile.user.id])
        return render(request, 'panel/employee/PanelShowEmployee.html', {'employee':employee, 'EmployeeJobStateFields':CVSignupProcessChoices, 'userprofile':userprofile})


def DeleteEmployees(request, id):
    if request.user.is_superuser or has_perm(request.user):
            
        # if request.user.userprofile.admin_permission == '0':
        obj = User.objects.get(userprofile__id=id)
        
        if obj.userprofile:
            employeeprofile_id = obj.userprofile.employeeprofile.id
            if employeeprofile_id:
                e_profile = EmployeeProfile.objects.filter(id=employeeprofile_id)
                e_profile.delete()
        obj.delete()
        msgr = MessengerModel.objects.filter(messenger_users__id__in=[obj.id])
        
        
        for i in msgr:
            i.delete()
        # else:
        #     messages.error(request, 'لا يوجد لديك اذونات للوصول الى هذه الخاصية')

        return redirect('PanelShowEmployees')
    




def Companys(request):
    if request.user.is_superuser or has_perm(request.user):
        countrys = CountrysModel.objects.all()

        jobs = UserProfile.objects.filter(is_company=True).order_by('-id')
        

        search = request.GET.get('search')
        if search:jobs = jobs.filter(companyprofile__company_name__contains=search)
        else:search=''

        country = request.GET.get('country')
        if country:jobs = jobs.filter(employeeprofile__country=country)



        state = request.GET.get('state')
        if state:jobs = jobs.filter(company_signup_process=state)


        search_email = request.GET.get('search_email')
        if search_email:jobs = jobs.filter(user__email=search_email)
        else:search_email=''

        search_phone = request.GET.get('search_phone')
        if search_phone:jobs = jobs.filter(companyprofile__phone=search_phone)
        else:search_phone=''

        complite_name = request.GET.get('complite_name')
        if complite_name:jobs = jobs.filter(companyprofile__complite_name__contains=complite_name)
        else:complite_name=''

        publish_date = request.GET.get('publish_date')
        if publish_date:jobs = jobs.filter(creation_date__date=datetime.datetime.strptime(publish_date, '%Y-%m-%d'))
        else:publish_date=''
        
        fields = {
                'state':state,
                'CompanySignupProcessChoices':CompanySignupProcessChoices,
                'countrys':countrys,
                'country_id':country,
                'search':search,
                'publish_date':publish_date,
                'search_email':search_email,
                'search_phone':search_phone,
                'complite_name':complite_name,
                }
        
        obj = {'jobs':jobs}
        obj.update(fields)
        return render(request, 'panel/company/company/Companys.html', obj)




def Company(request, id):
    if request.user.is_superuser or has_perm(request.user):            
        company = UserProfile.objects.get(id=id)
        img = get_user_img(company.user)

        if request.method == 'POST':
            state = request.POST.get('state')
            msg = request.POST.get('msg')
            subject = request.POST.get('subject')

            company.company_signup_process = state
            company.save()
            send_msg_email_phone_noti(subject, msg, request.user.id, [company.user.id])

        return render(request, 'panel/company/company/Company.html', {'company':company, 'img':img, 'CompanySignupProcessChoices':CompanySignupProcessChoices})
    
def DeleteCompanys(request, id):
    if request.user.is_superuser or has_perm(request.user):
        # if request.user.userprofile.admin_permission == '0':
        obj = User.objects.get(userprofile__id=id)
        obj.delete()
        # else:
        #     messages.error(request, 'لا يوجد لديك اذونات للوصول الى هذه الخاصية')
        return redirect('Companys')


def ViewJobsPanel(request):
    if request.user.is_superuser or has_perm(request.user):

        jobs = JobsModel.objects.filter().order_by('-id')

        

        search = request.GET.get('search')
        if search:jobs = jobs.filter(user__userprofile__companyprofile__company_name__contains=search)
        else:search=''

        job_title = request.GET.get('job_title')
        if job_title:jobs = jobs.filter(job_title__contains=job_title)
        else:job_title=''


        state = request.GET.get('state')
        if state:jobs = jobs.filter(state=state)


        search_email = request.GET.get('search_email')
        if search_email:jobs = jobs.filter(user__email=search_email)
        else:search_email=''

        search_phone = request.GET.get('search_phone')
        if search_phone:jobs = jobs.filter(user__userprofile__companyprofile__phone=search_phone)
        else:search_phone=''

        complite_name = request.GET.get('complite_name')
        if complite_name:jobs = jobs.filter(user__userprofile__companyprofile__complite_name__contains=complite_name)
        else:complite_name=''

        publish_date = request.GET.get('publish_date')
        if publish_date:jobs = jobs.filter(creation_date__date=datetime.datetime.strptime(publish_date, '%Y-%m-%d'))
        else:publish_date=''


    
    fields = {
            'JobStateChoices':JobStateChoices,
            'state':state,
            'search':search,
            'job_title':job_title,
            'publish_date':publish_date,
            'search_email':search_email,
            'search_phone':search_phone,
            'complite_name':complite_name,
            }
    
    obj = {'jobs':jobs}
    obj.update(fields)
    return render(request, 'panel/company/jobs/CompanyPostJobs.html', obj)


def ViewCompanyPostJobs(request, id):
    user = request.user
    job = JobsModel.objects.get(id=id)
    appliers = JobAppliersModel.objects.filter(job=job)
    state = job.state
    form = JobsModelForm(instance=job)
    if request.method == 'POST':
        state = request.POST.get('state')
        form = JobsModelForm(request.POST, instance=job)
        print(form)
        
        if form.is_valid():
            job = form.save(commit=False)
            job.state = state
            job.save()

    
    return render(request, 'panel/company/jobs/ViewCompanyPostJobs.html', {'form':form, 'job':job, 'appliers':appliers, 'JobStateChoices':JobStateChoices, 'state':state})


def adminDeleteAppier(request, id):
    applier = JobAppliersModel.objects.get(id=id)
    job_id = applier.job.id
    applier.delete()
    return redirect('ViewCompanyPostJobs', job_id)


def adminDeleteJob(request, id):
    job = JobsModel.objects.get(id=id)
    job.delete()
    return redirect('ViewJobsPanel')


def PanelViewSubscriptions(request):
    subscriptions = SubscriptionsModel.objects.all()
    return render(request, 'panel/subscriptions/sub/PanelViewSubscriptions.html', {'subscriptions':subscriptions})

def PanelAddSubscriptions(request):
    form = SubscriptionModelForm()
    if request.method == 'POST':
        form = SubscriptionModelForm(request.POST)
        form.save()
        
    return render(request, 'panel/subscriptions/sub/addSubscriptions.html', {'form':form})


def PanelEditSubscriptions(request, id):
    subscription = SubscriptionsModel.objects.get(id=id)
    form = SubscriptionModelForm(instance=subscription)
    if request.method == 'POST':
        form = SubscriptionModelForm(request.POST, instance=subscription)
        form.save()

    return render(request, 'panel/subscriptions/sub/addSubscriptions.html', {'form':form})


def ManageSubscriptionPriceByCountry(request):
    objs = SubscriptionPriceByCountry.objects.all()

    return render(request, 'panel/subscriptions/SubscriptionPriceByCountry/ManageSubscriptionPriceByCountry.html', {'objs':objs})

def AddSubscriptionPriceByCountry(request):
    form = SubscriptionPriceByCountryModelForm()
    if request.method == 'POST':
        form = SubscriptionPriceByCountryModelForm(request.POST)
        form.save()
        return redirect('ManageSubscriptionPriceByCountry')
    return render(request, 'panel/subscriptions/SubscriptionPriceByCountry/AddSubscriptionPriceByCountry.html', {'form':form})

def EditSubscriptionPriceByCountry(request, id):
    subscription = SubscriptionPriceByCountry.objects.get(id=id)
    form = SubscriptionPriceByCountryModelForm(instance=subscription)
    if request.method == 'POST':
        form = SubscriptionPriceByCountryModelForm(request.POST, instance=subscription)
        form.save()
        return redirect('ManageSubscriptionPriceByCountry')
    return render(request, 'panel/subscriptions/SubscriptionPriceByCountry/EditSubscriptionPriceByCountry.html', {'form':form})


def DeleteSubscriptionPriceByCountry(request, id):
    subscription = SubscriptionPriceByCountry.objects.get(id=id)
    subscription.delete()
    return redirect('ManageSubscriptionPriceByCountry')

def PanelDeleteSubscriptions(request, id):
    subscription = SubscriptionsModel.objects.get(id=id)
    subscription.delete()
    return redirect('PanelViewSubscriptions')



def ShowAllContactUsHistory(request):
    if request.user.is_superuser or has_perm(request.user):
            
        contact_us = ContactUsModel.objects.all().order_by('-id')

        return render(request, 'panel/network/ContactUs/ShowAllContactUsHistory.html', {'contact_us':contact_us})
    
def DeleteContactUs(request, id):
    if request.user.is_superuser or has_perm(request.user):
            
        contact_us = ContactUsModel.objects.get(id=id)
        contact_us.delete()

        return redirect('ShowAllContactUsHistory')    
    

def ContactUsSendReplay(request, id):
    if request.user.is_superuser or has_perm(request.user):
            
        contact_us = ContactUsModel.objects.get(id=id)
        if request.method == 'POST':
            subject = request.POST.get('subject')
            replay_msg = request.POST.get('replay_msg')
            email = contact_us.email
            if replay_msg:
                try:
                    send_mail( subject, replay_msg, email_from, [email])
                    messages.success(request, 'تم ارسال الرسالة')
                except:
                    messages.error(request, 'حدث خطاء اثناء ارسال الرسالة')
        return redirect('ShowAllContactUsHistory')    


def ManageAdminADS(request):
    objs = AdminADSModel.objects.all()

    return render(request, 'panel/ADS/ManageAdminADS.html', {'objs':objs})

def AddAdminADS(request):
    form = AdminADSModelForm()
    if request.method == 'POST':
        form = AdminADSModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            ob = form.save()
            ob.creation_date = timezone.now()
            ob.save()
            return redirect('ManageAdminADS')
    return render(request, 'panel/ADS/AddAdminADS.html', {'form':form})

def EditAdminADS(request, id):
    subscription = AdminADSModel.objects.get(id=id)
    form = AdminADSModelForm(instance=subscription)
    if request.method == 'POST':
        form = AdminADSModelForm(data=request.POST, files=request.FILES, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('ManageAdminADS')
    return render(request, 'panel/ADS/EditAdminADS.html', {'form':form})


def DeleteAdminADS(request, id):
    subscription = AdminADSModel.objects.get(id=id)
    subscription.delete()
    return redirect('ManageAdminADS')






def ManageCountrys(request):
    objs = CountrysModel.objects.all()

    return render(request, 'panel/countrys/ManageCountrys.html', {'objs':objs})

def AddCountrys(request):
    form = CountrysModelForm()
    if request.method == 'POST':
        form = CountrysModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            ob = form.save()
            ob.creation_date = timezone.now()
            ob.save()
            return redirect('ManageCountrys')
    return render(request, 'panel/countrys/AddCountrys.html', {'form':form})

def EditCountrys(request, id):
    subscription = CountrysModel.objects.get(id=id)
    form = CountrysModelForm(instance=subscription)
    if request.method == 'POST':
        form = CountrysModelForm(data=request.POST, files=request.FILES, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('ManageCountrys')
    return render(request, 'panel/countrys/EditCountrys.html', {'form':form})


def DeleteCountrys(request, id):
    subscription = CountrysModel.objects.get(id=id)
    subscription.delete()
    return redirect('ManageCountrys')






def ManageNationality(request):
    objs = NationalityModel.objects.all()

    return render(request, 'panel/nationality/ManageNationality.html', {'objs':objs})

def AddNationality(request):
    form = NationalityModelForm()
    if request.method == 'POST':
        form = NationalityModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            ob = form.save()
            ob.creation_date = timezone.now()
            ob.save()
            return redirect('ManageNationality')
    return render(request, 'panel/nationality/AddNationality.html', {'form':form})

def EditNationality(request, id):
    subscription = NationalityModel.objects.get(id=id)
    form = NationalityModelForm(instance=subscription)
    if request.method == 'POST':
        form = NationalityModelForm(data=request.POST, files=request.FILES, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('ManageNationality')
    return render(request, 'panel/nationality/EditNationality.html', {'form':form})

def DeleteNationality(request, id):
    subscription = NationalityModel.objects.get(id=id)
    subscription.delete()
    return redirect('ManageNationality')






def ManageHealthStatus(request):
    objs = HealthStatusModel.objects.all()

    return render(request, 'panel/HealthStatus/ManageHealthStatus.html', {'objs':objs})

def AddHealthStatus(request):
    form = HealthStatusModelForm()
    if request.method == 'POST':
        form = HealthStatusModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            ob = form.save()
            ob.creation_date = timezone.now()
            ob.save()
            return redirect('ManageHealthStatus')
    return render(request, 'panel/HealthStatus/AddHealthStatus.html', {'form':form})

def EditHealthStatus(request, id):
    subscription = HealthStatusModel.objects.get(id=id)
    form = HealthStatusModelForm(instance=subscription)
    if request.method == 'POST':
        form = HealthStatusModelForm(data=request.POST, files=request.FILES, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('ManageHealthStatus')
    return render(request, 'panel/HealthStatus/EditHealthStatus.html', {'form':form})

def DeleteHealthStatus(request, id):
    subscription = HealthStatusModel.objects.get(id=id)
    subscription.delete()
    return redirect('ManageHealthStatus')






def ManageAdminPermission(request):
    objs = AdminPermissionModel.objects.all()

    return render(request, 'panel/admin_permission/ManageAdminPermission.html', {'objs':objs})

def AddAdminPermission(request):
    form = AdminPermissionModelForm()
    if request.method == 'POST':
        form = AdminPermissionModelForm(data=request.POST, files=request.FILES)
        user_id = request.POST.get('user_id')
        users = User.objects.filter(username=user_id)
        if users.exists():
            user = users.first()
            if form.is_valid():
                ob = form.save(commit=False)
                ob.user = user
                ob.creation_date = timezone.now()
                ob.save()
                return redirect('ManageAdminPermission')
        else:messages.error(request, 'رقم العضوية غير موجودة')
    return render(request, 'panel/admin_permission/AddAdminPermission.html', {'form':form})

def EditAdminPermission(request, id):
    subscription = AdminPermissionModel.objects.get(id=id)
    form = AdminPermissionModelForm(instance=subscription)
    if request.method == 'POST':
        form = AdminPermissionModelForm(data=request.POST, files=request.FILES, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('ManageAdminPermission')
    return render(request, 'panel/admin_permission/EditAdminPermission.html', {'form':form})

def DeleteAdminPermission(request, id):
    subscription = AdminPermissionModel.objects.get(id=id)
    subscription.delete()
    return redirect('ManageAdminPermission')


def get_permission_state(user_id, url, method):
    user = User.objects.get(id=user_id)
    permissions = AdminPermissionModel.objects.filter(user=user)

    if user.is_superuser:
        return True
    
    elif permissions.exists():
        permission = permissions.first()
        if url == 'employees':
            if method == 'show':
                return permission.show_employees
            elif method == 'edit':
                return permission.edit_employees
            elif method == 'delete':
                return permission.delete_employees
            
        elif url == 'companys':
            if method == 'show':
                return permission.show_companys
            elif method == 'edit':
                return permission.edit_companys
            elif method == 'delete':
                return permission.delete_companys
            
        elif url == 'jobs':
            if method == 'show':
                return permission.show_jobs
            elif method == 'edit':
                return permission.edit_jobs
            elif method == 'delete':
                return permission.delete_jobs
            
        elif url == 'subscription':
            if method == 'show':
                return permission.show_subscription
            elif method == 'add':
                return permission.add_subscription
            elif method == 'edit':
                return permission.edit_subscription
            elif method == 'delete':
                return permission.delete_subscription
            
        elif url == 'custum_subscription':
            if method == 'show':
                return permission.show_custum_subscription
            elif method == 'add':
                return permission.add_custum_subscription
            elif method == 'edit':
                return permission.edit_custum_subscription
            elif method == 'delete':
                return permission.delete_custum_subscription
            
        elif url == 'ads':
            if method == 'show':
                return permission.show_ads
            elif method == 'add':
                return permission.add_ads
            elif method == 'edit':
                return permission.edit_ads
            elif method == 'delete':
                return permission.delete_ads
            
        elif url == 'countrys':
            if method == 'show':
                return permission.show_countrys
            elif method == 'add':
                return permission.add_countrys
            elif method == 'edit':
                return permission.edit_countrys
            elif method == 'delete':
                return permission.delete_countrys
            
        elif url == 'nationality':
            if method == 'show':
                return permission.show_nationality
            elif method == 'add':
                return permission.add_nationality
            elif method == 'edit':
                return permission.edit_nationality
            elif method == 'delete':
                return permission.delete_nationality
            
        elif url == 'user_subscription':
            if method == 'show':
                return permission.show_user_subscription
            elif method == 'edit':
                return permission.edit_user_subscription
            
        elif url == 'send_notifications':
            if method == 'show':
                return permission.send_notifications
            
        elif url == 'edit_settings':
            if method == 'show':
                return permission.edit_settings
            if method == 'edit':
                return permission.edit_settings
    
    return False


def EditVerificationMsg(request):
    path = str(BASE_DIR / 'accounts/jsons/verification_msg.json')
    file_reader = open(path, 'r', encoding='UTF-8')
    data = json.loads(file_reader.read())
    file_reader.close()
        
    if request.method == 'POST':
        subject = request.POST.get('subject')
        msg = request.POST.get('msg')
        file_writer = open(path, 'w', encoding='UTF-8')
        data = {
            'subject':subject,
            'msg': msg
        }
        file_writer.write(json.dumps(data))

    return render(request, 'panel/settings/EditVerificationMsg.html', {'data':data})



def EditTermsPolicy(request):
    path = str(BASE_DIR / 'accounts/jsons/terms_policy.json')
    file_reader = open(path, 'r', encoding='UTF-8')
    data = json.loads(file_reader.read())
    file_reader.close()
        
    if request.method == 'POST':
        TermsConditions = request.POST.get('TermsConditions')
        PrivacyPolicy = request.POST.get('PrivacyPolicy')
        file_writer = open(path, 'w', encoding='UTF-8')
        data = {
            'TermsConditions':TermsConditions,
            'PrivacyPolicy': PrivacyPolicy
        }
        file_writer.write(json.dumps(data))

    return render(request, 'panel/settings/TermsPolicy.html', {'data':data})







def WithdrawDelete(request, id):
    if request.user.is_superuser:
        REFERER = request.META['HTTP_REFERER']
        withdraws = Withdraw.objects.get(id=id)
        withdraws.delete()

        return redirect(REFERER)

def getWithdrawPercentage(total, percentage):
    
    x = percentage / 100
    x = Decimal(x)
    result = total * x
    return result

def WithdrawComplete(request, id):
    if request.user.is_superuser:
        REFERER = request.META['HTTP_REFERER']
        withdraws = Withdraw.objects.get(id=id)
        withdraws.status = '2'
        withdraws.save()

        link = reverse('Withdrawn')
        message_ar = f'تم الانتهاء من عملية السحب بنجاح بقيمة {withdraws.total_amount} للمشاهدة <a style="color: #438fff;" href={link} target="_blank">اضغط هنا</a>'
        create_notifications(sender_id=request.user.id, receiver_ids=[withdraws.user.id], msg=message_ar)
        
        userprofile = withdraws.user.userprofile
        userprofile.money = userprofile.money - withdraws.total_amount
        userprofile.save()
        if userprofile.referral:
            ref = ReferralLinkModel.objects.get(id=userprofile.referral.id)
            result = getWithdrawPercentage(withdraws.total_amount, ref.percentage_of_withdraw)
            ref.total_earn = ref.total_earn + result
            ref.all_total_earn = ref.all_total_earn + result
            ref.save()
        return redirect(REFERER)

def WithdrawCancel(request, id):
    if request.user.is_superuser:
        
        if request.method == 'POST':

            REFERER = request.META['HTTP_REFERER']
            withdraws = Withdraw.objects.get(id=id)
            userprofile = withdraws.user.userprofile
            if withdraws.status == '2':
                userprofile.money += withdraws.total_amount
                if userprofile.referral:
                    ref = ReferralLinkModel.objects.get(id=userprofile.referral.id)
                    result = getWithdrawPercentage(withdraws.total_amount, ref.percentage_of_withdraw)
                    ref.total_earn = ref.total_earn - result
                    ref.all_total_earn = ref.all_total_earn - result
                    ref.save()

                
            withdraws.status = '3'
            withdraws.save()
            msg = request.POST.get('msg')
            create_notifications(sender_id=request.user.id, receiver_ids=[withdraws.user.id], msg=msg)

            userprofile.save()
    
            return redirect(REFERER)

def WithdrawAccept(request, id):
    if request.user.is_superuser:
        REFERER = request.META['HTTP_REFERER']
        withdraws = Withdraw.objects.get(id=id)
        withdraws.status = '1'
        withdraws.save()
        return redirect(REFERER)

def dashboardWithdraw(request):
    data = request.GET
    filter_enabled = data.get('filter_enabled')
    withdraws = Withdraw.objects.filter()
    filter_list = []
    if data.get('Pending'):
        filter_list.append('0')

    if data.get('Accepted'):
        filter_list.append('1')

    if data.get('Completed'):
        
        filter_list.append('2')

    if data.get('Canceled'):
        filter_list.append('3')
    if filter_enabled:
        withdraws = withdraws.filter(status__in=filter_list)
    Pending = withdraws.filter(status='0').count()
    accepted = withdraws.filter(status='1').count()
    Completed = withdraws.filter(status='2').count()
    Canceled = withdraws.filter(status='3').count()

    return render(request, 'panel/withdraw/dashboardWithdraw.html', {'withdraws':withdraws, 'accepted':accepted,
    'Completed':Completed, 'Canceled':Canceled, 'Pending':Pending, 'Pending_form': data.get('Pending'), 
    'Accepted_form': data.get('Accepted'), 'Completed_form' : data.get('Completed'), 'Canceled_form': data.get('Canceled'), 'filter_enabled': filter_enabled,
    'withdrawal_method':withdrawal_method_list, 'usdt_network_choices':usdt_network_choices
    })
