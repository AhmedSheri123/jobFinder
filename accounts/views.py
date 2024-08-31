from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile, EmployeeProfile, CompanyProfile, CountrysModel, SkilsModel, EmployeeProfileImages, ReferralLinkModel, SubscriptionsModel, UserSubscriptionModel, UserViewedProfileModel, CompanyRandomNumCodeGen, UserPaymentOrderModel, WhatsappOTP, EmailOTPModel, UserLikeModel, ForgetPWDModel
from .fields import GenderFields, StateFields, YesNoFields, HealthStatusFields, CertTypeFields, NationalityFields
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .froms import CompanyProfileForm
from django.contrib.sites.shortcuts import get_current_site
from .libs import DatetimeNow, get_ip_info, filter_sub_price
from .payment import addInvoice, getInvoice
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from .whatsapp import wa_send_msg
from django.core.mail import send_mail
from messenger.models import FavoriteUserModel
from django.conf import settings
from django.db.models import Q
# Create your views here.
email_from = settings.EMAIL_HOST_USER

def cvSignup(request):
    alt_id = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('full_phone')

        employee_profiles = EmployeeProfile.objects.filter(phone=phone)
        if employee_profiles.exists():
            messages.error(request, 'الرقم مسجل من قبل الرجاء تسجيل الدخول')
            return redirect('Login')

        user = User.objects.create()
        user.set_password(password)
        employee_profile = EmployeeProfile.objects.create()
        employee_profile.phone = phone

        employee_profile.save()
        userprofile = UserProfile.objects.create(user=user, is_employee=True, employeeprofile=employee_profile)
        user.username = userprofile.alt_id
        user.save()
        userprofile.cv_signup_process = '2'
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
            msg = f'رمز تاكيد رقم الهاتف هو : {OPT.secret}'
            wa_send_msg(msg, co.phone)
            return redirect('EmployeeSendWhaCodeVerify', alt_id)


    if request.method == 'POST':
        if VerifyProccess == '1':
            full_phone = request.POST.get('full_phone')
            co = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
            co.phone = full_phone
            co.save()
            OPT = WhatsappOTP.objects.create(user=user)
            OPT.save()
            msg = f'رمز تاكيد رقم الهاتف هو : {OPT.secret}'
            wa_send_msg(msg, full_phone)
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
    countrys = CountrysModel.objects.all()
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
        skils = request.POST.get('skils')
        desires = request.POST.getlist('desires')
        
        userprofile = UserProfile.objects.get(alt_id=alt_id)
        employee_profile = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
        
        employee_profile.weight = weight
        employee_profile.height = height
        employee_profile.marital_status = marital_status
        employee_profile.health_status = health_status
        employee_profile.country = countrys.get(id=country)
        employee_profile.employee_city = employee_city
        employee_profile.district = district
        employee_profile.nationality = nationality
        employee_profile.have_car = have_car
        employee_profile.about_me = about_me
        employee_profile.cert_type = cert_type
        employee_profile.major = major
        employee_profile.skils = skils
        employee_profile.desires = {'desires':desires}
        

        userprofile.cv_signup_process = '5'
        employee_profile.save()
        userprofile.save()
        EnableDefaultUserSubscription(userprofile.id)

        return redirect('Login')
    return render(request, 'accounts/signup/Employee/cvSignupCvCreation.html', {'alt_id':alt_id, 'NationalityFields':NationalityFields, 'CertTypeFields':CertTypeFields, 'skils_model':skils_model, 'HealthStatusFields':HealthStatusFields, 'StateFields':StateFields, 'YesNoFields':YesNoFields, 'countrys':countrys})


def companySignup(request):
    alt_id = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('full_phone')

        company_profiles = CompanyProfile.objects.filter(phone=phone)
        if company_profiles.exists():
            messages.error(request, 'الرقم مسجل من قبل الرجاء تسجيل الدخول')
            return redirect('Login')
        user = User.objects.create()
        user.set_password(password)
        company_profile = CompanyProfile.objects.create()
        company_profile.phone = phone
        company_profile.save()

        userprofile = UserProfile.objects.create(user=user, is_company=True, companyprofile=company_profile)
        
        user.username = userprofile.alt_id
        alt_id = userprofile.alt_id
        user.save()
        userprofile.company_signup_process = '2'
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
        return redirect('SignupSetupProcess', userprofile.alt_id)
    return render(request, 'accounts/signup/Company/companySignupConf.html', {'countrys':countrys, 'alt_id':alt_id})


