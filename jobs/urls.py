from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='JobIndex'),
    path('viewJob/<int:id>', views.viewJob, name='viewJob'),

    #company
    path('companyJobs', views.companyJobs, name='companyJobs'),
    path('companyviewJob', views.companyviewJob, name='companyviewJob'),
    path('companyCreateJob', views.companyCreateJob, name='companyCreateJob'),
]