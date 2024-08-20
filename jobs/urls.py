from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='JobIndex'),
    path('viewJob/<int:id>', views.viewJob, name='viewJob'),

    #company
    path('companyJobs', views.companyJobs, name='companyJobs'),
    path('companyviewJob/<int:id>', views.companyviewJob, name='companyviewJob'),
    path('companyCreateJob', views.companyCreateJob, name='companyCreateJob'),
    path('companyCloseJob/<int:id>', views.companyCloseJob, name='companyCloseJob'),
    path('companyOpenJob/<int:id>', views.companyOpenJob, name='companyOpenJob'),

    path('applyJob/<int:job_id>', views.applyJob, name='applyJob'),
]