def sendEmailCode(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    user = userprofile.user
    OPT = EmailOTPModel.objects.create(user=user)
    OPT.save()
    msg = f'رمز تاكيد البريد الالكتروني هو : {OPT.secret}'
    subject = 'تأكيد البريد الالكتروني'
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
            msg = f'رمز تاكيد رقم الهاتف هو : {OPT.secret}'
            wa_send_msg(msg, co.phone)
            return redirect('SendWhaCodeVerify', alt_id)



    if request.method == 'POST':

        if VerifyProccess == '1':
            full_phone = request.POST.get('full_phone')
            co = CompanyProfile.objects.get(id=userprofile.companyprofile.id)
            co.phone = full_phone
            co.save()
            OPT = WhatsappOTP.objects.create(user=user)
            OPT.save()
            msg = f'رمز تاكيد رقم الهاتف هو : {OPT.secret}'
            wa_send_msg(msg, full_phone)
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
            msg = f'رمز تاكيد رقم الهاتف هو : {OPT.secret}'
            wa_send_msg(msg, co.phone)
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
            msg = f'رمز تاكيد رقم الهاتف هو : {OPT.secret}'
            wa_send_msg(msg, co.phone)
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
    if request.method == 'POST':
        type = request.POST.get('type')
        email = request.POST.get('email')
        full_phone = request.POST.get('full_phone')
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
                            if userprofile.cv_signup_process != '5' or userprofile.cv_signup_process != '6':
                                return redirect('SignupSetupProcess', alt_id)
                        elif userprofile.is_company:
                            if userprofile.company_signup_process == '4' or userprofile.company_signup_process == '5':
                                return redirect('SignupSetupProcess', alt_id)
                    login(request, user)
                    return redirect('index')
            else:
                messages.error(request, 'خطاء في البريد الالكتروني او كلمة المرور')
        # userprofile = UserProfile.objects.get(user=user)

        # return redirect('index',)
    return render(request, 'accounts/login/login.html')


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
    

    is_liked = UserLikeModel.objects.filter(liker=request.user, liked__id=id).exists()
    is_fav = FavoriteUserModel.objects.filter(creator=request.user, user__id=id).exists()

    user = User.objects.get(id=id)
    userprofile = user.userprofile
    employee_profile = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
    profile_images = EmployeeProfileImages.objects.filter(user=user)

    return render(request, 'accounts/profile/Employee/profile.html', {'is_fav':is_fav, 'is_liked':is_liked, 'UserFavURL':UserFavURL, 'UserLikeURL':UserLikeURL, 'employee_profile':employee_profile, 'profile_images':profile_images, 'userprofile':userprofile})

def CPProfile(request, id):

    user = User.objects.get(id=id)
    userprofile = user.userprofile
    company_profile = userprofile.companyprofile

    return render(request, 'accounts/profile/Company/profile.html', {'company_profile':company_profile, 'userprofile':userprofile})

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
            email = request.POST.get('email')
            img_base64 = request.POST.get('profile_img')

            user.username = username
            user.email = email
            user.save()
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
        user.username = username

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
        skils = request.POST.get('skils')
        desires = request.POST.getlist('desires')

        phone = request.POST.get('phone')
        facebook = request.POST.get('facebook')
        linkedin = request.POST.get('linkedin')
        whatsapp = request.POST.get('whatsapp')
        instgram = request.POST.get('instgram')
        snapshat = request.POST.get('snapshat')
        tiktok = request.POST.get('tiktok')

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
        employee_profile.health_status = health_status
        employee_profile.country = countrys.get(id=country)
        employee_profile.employee_city = employee_city
        employee_profile.district = district
        employee_profile.nationality = nationality
        employee_profile.have_car = have_car
        employee_profile.about_me = about_me
        employee_profile.cert_type = cert_type
        employee_profile.major = major
        employee_profile.skils = skils
        employee_profile.desires = {'desires':desires}
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
    return render(request, 'accounts/settings/Employee/settings-cv.html', {'user':user, 'employee_profile':employee_profile, 'userprofile':userprofile, 'GenderFields':GenderFields, 'NationalityFields':NationalityFields, 'CertTypeFields':CertTypeFields, 'skils_model':skils_model, 'HealthStatusFields':HealthStatusFields, 'StateFields':StateFields, 'YesNoFields':YesNoFields, 'countrys':countrys, 'profile_imgs':profile_imgs})




def getDomain(request):
    domain = get_current_site(request).domain
    return domain

def MyReferralLink(request):
    domain = getDomain(request)
    user = request.user
    userprofile = user.userprofile

    refs = ReferralLinkModel.objects.filter(creator_userprofile = userprofile)

    refs_total_earn = 0
    refs_all_total_earn = 0
    total_links = refs.count()
    total_signin_users = UserProfile.objects.filter(referral__creator_userprofile = userprofile).count()
    for ref in refs:
        refs_total_earn += ref.total_earn
        refs_all_total_earn += ref.all_total_earn

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
    
    return redirect('cvSignup')


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
        userprofile = UserProfile.objects.get(user=user)
        if dont_receive_msg_from_companys:
            userprofile.dont_receive_msg_from_companys = True
        else:
            userprofile.dont_receive_msg_from_companys = False

        if dont_receive_msg_from_employees:
            userprofile.dont_receive_msg_from_employees = True
        else:
            userprofile.dont_receive_msg_from_employees = False

        userprofile.save()

    return render(request, 'accounts/settings/Employee/notifications-settings.html')

def CompanyNotificationsSettings(request):
    user = request.user
    if request.method == 'POST':
        dont_receive_msg_from_companys = request.POST.get('dont_receive_msg_from_companys')
        dont_receive_msg_from_employees = request.POST.get('dont_receive_msg_from_employees')
        userprofile = UserProfile.objects.get(user=user)
        if dont_receive_msg_from_companys:
            userprofile.dont_receive_msg_from_companys = True
        else:
            userprofile.dont_receive_msg_from_companys = False

        if dont_receive_msg_from_employees:
            userprofile.dont_receive_msg_from_employees = True
        else:
            userprofile.dont_receive_msg_from_employees = False
            
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
            phone = request.POST.get('full_phone')
            users = User.objects.filter(Q(userprofile__employeeprofile__phone=phone) | Q(userprofile__companyprofile__phone=phone))
            if users.exists():
                user = users.first()
                userprofile = UserProfile.objects.get(user=user)
                code = ForgetPWDModel.objects.create(user=user)
                code.save()

                index_url = request.build_absolute_uri('/')
                index_url = index_url.rsplit('/', 1)[0]
                profile_reverced_url = reverse('ResetPassword', kwargs={'code': code.secret})
                callBackUrl = index_url+profile_reverced_url

                msg = f'تغير كلمة المرور من هذا الرابط : {callBackUrl}'
                wa_send_msg(msg, phone)
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