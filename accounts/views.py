from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile, EmployeeProfile, CompanyProfile, CountrysModel, SkilsModel, EmployeeProfileImages, ReferralLinkModel, SubscriptionsModel, UserSubscriptionModel, UserViewedProfileModel, CompanyRandomNumCodeGen, UserPaymentOrderModel, WhatsappOTP, EmailOTPModel, UserLikeModel, ForgetPWDModel, NationalityModel, GenrateUserID, HealthStatusModel, Withdraw, withdrawal_method_list, usdt_network_choices
from .fields import GenderFields, StateFields, YesNoFields, HealthStatusFields, CertTypeFields, NationalityFields
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .froms import CompanyProfileForm
from django.contrib.sites.shortcuts import get_current_site
from .libs import DatetimeNow, get_ip_info, filter_sub_price, extract_soshial_profile_url
from .payment import addInvoice, getInvoice
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from .whatsapp import wa_send_msg
from django.core.mail import send_mail
from messenger.models import FavoriteUserModel
from django.conf import settings
from django.db.models import Q
from dashboard.views import has_perm
from .libs import get_dial_code_by_country_code, phoneCleaner
from jobs.models import JobAppliersModel, JobsModel
import json
# Create your views here.
email_from = settings.EMAIL_HOST_USER
BASE_DIR = settings.BASE_DIR



def cvSignup(request):
    alt_id = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = phoneCleaner(request.POST.get('phone'))
        country_code = request.POST.get('country_code')

        company_profiles = CompanyProfile.objects.filter(phone=phone, phone_country_code=country_code)
        employee_profiles = EmployeeProfile.objects.filter(phone=phone, phone_country_code=country_code)
        if employee_profiles.exists() and company_profiles.exists():
            messages.error(request, 'الرقم مسجل من قبل الرجاء تسجيل الدخول')
            return redirect('Login')

        user = User.objects.create()
        user.set_password(password)
        employee_profile = EmployeeProfile.objects.create()
        employee_profile.phone = phone
        employee_profile.phone_country_code=country_code = country_code

        employee_profile.save()
        userprofile = UserProfile.objects.create(user=user, is_employee=True, employeeprofile=employee_profile)
        user.username = GenrateUserID(5)
        user.save()
        userprofile.cv_signup_process = '2'
        referral_id = request.session['referral_id']
        if referral_id:
            referral = ReferralLinkModel.objects.get(id=referral_id)
            userprofile.referral=referral

        userprofile.save()
        alt_id = userprofile.alt_id

        return redirect('SignupSetupProcess', userprofile.alt_id)
    return render(request, 'accounts/signup/Employee/cvSignup.html', {'alt_id':alt_id})



