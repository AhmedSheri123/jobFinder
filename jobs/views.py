from django.shortcuts import render, redirect
from .models import JobsModel, JobAppliersModel, JobSalariesModel
from .forms import JobsModelForm, JobSalariesModelForm
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from accounts.libs import filter_job_msg, add_get_user_ip

# Create your views here.

def index(request):
    ip_info = add_get_user_ip(request)
    country_code = ip_info.get('isocode')

    jobs = JobsModel.objects.filter(Q(state='1', country__name=str(country_code).upper()) | Q(state='2'), country__name=str(country_code).upper())
    return render(request, 'jobs/index.html', {'jobs':jobs})

def viewJob(request, id):
    user = request.user
    if user.is_authenticated:
        userprofile = user.userprofile
        if userprofile.is_has_subscription:
            job = JobsModel.objects.get(id=id)
            appliers = JobAppliersModel.objects.filter(job=job)
            return render(request, 'jobs/viewJob.html', {'job':job, 'appliers':appliers})
        else:
            messages.error('يرجى اشتراك باحد الباقات لتتمكن من تقديم على الوظائف')
            return redirect('JobIndex')
    else:
        messages.error('يرجى تسجيل الدخول او انشاء حساب')
        return redirect('JobIndex')
    
def companyJobs(request):
    user = request.user
    jobs = JobsModel.objects.filter(user=user)
    if request.user.userprofile.company_signup_process != '5':
        messages.error(request, 'لا يمكنك اضافة وظائف حالية لان حسابك قيد المراجعة الرجاء الانتظار حتى يتم اكمال مراجعة حسابك')
    return render(request, 'jobs/company/Jobs.html', {'jobs':jobs})

def companyviewJob(request, id):
    job = JobsModel.objects.get(id=id)
    appliers = JobAppliersModel.objects.filter(job=job)
    
    return render(request, 'jobs/company/viewJob.html', {'job':job, 'appliers':appliers})

def companyCreateJob(request):
    user = request.user
    form = JobsModelForm()

    if request.method == 'POST':
        form = JobsModelForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = user
            job.creation_date = timezone.now()
            job.save()
            messages.success(request, 'لقد تم استلام طلبك وهو قيد المراجعة الان وقد يستغرق ذلك ٢٤ ساعة . ستصلكم اشعار عند اعتمادة')
            return redirect('companyJobs')
    return render(request, 'jobs/company/CreateJob.html', {'form':form})

def companyEditJob(request, id):
    job = JobsModel.objects.get(id=id)
    form = JobsModelForm(instance=job)

    if request.method == 'POST':
        form = JobsModelForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            job.has_complited = False
            job.state = '0'
            job.save()
            messages.success(request, 'لقد تم استلام طلبك وهو قيد المراجعة الان وقد يستغرق ذلك ٢٤ ساعة . ستصلكم اشعار عند اعتمادة')
            return redirect('companyJobs')
    return render(request, 'jobs/company/EditJob.html', {'form':form})

def companyCloseJob(request, id):
    job = JobsModel.objects.get(id=id)
    job.state = '2'
    job.save()
    return redirect('companyJobs')


def companyOpenJob(request, id):
    job = JobsModel.objects.get(id=id)
    if job.has_complited:
        job.state = '1'
    else:job.state = '0'
    
    job.save()
    return redirect('companyJobs')

def applyJob(request, job_id):
    if request.user.is_authenticated:
            
        user = request.user
        if request.method == 'POST':
            job = JobsModel.objects.get(id=job_id)
            msg = request.POST.get('msg')
            appliers = JobAppliersModel.objects.filter(user=user, job=job)
            if not appliers.exists():
                msg = filter_job_msg(msg)
                applier = JobAppliersModel.objects.create(user=user, job=job, msg=msg)
                applier.creation_date = timezone.now()
                applier.save()

            return redirect('viewJob', job_id)
    else:return redirect('Login')


