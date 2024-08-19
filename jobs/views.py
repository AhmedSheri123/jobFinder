from django.shortcuts import render, redirect
from .models import JobsModel, JobAppliersModel

# Create your views here.

def index(request):
    return render(request, 'jobs/index.html')

def viewJob(request, id):
    return render(request, 'jobs/viewJob.html')

def companyJobs(request):
    return render(request, 'jobs/company/Jobs.html')

def companyviewJob(request):
    return render(request, 'jobs/company/viewJob.html')

def companyCreateJob(request):
    return render(request, 'jobs/company/CreateJob.html')
