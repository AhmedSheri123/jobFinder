from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile, EmployeeProfile, CompanyProfile, CountrysModel, SkilsModel, EmployeeProfileImages
from .fields import GenderFields, StateFields, YesNoFields, HealthStatusFields, CertTypeFields, NationalityFields
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .froms import CompanyProfileForm
# Create your views here.

def cvSignup(request):
    alt_id = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create(email=email)
        user.set_password(password)
        userprofile = UserProfile.objects.create(user=user, is_employee=True)
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

    if request.method == 'POST':
        
        userprofile.cv_signup_process = '3'
        userprofile.save()
        return redirect('SignupSetupProcess', userprofile.alt_id)
    return render(request, 'accounts/signup/Employee/cvSignupVerifyEmail.html', {'alt_id':alt_id})

def cvSignupConf(request, alt_id):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        job_title = request.POST.get('job_title')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        userprofile = UserProfile.objects.get(alt_id=alt_id)
        
        employee_profile = EmployeeProfile.objects.create(name=full_name, job_title=job_title, gender=gender, age=age)
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
        skils = request.POST.getlist('skils[]')
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
        employee_profile.skils.set(skils_model.filter(id__in=skils))
        employee_profile.desires = {'desires':desires}
        

        userprofile.cv_signup_process = '5'
        employee_profile.save()
        userprofile.save()

        return redirect('Login')
    return render(request, 'accounts/signup/Employee/cvSignupCvCreation.html', {'alt_id':alt_id, 'NationalityFields':NationalityFields, 'CertTypeFields':CertTypeFields, 'skils_model':skils_model, 'HealthStatusFields':HealthStatusFields, 'StateFields':StateFields, 'YesNoFields':YesNoFields, 'countrys':countrys})


def companySignup(request):
    alt_id = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create(email=email)
        user.set_password(password)
        userprofile = UserProfile.objects.create(user=user, is_company=True)
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
        
        company_profile = CompanyProfile.objects.create(company_name=company_name, complite_name=complite_name, employee_city=city, district=district)
        company_profile.country = countrys.get(id=country)
        company_profile.save()
        userprofile.companyprofile = company_profile
        userprofile.company_signup_process = '3'
        userprofile.save()
        return redirect('SignupSetupProcess', userprofile.alt_id)
    return render(request, 'accounts/signup/Company/companySignupConf.html', {'countrys':countrys, 'alt_id':alt_id})



def companySignupVerifyEmail(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    if request.method == 'POST':
        userprofile.company_signup_process = '4'
        userprofile.save()
    
        return redirect('Login')
    
    return render(request, 'accounts/signup/Company/companySignupVerifyEmail.html', {'alt_id':alt_id})


def SignupSetupProcess(request, alt_id):
    userprofile = UserProfile.objects.get(alt_id=alt_id)
    if userprofile.is_company:
        process = userprofile.company_signup_process

        if process == '2':
            return companySignupConf(request, alt_id)
        elif process == '3':
            return companySignupVerifyEmail(request, alt_id)
        else:
            return redirect('index')
        
    elif userprofile.is_employee:
        process = userprofile.cv_signup_process

        if process == '2':
            return cvSignupVerifyEmail(request, alt_id)
        elif process == '3':
            return cvSignupConf(request, alt_id)
        elif process == '4':
            return cvSignupCvCreation(request, alt_id)
        else:
            return redirect('index')


def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        users = User.objects.filter(email=email)
        user = users.first()

        user = authenticate(username=user.username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('Login')
        else:
            login(request, user)
            return redirect('index')

        # userprofile = UserProfile.objects.get(user=user)

        # return redirect('index',)
    return render(request, 'accounts/login/login.html')


def Logout(request):
    logout(request)
    return redirect('index')

def Profile(request):
    user = request.user
    userprofile = user.userprofile

    if userprofile.is_employee:
        return CVProfile(request)
    elif userprofile.is_company:
        return CPProfile(request)
    else:return redirect('index')
    # return render(request, 'accounts/profile/Employee/profile.html')

def CVProfile(request):
    user = request.user
    userprofile = user.userprofile
    employee_profile = EmployeeProfile.objects.get(id=userprofile.employeeprofile.id)
    profile_images = EmployeeProfileImages.objects.filter(user=user)

    return render(request, 'accounts/profile/Employee/profile.html', {'employee_profile':employee_profile, 'profile_images':profile_images})

def CPProfile(request):

    user = request.user
    userprofile = user.userprofile
    company_profile = userprofile.companyprofile

    return render(request, 'accounts/profile/Company/profile.html', {'company_profile':company_profile, 'userprofile':userprofile})

def CompanySettingGernral(request):
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
            print(img_base64)
            user.save()
            form2 = form.save(commit=False)
            form2.img_base64 = img_base64
            form2.save()
    return render(request, 'accounts/settings/Company/settings.html', {'form':form})


def Settings(request):
    return render(request, 'accounts/settings/Employee/settings.html')

def CVSettingsGernral(request):
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

    return render(request, 'accounts/settings/Employee/settings.html', {'user':user, 'employee_profile':employee_profile})

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

