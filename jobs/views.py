from django.shortcuts import render, redirect
from .models import JobsModel, JobAppliersModel
from .forms import JobsModelForm
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
# Create your views here.

def index(request):
    jobs = JobsModel.objects.filter(Q(state='1') | Q(state='2'))
    return render(request, 'jobs/index.html', {'jobs':jobs})

def viewJob(request, id):
    job = JobsModel.objects.get(id=id)
    appliers = JobAppliersModel.objects.filter(job=job)
    return render(request, 'jobs/viewJob.html', {'job':job, 'appliers':appliers})

def companyJobs(request):
    user = request.user
    jobs = JobsModel.objects.filter(user=user)

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
            messages.success(request, 'طلبك قيد المراجعة سوف يتم النشر في حال الموافقة عليه من قبل الادارة')
            return redirect('companyJobs')
    return render(request, 'jobs/company/CreateJob.html', {'form':form})

def companyCloseJob(request, id):
    job = JobsModel.objects.get(id=id)
    job.state = '2'
    job.save()
    return redirect('companyJobs')


def companyOpenJob(request, id):
    job = JobsModel.objects.get(id=id)
    job.state = '0'
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
                applier = JobAppliersModel.objects.create(user=user, job=job, msg=msg)
                applier.creation_date = timezone.now()
                applier.save()

            return redirect('viewJob', job_id)
    else:return redirect('Login')   