def cvSignupVerifyEmail(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    user = userprofile.user
    VerifyProccess = None
    
    if not userprofile.is_phone_verificated:VerifyProccess='1'
    elif not userprofile.is_email_verificated:VerifyProccess='2'
    else:VerifyProccess='0'


    # if VerifyProccess == '2':
    #     first_opt = EmailOTPModel.objects.filter(user=user, is_finshed=False)
    #     if not first_opt.exists():
    #         return sendEmailCode(request, alt_id)

    if VerifyProccess == '1':
        first_opt = WhatsappOTP.objects.filter(user=user, is_finshed=False)
        if not first_opt.exists():
            co = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
            OPT = WhatsappOTP.objects.create(user=user)
            OPT.save()

            path = str(BASE_DIR / 'accounts/jsons/verification_msg.json')
            file_reader = open(path, 'r', encoding='UTF-8')
            data = json.loads(file_reader.read())
            msg = data['msg'].format(code=OPT.secret)
            dial_code = get_dial_code_by_country_code(co.phone_country_code)

            wa_send_msg(msg, co.phone, dial_code)
            return redirect('EmployeeSendWhaCodeVerify', alt_id)


    if request.method == 'POST':
        if VerifyProccess == '1':
            phone = phoneCleaner(request.POST.get('phone'))
            country_code = request.POST.get('country_code')
            co = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
            co.phone = phone
            co.phone_country_code = country_code
            co.save()
            OPT = WhatsappOTP.objects.create(user=user)
            OPT.save()
            path = str(BASE_DIR / 'accounts/jsons/verification_msg.json')
            file_reader = open(path, 'r', encoding='UTF-8')
            data = json.loads(file_reader.read())
            msg = data['msg'].format(code=OPT.secret)

            dial_code = get_dial_code_by_country_code(co.phone_country_code)
            
            wa_send_msg(msg, co.phone, dial_code)
            return redirect('EmployeeSendWhaCodeVerify', alt_id)


        elif VerifyProccess == '2':
            email = request.POST.get('email')
            users = User.objects.filter(email=email)
            if users.exists():
                messages.error(request, 'البريد الالكتروني مسجل من قبل الرجاء اختيار بريد اخر')
                return redirect('SignupSetupProcess', userprofile.alt_id)
            if email:
                user.email = email
                user.save()
                # EnableDefaultUserSubscription(userprofile.id)
                sendEmailCode(request, alt_id)
                return redirect('EmployeeSendEmailCodeVerify', alt_id)


        return redirect('SignupSetupProcess', userprofile.alt_id)
    return render(request, 'accounts/signup/Employee/cvSignupVerifyEmail.html', {'alt_id':alt_id, 'VerifyProccess':VerifyProccess})

def cvSignupConf(request, alt_id):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        job_title = request.POST.get('job_title')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        userprofile = UserProfile.objects.get(alt_id=alt_id)
        
        employee_profile = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
        employee_profile.name = full_name
        employee_profile.job_title = job_title
        employee_profile.gender = gender
        employee_profile.age = age
        employee_profile.save()
        userprofile.employeeprofile = employee_profile
        userprofile.cv_signup_process = '4'
        userprofile.save()
        return redirect('SignupSetupProcess', userprofile.alt_id)
    return render(request, 'accounts/signup/Employee/cvSignupConf.html', {'GenderFields':GenderFields, 'alt_id':alt_id})


def cvSignupCvCreation(request, alt_id):
    healthes_status = HealthStatusModel.objects.all()
    countrys = CountrysModel.objects.all()
    nationalitys = NationalityModel.objects.all()
    skils_model = SkilsModel.objects.all()

    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        marital_status = request.POST.get('marital_status')
        health_status = request.POST.get('health_status')
        country = request.POST.get('country')
        employee_city = request.POST.get('employee_city')
        district = request.POST.get('district')
        nationality = request.POST.get('nationality')
        have_car = request.POST.get('have_car')
        about_me = request.POST.get('about_me')
        cert_type = request.POST.get('cert_type')
        major = request.POST.get('major')
        
        desires = request.POST.getlist('desires')
        experiences = request.POST.getlist('experiences')
        classes = request.POST.getlist('classes')
        skils = request.POST.getlist('skils')
        lang = request.POST.getlist('lang')
        
        userprofile = UserProfile.objects.get(alt_id=alt_id)
        employee_profile = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
        
        employee_profile.weight = weight
        employee_profile.height = height
        employee_profile.marital_status = marital_status
        employee_profile.health_status = HealthStatusModel.objects.get(id=health_status)
        employee_profile.country = countrys.get(id=country)
        employee_profile.employee_city = employee_city
        employee_profile.district = district
        employee_profile.nationality = nationalitys.get(id=nationality)
        employee_profile.have_car = have_car
        employee_profile.about_me = about_me
        employee_profile.cert_type = cert_type
        employee_profile.major = major
        employee_profile.desires = {'desires':desires}
        employee_profile.experiences = {'desires':experiences}
        employee_profile.classes = {'desires':classes}
        employee_profile.skils = {'desires':skils}
        employee_profile.lang = {'desires':lang}
        

        userprofile.cv_signup_process = '5'
        employee_profile.save()
        userprofile.save()
        EnableDefaultUserSubscription(userprofile.id)
        messages.success(request, '( تم التسجيل بنجاح وهو قيد المراجعة الان . وقد يستغرق ذلك ٢٤ الى ٤٨ ساعة ) . حتى تتمكن من استخدام خدمات المنصة')
        return redirect('Login')
    return render(request, 'accounts/signup/Employee/cvSignupCvCreation.html', {'alt_id':alt_id, 'NationalityFields':NationalityFields, 'CertTypeFields':CertTypeFields, 'skils_model':skils_model, 'HealthStatusFields':HealthStatusFields, 'StateFields':StateFields, 'YesNoFields':YesNoFields, 'countrys':countrys, 'nationalitys':nationalitys, 'healthes_status':healthes_status})


def companySignup(request):
    alt_id = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = phoneCleaner(request.POST.get('phone'))
        country_code = request.POST.get('country_code')

        employee_profiles = EmployeeProfile.objects.filter(phone=phone, phone_country_code=country_code)
        company_profiles = CompanyProfile.objects.filter(phone=phone, phone_country_code=country_code)
        if company_profiles.exists() and employee_profiles.exists():
            messages.error(request, 'الرقم مسجل من قبل الرجاء تسجيل الدخول')
            return redirect('Login')
        user = User.objects.create()
        user.set_password(password)
        company_profile = CompanyProfile.objects.create()
        company_profile.phone = phone
        company_profile.phone_country_code=country_code
        company_profile.save()

        userprofile = UserProfile.objects.create(user=user, is_company=True, companyprofile=company_profile)
        
        user.username = GenrateUserID(5)
        alt_id = userprofile.alt_id
        user.save()
        userprofile.company_signup_process = '2'
        referral_id = request.session['referral_id']
        if referral_id:
            referral = ReferralLinkModel.objects.get(id=referral_id)
            userprofile.referral=referral

        userprofile.save()
        return redirect('SignupSetupProcess', userprofile.alt_id)
    return render(request, 'accounts/signup/Company/companySignup.html', {'alt_id':alt_id})

def companySignupConf(request, alt_id):
    countrys = CountrysModel.objects.all()

    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        complite_name = request.POST.get('complite_name')
        country = request.POST.get('country')
        city = request.POST.get('city')
        district = request.POST.get('district')

        userprofile = UserProfile.objects.get(alt_id=alt_id)
        
        company_profile = CompanyProfile.objects.get(id=userprofile.companyprofile.id)
        company_profile.company_name=company_name
        company_profile.complite_name=complite_name
        company_profile.employee_city=city
        company_profile.district=district
        company_profile.country = countrys.get(id=country)
        company_profile.save()
        userprofile.company_signup_process = '4'
        userprofile.save()
        EnableDefaultUserSubscription(userprofile.id)
        messages.success(request, '( تم التسجيل بنجاح وهو قيد المراجعة الان . وقد يستغرق ذلك ٢٤ الى ٤٨ ساعة ) . حتى تتمكن من استخدام خدمات المنصة')

        return redirect('SignupSetupProcess', userprofile.alt_id)
    return render(request, 'accounts/signup/Company/companySignupConf.html', {'countrys':countrys, 'alt_id':alt_id})


def sendEmailCode(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    user = userprofile.user
    OPT = EmailOTPModel.objects.create(user=user)
    OPT.save()

    path = str(BASE_DIR / 'accounts/jsons/verification_msg.json')
    file_reader = open(path, 'r', encoding='UTF-8')
    data = json.loads(file_reader.read())
    subject = data['subject']
    msg = data['msg'].format(code=OPT.secret)

    send_mail( subject, msg, email_from, [userprofile.user.email] )
    messages.success(request, 'تم ارسال رمز تأكيد عبر البريدالالكتروني')

    # return redirect('SignupSetupProcess', alt_id)
    return True
# 

def companySignupVerifyEmail(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    user = User.objects.get(id=userprofile.user.id)
    VerifyProccess = None
    
    if not userprofile.is_phone_verificated:VerifyProccess='1'
    elif not userprofile.is_email_verificated:VerifyProccess='2'
    else:VerifyProccess='0'

    # if VerifyProccess == '2':
    #     first_opt = EmailOTPModel.objects.filter(user=user, is_finshed=False)
    #     if not first_opt.exists():
    #         return sendEmailCode(request, alt_id)

    if VerifyProccess == '1':
        first_opt = WhatsappOTP.objects.filter(user=user, is_finshed=False)
        if not first_opt.exists():
            co = CompanyProfile.objects.get(id=userprofile.companyprofile.id)
            OPT = WhatsappOTP.objects.create(user=user)
            OPT.save()
            path = str(BASE_DIR / 'accounts/jsons/verification_msg.json')
            file_reader = open(path, 'r', encoding='UTF-8')
            data = json.loads(file_reader.read())
            msg = data['msg'].format(code=OPT.secret)
            dial_code = get_dial_code_by_country_code(co.phone_country_code)

            wa_send_msg(msg, co.phone, dial_code)
            return redirect('SendWhaCodeVerify', alt_id)



    if request.method == 'POST':

        if VerifyProccess == '1':
            phone = phoneCleaner(request.POST.get('phone'))
            country_code = request.POST.get('country_code')
            co = CompanyProfile.objects.get(id=userprofile.companyprofile.id)
            co.phone = phone
            co.phone_country_code = country_code
            co.save()
            OPT = WhatsappOTP.objects.create(user=user)
            OPT.save()
            path = str(BASE_DIR / 'accounts/jsons/verification_msg.json')
            file_reader = open(path, 'r', encoding='UTF-8')
            data = json.loads(file_reader.read())
            msg = data['msg'].format(code=OPT.secret)

            dial_code = get_dial_code_by_country_code(co.phone_country_code)


            wa_send_msg(msg, co.phone, dial_code)
            return redirect('SendWhaCodeVerify', alt_id)

        elif VerifyProccess == '2':
            email = request.POST.get('email')
            users = User.objects.filter(email=email)
            if users.exists():
                messages.error(request, 'البريد الالكتروني مسجل من قبل الرجاء اختيار بريد اخر')
                return redirect('SignupSetupProcess', userprofile.alt_id)
            
            if email:
                user.email = email
                user.save()
                # EnableDefaultUserSubscription(userprofile.id)
                sendEmailCode(request, alt_id)
                return redirect('CompanySendEmailCodeVerify', alt_id)

        # return redirect('Login')
        return redirect('companySignupVerifyEmail', alt_id)
    
    return render(request, 'accounts/signup/Company/companySignupVerifyEmail.html', {'alt_id':alt_id, 'VerifyProccess':VerifyProccess})

def SendWhaCodeVerify(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    user=userprofile.user
    if request.method == 'POST':
        code = request.POST.get('code')
        resend = request.POST.get('resend')

        if resend:
            co = CompanyProfile.objects.get(id=userprofile.companyprofile.id)
            OPT = WhatsappOTP.objects.create(user=user)
            OPT.save()
            path = str(BASE_DIR / 'accounts/jsons/verification_msg.json')
            file_reader = open(path, 'r', encoding='UTF-8')
            data = json.loads(file_reader.read())
            msg = data['msg'].format(code=OPT.secret)
            dial_code = get_dial_code_by_country_code(co.phone_country_code)
            
            wa_send_msg(msg, co.phone, dial_code)
            return redirect('SendWhaCodeVerify', alt_id)


        if code:
            OPT = WhatsappOTP.objects.filter(user=user, secret=code, is_finshed=False)
            if OPT.exists():
                userprofile = UserProfile.objects.get(user=user)
                userprofile.is_phone_verificated = True
                userprofile.save()
                messages.success(request, 'تم تأكيد رقم الهاتف بنجاح')
                return redirect('SignupSetupProcess', alt_id)
            else:
                messages.error(request, 'رمز تأكيد رقم الهاتف خاطئ')
    return render(request, 'accounts/signup/Company/SendWhaCodeVerify.html', {'alt_id':alt_id})

def EmployeeSendWhaCodeVerify(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    user=userprofile.user
    if request.method == 'POST':
        code = request.POST.get('code')
        resend = request.POST.get('resend')
        if resend:
            co = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
            OPT = WhatsappOTP.objects.create(user=user)
            OPT.save()
            path = str(BASE_DIR / 'accounts/jsons/verification_msg.json')
            file_reader = open(path, 'r', encoding='UTF-8')
            data = json.loads(file_reader.read())
            msg = data['msg'].format(code=OPT.secret)
            dial_code = get_dial_code_by_country_code(co.phone_country_code)

            wa_send_msg(msg, co.phone, dial_code)
            return redirect('EmployeeSendWhaCodeVerify', alt_id)

        if code:
            OPTS = WhatsappOTP.objects.filter(user=user, secret=code, is_finshed=False)
            if OPTS.exists():
                
                userprofile.is_phone_verificated = True
                userprofile.save()
                OPT = OPTS.first()
                OPT.is_finshed = True
                OPT.save()
                messages.success(request, 'تم تأكيد رقم الهاتف بنجاح')
                return redirect('SignupSetupProcess', alt_id)
            else:
                messages.error(request, 'رمز تأكيد رقم الهاتف خاطئ')
    return render(request, 'accounts/signup/Employee/SendWhaCodeVerify.html', {'alt_id':alt_id})


def EmployeeSendEmailCodeVerify(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    user=userprofile.user
    if request.method == 'POST':
        code = request.POST.get('code')
        resend = request.POST.get('resend')
        if resend:
            sendEmailCode(request, alt_id)
            return redirect('EmployeeSendEmailCodeVerify', alt_id)

        if code:
            OPTS = EmailOTPModel.objects.filter(user=user, secret=code, is_finshed=False)
            if OPTS.exists():
                
                userprofile.is_email_verificated = True
                userprofile.cv_signup_process = '3'
                userprofile.save()
                OPT = OPTS.first()
                OPT.is_finshed = True
                OPT.save()
                messages.success(request, 'تم تأكيد بريد الالكتروني بنجاح')
                
                return redirect('SignupSetupProcess', alt_id)
            else:
                messages.error(request, 'رمز تأكيد بريد الالكتروني خاطئ')
    return render(request, 'accounts/signup/Employee/SendEmailCodeVerify.html', {'alt_id':alt_id})

def CompanySendEmailCodeVerify(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    user=userprofile.user
    if request.method == 'POST':
        code = request.POST.get('code')
        resend = request.POST.get('resend')
        if resend:
            sendEmailCode(request, alt_id)
            return redirect('CompanySendEmailCodeVerify', alt_id)

        if code:
            OPTS = EmailOTPModel.objects.filter(user=user, secret=code, is_finshed=False)
            if OPTS.exists():
                
                userprofile.is_email_verificated = True
                userprofile.company_signup_process = '3'
                userprofile.save()
                OPT = OPTS.first()
                OPT.is_finshed = True
                OPT.save()
                messages.success(request, 'تم تأكيد بريد الالكتروني بنجاح')
                
                return redirect('SignupSetupProcess', alt_id)
            else:
                messages.error(request, 'رمز تأكيد بريد الالكتروني خاطئ')
    return render(request, 'accounts/signup/Company/SendEmailCodeVerify.html', {'alt_id':alt_id})


def CompanyEmailVerify(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    user=userprofile.user
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            OPTS = WhatsappOTP.objects.filter(user=user, secret=code, is_finshed=False)
            if OPTS.exists():
                userprofile = UserProfile.objects.get(user=user)
                userprofile.is_phone_verificated = True
                userprofile.save()
                OPT = OPTS.first()
                OPT.is_finshed = True
                OPT.save()
                messages.success(request, 'تم تأكيد رقم الهاتف بنجاح')
                return redirect('SignupSetupProcess', alt_id)
            else:
                messages.error(request, 'رمز تأكيد رقم الهاتف خاطئ')
    return render(request, 'accounts/signup/Company/CompanyEmailVerify.html', {'alt_id':alt_id})


def SignupSetupProcess(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    if userprofile.is_company:
        process = userprofile.company_signup_process

        if process == '2':
            return companySignupVerifyEmail(request, alt_id)
        elif process == '3':
            return companySignupConf(request, alt_id)
        else:
            return redirect('Login')
        
    elif userprofile.is_employee:
        process = userprofile.cv_signup_process

        if process == '2':
            return cvSignupVerifyEmail(request, alt_id)
        elif process == '3':
            return cvSignupConf(request, alt_id)
        elif process == '4':
            return cvSignupCvCreation(request, alt_id)
        else:
            return redirect('Login')


def Login(request):
    is_signup = request.GET.get('is_signup', '')

    if request.method == 'POST':
        type = request.POST.get('type')
        email = request.POST.get('email')
        full_phone = phoneCleaner(request.POST.get('phone'))
        password = request.POST.get('password')
        if type == '2':
            email = full_phone
        if email:    
            users = User.objects.filter(email=email)
            if not users.exists():
                users = User.objects.filter(Q(userprofile__employeeprofile__phone=email) | Q(userprofile__companyprofile__phone=email))
            if users.exists():
                user = users.first()
                user = authenticate(username=user.username, password=password)
                if user is None:
                    messages.error(request, "خطاء في البريد الالكتروني او كلمة المرور")
                    return redirect('Login')
                else:
                    if not user.is_superuser:

                        userprofile = UserProfile.objects.get(user=user)
                        alt_id = userprofile.alt_id
                        if userprofile.is_employee:
                            if userprofile.cv_signup_process != '5' and userprofile.cv_signup_process != '6':
                                return redirect('SignupSetupProcess', alt_id)
                        elif userprofile.is_company:
                            if userprofile.company_signup_process != '4' and userprofile.company_signup_process != '5':
                                return redirect('SignupSetupProcess', alt_id)

                    login(request, user)
                        
                    if user.is_superuser or has_perm(user):
                        return redirect('PanelHome')
                    return redirect('index')
            else:
                messages.error(request, 'خطاء في البريد الالكتروني او كلمة المرور')
        # userprofile = UserProfile.objects.get(user=user)

        # return redirect('index',)
    return render(request, 'accounts/login/login.html', {'is_signup':is_signup})


def Logout(request):
    logout(request)
    return redirect('index')

def Profile(request, id):
    if request.user.is_authenticated: 
        
        viewer_user = request.user
        viewer_userprofile = UserProfile.objects.get(user=viewer_user)
        passed = False


        user = User.objects.get(id=id)
        userprofile = UserProfile.objects.get(user=user)
        if request.user != user:
            viewed_profiles = UserViewedProfileModel.objects.filter(profile_viewer=viewer_user, profile_viewed=user)
            if not viewed_profiles.exists():

                if viewer_userprofile.subscription:
                    
                        subscription_viewed_profile_data = viewer_userprofile.subscription_viewed_profile_data()
                        if subscription_viewed_profile_data[0]:
                            viewed_profile = UserViewedProfileModel.objects.create(profile_viewer=viewer_user, profile_viewed=user)
                            viewed_profile.creation_date = DatetimeNow(user.id)
                            viewed_profile.save()
                            viewer_sub = UserSubscriptionModel.objects.get(id=viewer_userprofile.subscription.id)
                            
                            viewer_sub.used_number_of_view_profiles += 1
                            viewer_sub.save()
                            passed =True
                        else: messages.error(request, 'يرجى تجديد الباقة او ترقيتها حتى تتمكن من الوصول الى الملف الشخصي للمستخدم')
                else:
                    messages.error(request, 'يرجى الاشتراك حتى تتمكن من الوصول الى الملف الشخصي للمستخدم')
            else:
                passed = True
        else:
            passed = True
                
        if passed:
            if userprofile.is_employee:
                return CVProfile(request, id)
            elif userprofile.is_company:
                return CPProfile(request, id)
        return redirect('index')
    else:messages.error(request, 'يرجى الاشتراك حتى تتمكن من الوصول الى الملف الشخصي للمستخدم');return redirect('Login')   
    # return render(request, 'accounts/profile/Employee/profile.html')

def CVProfile(request, id):
    UserLikeURL = reverse('UserLike', kwargs={'liked_id':id})
    UserFavURL = reverse('AddDeleteFavorite', kwargs={'receiver_id':id})
    user = User.objects.get(id=id)
    
    applier = JobAppliersModel.objects.filter(user=user)
    is_liked = UserLikeModel.objects.filter(liker=request.user, liked__id=id).exists()
    is_fav = FavoriteUserModel.objects.filter(creator=request.user, user__id=id).exists()

    userprofile = user.userprofile
    employee_profile = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
    profile_images = EmployeeProfileImages.objects.filter(user=user)
    if userprofile.cv_signup_process == '5':
        messages.error(request, 'حاليا لن يتم ظهور حسابك ضمن نتائج حتى تتم مراجعته واعتماده من قبل الادارة')
    return render(request, 'accounts/profile/Employee/profile.html', {'is_fav':is_fav, 'is_liked':is_liked, 'UserFavURL':UserFavURL, 'UserLikeURL':UserLikeURL, 'employee_profile':employee_profile, 'profile_images':profile_images, 'userprofile':userprofile, 'applier':applier})

def CPProfile(request, id):

    user = User.objects.get(id=id)
    userprofile = user.userprofile
    company_profile = userprofile.companyprofile
    jobs = JobsModel.objects.filter(user=user)
    if userprofile.cv_signup_process == '4':
        messages.error(request, 'حاليا لن تتمكن من التواصل مع صاحب السير او عرض سيرتهم حتى تتم مراجعت حسابك واعتماده من قبل الادارة')
    return render(request, 'accounts/profile/Company/profile.html', {'company_profile':company_profile, 'userprofile':userprofile, 'jobs':jobs})

def CompanySettingGernral(request):
    index_url = request.build_absolute_uri('/')
    index_url = index_url.rsplit('/', 1)[0]
    profile_reverced_url = reverse('Profile', kwargs={'id': request.user.id})
    callBackUrl = index_url+profile_reverced_url

    user = User.objects.get(id=request.user.id)
    form = CompanyProfileForm(instance=user.userprofile.companyprofile)
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, instance=user.userprofile.companyprofile)

        if form.is_valid():
            username = request.POST.get('username')
            # email = request.POST.get('email')
            img_base64 = request.POST.get('profile_img')

            # user.username = username
            # user.email = email
            # user.save()
            form2 = form.save(commit=False)
            form2.img_base64 = img_base64
            form2.save()
    return render(request, 'accounts/settings/Company/settings.html', {'form':form, 'callBackUrl':callBackUrl, 'profile_reverced_url':profile_reverced_url})


def Settings(request):
    return render(request, 'accounts/settings/Employee/settings.html')

def CVSettingsGernral(request):
    index_url = request.build_absolute_uri('/')
    index_url = index_url.rsplit('/', 1)[0]
    profile_reverced_url = reverse('Profile', kwargs={'id': request.user.id})
    callBackUrl = index_url+profile_reverced_url

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone = request.POST.get('phone')

        user = User.objects.get(id=request.user.id)
        user.email = email
        # user.username = username

        userprofile = UserProfile.objects.get(user=user)
        employee_profile = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
        employee_profile.phone = phone

        user.save()
        employee_profile.save()

    user = User.objects.get(id=request.user.id)
    userprofile = UserProfile.objects.get(user=user)
    employee_profile = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)

    return render(request, 'accounts/settings/Employee/settings.html', {'user':user, 'employee_profile':employee_profile, 'callBackUrl':callBackUrl, 'profile_reverced_url':profile_reverced_url})

def SettingsCV(request):
    healthes_status = HealthStatusModel.objects.all()
    nationalitys = NationalityModel.objects.all()
    countrys = CountrysModel.objects.all()
    skils_model = SkilsModel.objects.all()
    

    if request.method == 'POST':
        profile_imgs_list = request.POST.getlist('profile_imgs')

        full_name = request.POST.get('full_name')
        job_title = request.POST.get('job_title')
        gender = request.POST.get('gender')
        age = request.POST.get('age')

        weight = request.POST.get('weight')
        height = request.POST.get('height')
        marital_status = request.POST.get('marital_status')
        health_status = request.POST.get('health_status')
        country = request.POST.get('country')
        employee_city = request.POST.get('employee_city')
        district = request.POST.get('district')
        nationality = request.POST.get('nationality')
        have_car = request.POST.get('have_car')
        about_me = request.POST.get('about_me')
        cert_type = request.POST.get('cert_type')
        major = request.POST.get('major')
        desires = request.POST.getlist('desires')

        experiences = request.POST.getlist('experiences')
        classes = request.POST.getlist('classes')
        skils = request.POST.getlist('skils')
        lang = request.POST.getlist('lang')


        phone = request.POST.get('phone')
        facebook = extract_soshial_profile_url(request.POST.get('facebook'), 'facebook')
        linkedin = extract_soshial_profile_url(request.POST.get('linkedin'), 'linkedin')
        whatsapp = extract_soshial_profile_url(request.POST.get('whatsapp'), 'whatsapp')
        instgram = extract_soshial_profile_url(request.POST.get('instgram'), 'instgram')
        snapshat = extract_soshial_profile_url(request.POST.get('snapshat'), 'snapchat')
        tiktok = extract_soshial_profile_url(request.POST.get('tiktok'), 'tiktok')

        user = User.objects.get(id=request.user.id)
        userprofile = UserProfile.objects.get(user=user)
        employee_profile = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
        
        employee_profile.name = full_name
        employee_profile.job_title = job_title
        employee_profile.gender = gender
        employee_profile.age = age
        employee_profile.weight = weight
        employee_profile.height = height
        employee_profile.marital_status = marital_status
        employee_profile.health_status = HealthStatusModel.objects.get(id=health_status)
        employee_profile.country = countrys.get(id=country)
        employee_profile.employee_city = employee_city
        employee_profile.district = district
        employee_profile.nationality = nationalitys.get(id=nationality)
        employee_profile.have_car = have_car
        employee_profile.about_me = about_me
        employee_profile.cert_type = cert_type
        employee_profile.major = major
        employee_profile.skils = skils
        employee_profile.desires = {'desires':desires}
        employee_profile.experiences = {'desires':experiences}
        employee_profile.classes = {'desires':classes}
        employee_profile.skils = {'desires':skils}
        employee_profile.lang = {'desires':lang}

        employee_profile.phone = phone
        employee_profile.facebook = facebook
        employee_profile.linkedin = linkedin
        employee_profile.whatsapp = whatsapp
        employee_profile.instgram = instgram
        employee_profile.snapshat = snapshat
        employee_profile.tiktok = tiktok

        employee_profile.save()

        for i in EmployeeProfileImages.objects.filter(user=user):
            i.delete()
        for img_base64 in profile_imgs_list:
            profile_img = EmployeeProfileImages.objects.create(user=user, img_base64=img_base64)
            profile_img.save()

    user = User.objects.get(id=request.user.id)
    userprofile = UserProfile.objects.get(user=user)
    employee_profile = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
    profile_imgs = EmployeeProfileImages.objects.filter(user=user)
    return render(request, 'accounts/settings/Employee/settings-cv.html', {'user':user, 'employee_profile':employee_profile, 'userprofile':userprofile, 'GenderFields':GenderFields, 'NationalityFields':NationalityFields, 'CertTypeFields':CertTypeFields, 'skils_model':skils_model, 'HealthStatusFields':HealthStatusFields, 'StateFields':StateFields, 'YesNoFields':YesNoFields, 'countrys':countrys, 'profile_imgs':profile_imgs, 'nationalitys':nationalitys, 'healthes_status':healthes_status})




def getDomain(request):
    domain = get_current_site(request).domain
    return domain

def MyReferralLink(request):
    domain = getDomain(request)
    user = request.user
    userprofile = user.userprofile

    subs_url = reverse('Subscriptions')
    if userprofile.subscription:
        if userprofile.subscription.subscription.referral_link_to_earn:
            refs = ReferralLinkModel.objects.filter(creator_userprofile = userprofile)

            refs_total_earn = 0
            refs_all_total_earn = 0
            total_links = refs.count()
            total_signin_users = UserProfile.objects.filter(referral__creator_userprofile = userprofile).count()
            for ref in refs:
                refs_total_earn += ref.total_earn
                refs_all_total_earn += ref.all_total_earn
        else:
            messages.error(request, f'لتتمكن من الحصول على رابط تحقق من خلاله ارباح, يجب عليك الاشتراك في احد الباقات <a href="{subs_url}">اضغط هنا</a>')
            return redirect('Profile', user.id)
    else:
        
        messages.error(request, f'لتتمكن من الحصول على رابط تحقق من خلاله ارباح, يجب عليك الاشتراك في احد الباقات <a href="{subs_url}">اضغط هنا</a>')
        return redirect('Profile', user.id)
    
    return render(request, 'ReferralLink/MyReferralLinks.html', {'refs':refs, 'refs_total_earn':refs_total_earn, 'refs_all_total_earn':refs_all_total_earn, 'total_links':total_links, 'total_signin_users':total_signin_users, 'domain':domain})

def CreateReferralLinkForMe(request):
    user = request.user
    userprofile = user.userprofile
    alias_name = request.GET.get('alias_name')

    link = ReferralLinkModel.objects.create()
    if alias_name:
        link.alias_name = alias_name
    link.creator_userprofile = userprofile
    link.percentage_of_withdraw = 20
    link.save()
    messages.success(request, 'تم انشاء رابط أحالة بنجاح')

    return redirect('MyReferralLink')


def DeleteReferralLinkForMe(request, referral_id):
    user = request.user
    userprofile = user.userprofile

    link = ReferralLinkModel.objects.filter(creator_userprofile = userprofile, referral_id=referral_id)
    if link.exists():
        referral_id = link.first().referral_id
        link.first().delete()
        

        messages.success(request, f'تم حذف رابط أحالة {referral_id} بنجاح')

    else:
        messages.error(request, 'لن نتمكن من العثور على رابط الأحالة الخاص  بك')

    return redirect('MyReferralLink')

def WithdrawReferralLinkBalance(request, referral_id):
    user = request.user
    userprofile = user.userprofile

    links = ReferralLinkModel.objects.filter(creator_userprofile = userprofile, referral_id=referral_id)
    link = links.first()
    total_earn = link.total_earn
    userprofile.money = userprofile.money + total_earn
    link.total_earn = link.total_earn - total_earn
    link.withdraw_earn = link.withdraw_earn + total_earn
    userprofile.save()
    link.save()
    

    messages.success(request, f'تم سحب ارباح بقيمة {total_earn} بنجاح')
        
    return redirect('MyReferralLink')


def SignUpReferralLink(request, referral_id):
    request.session['referral_id'] = referral_id
    
    return redirect(reverse('Login')+'?is_signup=1')


def EnableUserSubscription(request, id):
    order = UserPaymentOrderModel.objects.get(id=id)
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    
    subscription = SubscriptionsModel.objects.get(id=order.subscription.id)

    user_subscription = UserSubscriptionModel.objects.create(subscription=subscription, price = subscription.price, number_of_days = subscription.number_of_days, number_of_receive_msgs = subscription.number_of_receive_msgs, number_of_send_msgs = subscription.number_of_send_msgs, number_of_view_profiles = subscription.number_of_view_profiles)
    user_subscription.save()

    if userprofile.subscription:
        old_user_subscription = UserSubscriptionModel.objects.get(id=userprofile.subscription.id)
        old_user_subscription.delete()

    userprofile.subscription = user_subscription
    userprofile.save()
    order.is_buyed = True
    order.save()
    messages.success(request, 'تم الاشتراك بنجاح')
    return redirect('index')


def AdminEnableUserSubscription(request):
    if request.user.is_superuser or has_perm(request.user):
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            subscription_id = request.POST.get('subscription_id')

            user = User.objects.get(username=user_id)
            userprofile = UserProfile.objects.get(user=user)

            subscription = SubscriptionsModel.objects.get(id=subscription_id)
            user_subscription = UserSubscriptionModel.objects.create(subscription=subscription, price = subscription.price, number_of_days = subscription.number_of_days, number_of_receive_msgs = subscription.number_of_receive_msgs, number_of_send_msgs = subscription.number_of_send_msgs, number_of_view_profiles = subscription.number_of_view_profiles)
            user_subscription.save()

            userprofile.subscription = user_subscription
            userprofile.save()
            messages.success(request, 'تم الاشتراك بنجاح')
    return redirect('PanelViewSubscriptions')

def DisableUserSubscription(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    userprofile.subscription = None
    userprofile.save()
    messages.success(request, 'تم الغاء اشتراك بنجاح')
    return redirect('Profile', user.id)

def EnableDefaultUserSubscription(userprofile_id):
    userprofile = UserProfile.objects.get(id=userprofile_id)
    
    subscriptions = SubscriptionsModel.objects.filter(is_default_Subscription=True)
    if subscriptions.exists():
        subscription = subscriptions.first()
        user_subscription = UserSubscriptionModel.objects.create(subscription=subscription, price = subscription.price, number_of_days = subscription.number_of_days, number_of_receive_msgs = subscription.number_of_receive_msgs, number_of_send_msgs = subscription.number_of_send_msgs, number_of_view_profiles = subscription.number_of_view_profiles)
        user_subscription.save()
        
        if userprofile.subscription:
            old_user_subscription = UserSubscriptionModel.objects.get(id=userprofile.subscription.id)
            old_user_subscription.delete()

        userprofile.subscription = user_subscription
        userprofile.save()

        return True
    return False

def EmployeeUserSubscription(request):
    return render(request, 'accounts/settings/Employee/UserSubscription.html')

def CompanyUserSubscription(request):
    return render(request, 'accounts/settings/Company/UserSubscription.html')



def EmployeeNotificationsSettings(request):
    user = request.user
    if request.method == 'POST':
        dont_receive_msg_from_companys = request.POST.get('dont_receive_msg_from_companys')
        dont_receive_msg_from_employees = request.POST.get('dont_receive_msg_from_employees')
        show_email = request.POST.get('show_email')
        show_phone = request.POST.get('show_phone')
        show_facebook = request.POST.get('show_facebook')
        show_linkedin = request.POST.get('show_linkedin')
        show_whatsapp = request.POST.get('show_whatsapp')
        show_instgram = request.POST.get('show_instgram')
        show_snapshat = request.POST.get('show_snapshat')
        show_tiktok = request.POST.get('show_tiktok')


        userprofile = UserProfile.objects.get(user=user)
        if dont_receive_msg_from_companys:
            userprofile.dont_receive_msg_from_companys = True
        else:
            userprofile.dont_receive_msg_from_companys = False

        if dont_receive_msg_from_employees:
            userprofile.dont_receive_msg_from_employees = True
        else:
            userprofile.dont_receive_msg_from_employees = False



        if show_email:
            userprofile.show_email = True
        else:
            userprofile.show_email = False

        if show_phone:
            userprofile.show_phone = True
        else:
            userprofile.show_phone = False

        if show_facebook:
            userprofile.show_facebook = True
        else:
            userprofile.show_facebook = False

        if show_linkedin:
            userprofile.show_linkedin = True
        else:
            userprofile.show_linkedin = False

        if show_whatsapp:
            userprofile.show_whatsapp = True
        else:
            userprofile.show_whatsapp = False

        if show_instgram:
            userprofile.show_instgram = True
        else:
            userprofile.show_instgram = False

        if show_snapshat:
            userprofile.show_snapshat = True
        else:
            userprofile.show_snapshat = False

        if show_tiktok:
            userprofile.show_tiktok = True
        else:
            userprofile.show_tiktok = False
        userprofile.save()

    return render(request, 'accounts/settings/Employee/notifications-settings.html')

def CompanyNotificationsSettings(request):
    user = request.user
    if request.method == 'POST':
        dont_receive_msg_from_companys = request.POST.get('dont_receive_msg_from_companys')
        dont_receive_msg_from_employees = request.POST.get('dont_receive_msg_from_employees')
        show_email = request.POST.get('show_email')
        show_phone = request.POST.get('show_phone')
        show_facebook = request.POST.get('show_facebook')
        show_linkedin = request.POST.get('show_linkedin')
        show_whatsapp = request.POST.get('show_whatsapp')
        show_instgram = request.POST.get('show_instgram')
        show_snapshat = request.POST.get('show_snapshat')
        show_tiktok = request.POST.get('show_tiktok')

        userprofile = UserProfile.objects.get(user=user)
        if dont_receive_msg_from_companys:
            userprofile.dont_receive_msg_from_companys = True
        else:
            userprofile.dont_receive_msg_from_companys = False

        if dont_receive_msg_from_employees:
            userprofile.dont_receive_msg_from_employees = True
        else:
            userprofile.dont_receive_msg_from_employees = False
            


        if show_email:
            userprofile.show_email = True
        else:
            userprofile.show_email = False

        if show_phone:
            userprofile.show_phone = True
        else:
            userprofile.show_phone = False

        if show_facebook:
            userprofile.show_facebook = True
        else:
            userprofile.show_facebook = False

        if show_linkedin:
            userprofile.show_linkedin = True
        else:
            userprofile.show_linkedin = False

        if show_whatsapp:
            userprofile.show_whatsapp = True
        else:
            userprofile.show_whatsapp = False

        if show_instgram:
            userprofile.show_instgram = True
        else:
            userprofile.show_instgram = False

        if show_snapshat:
            userprofile.show_snapshat = True
        else:
            userprofile.show_snapshat = False

        if show_tiktok:
            userprofile.show_tiktok = True
        else:
            userprofile.show_tiktok = False

        userprofile.save()

    return render(request, 'accounts/settings/Company/notifications-settings.html')

def UserPayment(request, subscription_id):
    if request.user.is_authenticated:   
        user = request.user
        userprofile = user.userprofile
        subscriptions = filter_sub_price(request, SubscriptionsModel.objects.filter(id=subscription_id))
        subscription = subscriptions[0]

        if request.method == 'POST':
            index_url = request.build_absolute_uri('/')
            callBackUrl = index_url.rsplit('/', 1)[0]
            order = UserPaymentOrderModel.objects.create(user=user, subscription=subscription)
            

            orderID = order.orderID
            
            clientName = None
            total_price_amount = float(subscription.price)
            email = user.email
            phone = None
            callBackUrl+=reverse('checkPaymentProcess', kwargs={'orderID': orderID})
            if userprofile.is_employee:phone=userprofile.employeeprofile.phone;clientName=userprofile.employeeprofile.name
            else:phone=userprofile.companyprofile.phone;clientName=userprofile.companyprofile.complite_name

            ser_title = subscription.title
            ser_disc = subscription.subtitle


            res = addInvoice(orderID, total_price_amount, email, phone, clientName, ser_title, ser_disc, callBackUrl, index_url, subscription.currency)
            if res.get('success'):
                order.transactionNo = res.get('transactionNo')
                order.save()
                return HttpResponseRedirect(res.get('url'))
    else:return redirect('Login')         
    return render(request, 'payment/pay.html', {'subscription':subscription})


def checkPaymentProcess(request, orderID):
    order = UserPaymentOrderModel.objects.get(orderID=orderID)
    r = getInvoice(order.transactionNo)
    if r.get('success'):
        if r.get('orderStatus') == 'Paid':
            buyed_user = order.user

            try:
                referrals = ReferralLinkModel.objects.filter(id=buyed_user.userprofile.referral.id)
            except:referrals=None
            
            if referrals.exists():
                referral = referrals.first()
                subscription = order.subscription
                price = subscription.price
                referral_percentage = subscription.referral_percentage_earn / 100
                total_earn = price * referral_percentage
                referral.total_earn += total_earn
                referral.save()

            return EnableUserSubscription(request, order.id)
    return redirect('index')


def UserLike(request, liked_id):
    liker = request.user
    liked = User.objects.get(id=liked_id)
    likes = UserLikeModel.objects.filter(liker=liker, liked=liked)
    if likes.exists():
        for i in likes:i.delete()
        return JsonResponse({'status':False})
    else:
        like = UserLikeModel.objects.create(liker=liker, liked=liked)
        like.save()
        return JsonResponse({'status':True})
    


def ForgetPassword(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        if type == '1':
            email = request.POST.get('email')
    
            users = User.objects.filter(email=email)
            if users.exists():
                user = users.first()
                code = ForgetPWDModel.objects.create(user=user)
                code.save()

                index_url = request.build_absolute_uri('/')
                index_url = index_url.rsplit('/', 1)[0]
                profile_reverced_url = reverse('ResetPassword', kwargs={'code': code.secret})
                callBackUrl = index_url+profile_reverced_url
                msg = f'تغير كلمة المرور من هذا الرابط : {callBackUrl}'
                subject = 'تغير كلمة المرور'
                send_mail( subject, msg, email_from, [email] )
            messages.success(request, 'اذا كان البيات التي ادخلتها صحيحاََ فسوف تستلم رابط تغير كلمة المرور عبر البريد الالكتروني')
        elif type == '2':
            phone = phoneCleaner(request.POST.get('phone'))
            country_code = request.POST.get('country_code')
            users = User.objects.filter(Q(userprofile__employeeprofile__phone=phone, userprofile__employeeprofile__phone_country_code=country_code) | Q(userprofile__companyprofile__phone=phone, userprofile__companyprofile__phone_country_code=country_code))
            if users.exists():
                user = users.first()
                userprofile = UserProfile.objects.get(user=user)
                code = ForgetPWDModel.objects.create(user=user)
                code.save()

                index_url = request.build_absolute_uri('/')
                index_url = index_url.rsplit('/', 1)[0]
                profile_reverced_url = reverse('ResetPassword', kwargs={'code': code.secret})
                callBackUrl = index_url+profile_reverced_url

                dial_code = get_dial_code_by_country_code(country_code)
                
                msg = f'تغير كلمة المرور من هذا الرابط : {callBackUrl}'
                wa_send_msg(msg, phone, dial_code)
            messages.success(request, 'اذا كان البيات التي ادخلتها صحيحاََ فسوف تستلم رابط تغير كلمة المرور عبر الواتساب')
            return redirect('ForgetPassword')

    return render(request, 'accounts/forget_password/forgetPWD.html')

def ResetPassword(request, code):
    codes = ForgetPWDModel.objects.filter(secret=code, is_finshed=False)
    if codes.exists():
        code = codes.first()
        if request.method == 'POST':
            password = request.POST.get('password')
            user = User.objects.get(id=code.user.id)
            user.set_password(password)
            user.save()
            code.is_finshed = True
            code.save()
            messages.success(request, 'تم تغير كلمة المرور بنجاح')
            return redirect('Login')
        return render(request, 'accounts/forget_password/ResetPassword.html')
    return redirect('Login')


def changePWD(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')

        user = authenticate(request, username=request.user.username, password=password)
        if user is not None:
            user = User.objects.get(id=request.user.id)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'تم تغير كلمة المرور بنجاح')
            return redirect('Login')
        else:
            messages.success(request, 'كلمة المرور الحالي الذي ادخلتها خاطئة')
    return render(request, 'accounts/forget_password/changePWD.html')




def Withdrawn(request):
    user = request.user
    withdraw = Withdraw.objects.filter(user=user)
    Pending = withdraw.filter(status__in=['0','1'])
    Completed = withdraw.filter(status='2')
    TotalAmountPendingMoney = 0
    TotalAmountWithdrawnMoney = 0

    for i in Completed:
        TotalAmountWithdrawnMoney += i.total_amount
    for i in Pending:
        TotalAmountPendingMoney += i.total_amount
        
    money_now = request.user.userprofile.money-TotalAmountPendingMoney
    if request.method == 'POST':
        data = request.POST
        withdrawn_type = data.get('withdrawn_type')
        amount = data.get('amount')
        desc = data.get('desc')

        if float(money_now) >= float(amount):
            if float(amount) >= 100:
                if withdrawn_type == '1':
                    usdt_network = data.get('usdt_network')
                    usdt_address = data.get('usdt_address')

                    obj = withdraw.create(user=user, status='0', withdrawal_method=withdrawn_type, total_amount=amount, desc=desc, usdt_network=usdt_network, usdt_address=usdt_address)
                    obj.save()
                elif withdrawn_type == '2':
                    full_name = data.get('full_name')
                    bank_name = data.get('bank_name')
                    bank_account_number = data.get('bank_account_number')
                    IBAN_number = data.get('IBAN_number')

                    obj = withdraw.create(user=user, status='0', withdrawal_method=withdrawn_type, total_amount=amount, desc=desc, full_name = full_name, bank_name = bank_name, bank_account_number = bank_account_number, IBAN_number = IBAN_number)
                    obj.save()
                return redirect('Withdrawn')
            else:
                messages.error(request, 'يجب ان تسحب على الاقل 10 دولار')

                
        else:
            messages.error(request, 'ليس لديك رصيد كافي')

            
    return render(request, 'accounts/withdraw/withdraw.html', {'withdrawal_method':withdrawal_method_list, 'usdt_network_choices':usdt_network_choices, 'withdraws':withdraw, 'TotalAmountPendingMoney':TotalAmountPendingMoney, 'TotalAmountWithdrawnMoney':TotalAmountWithdrawnMoney, 'money_now':money_now})




def change_phone(request):
    if request.method == 'POST':
        phone = phoneCleaner(request.POST.get('phone'))
        country_code = request.POST.get('country_code')

        company_profiles = CompanyProfile.objects.filter(phone=phone, phone_country_code=country_code)
        employee_profiles = EmployeeProfile.objects.filter(phone=phone, phone_country_code=country_code)
        if not employee_profiles.exists() and not company_profiles.exists():
            user = request.user
            OPT = WhatsappOTP.objects.create(user=user, phone=phone, country_code=country_code)
            OPT.save()

            path = str(BASE_DIR / 'accounts/jsons/verification_msg.json')
            file_reader = open(path, 'r', encoding='UTF-8')
            data = json.loads(file_reader.read())
            msg = data['msg'].format(code=OPT.secret)
            dial_code = get_dial_code_by_country_code(country_code)
            print(request.POST)
            if phone and dial_code:
                wa_send_msg(msg, phone, dial_code)
                messages.success(request, 'تم ارسال رمز التأكيد للرقم المدخل')
                return redirect('verify_change_phone')
        else:
            messages.error(request, 'الرقم مسجل من قبل الرجاء ادخال رقم اخر')

    return render(request, 'accounts/change_phone/change_phone.html')


def verify_change_phone(request):
    user = request.user
    userprofile = user.userprofile
    

    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            OPTS = WhatsappOTP.objects.filter(user=user, secret=code, is_finshed=False)
            if OPTS.exists():
                OPT = OPTS.first()
                redirect_user = 'index'
                if userprofile.is_company:
                    redirect_user = 'CompanySettingGernral'
                    company_profile = CompanyProfile.objects.get(id=userprofile.companyprofile.id)
                    company_profile.phone = OPT.phone
                    company_profile.phone_country_code = OPT.country_code
                    company_profile.save()
                elif userprofile.is_employee:
                    redirect_user = 'CVSettingsGernral'
                    employee_profile = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
                    employee_profile.phone = OPT.phone
                    employee_profile.phone_country_code = OPT.country_code
                    employee_profile.save()
                OPT.is_finshed = True
                OPT.save()
                
                messages.success(request, 'تم تغير وتأكيد رقم الهاتف بنجاح')
                return redirect(redirect_user)
            else:
                messages.error(request, 'رمز تأكيد رقم الهاتف خاطئ')
    return render(request, 'accounts/change_phone/verify_change_phone.html')




def change_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
                
            users = User.objects.filter(email = email)
            if not users.exists():
                user = request.user
                OPT = WhatsappOTP.objects.create(user=user, email=email)
                OPT.save()

                path = str(BASE_DIR / 'accounts/jsons/verification_msg.json')
                file_reader = open(path, 'r', encoding='UTF-8')
                data = json.loads(file_reader.read())
                subject = data['subject']
                msg = data['msg'].format(code=OPT.secret)
                send_mail( subject, msg, email_from, [email] )
                messages.success(request, 'تم ارسال رمز التأكيد للرقم المدخل')
                return redirect('verify_change_email')

            else:
                messages.error(request, 'البريد مسجل من قبل الرجاء ادخال بريد اخر')
        else:
            messages.error(request, 'ادخل بريد الكتروني صالح')

    return render(request, 'accounts/change_email/change_email.html')


def verify_change_email(request):
    user = request.user
    userprofile = user.userprofile
    

    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            OPTS = WhatsappOTP.objects.filter(user=user, secret=code, is_finshed=False)
            if OPTS.exists():
                OPT = OPTS.first()
                redirect_user = 'index'
                if userprofile.is_employee:
                    redirect_user = 'CompanySettingGernral'
                elif userprofile.is_company:
                    redirect_user = 'CVSettingsGernral'

                user = User.objects.get(id=OPT.user.id)
                user.email = OPT.email
                user.save()

                OPT.is_finshed = True
                OPT.save()
                
                messages.success(request, 'تم تغير وتأكيد البريد بنجاح')
                return redirect(redirect_user)
            else:
                messages.error(request, 'رمز تأكيد البريد خاطئ')
    return render(request, 'accounts/change_email/verify_change_email.html')
