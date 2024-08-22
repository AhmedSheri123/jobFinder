from django.urls import path
from . import views

urlpatterns = [
    #Employee
    path('PanelHome', views.PanelHome, name='PanelHome'),
    path('PanelShowEmployees', views.PanelShowEmployees, name='PanelShowEmployees'),
    path('PanelShowEmployee/<int:id>', views.PanelShowEmployee, name='PanelShowEmployee'),
    path('DeleteEmployees/<int:id>', views.DeleteEmployees, name='DeleteEmployees'),


    #Company
    path('Companys', views.Companys, name='Companys'),
    path('Company/<int:id>', views.Company, name='Company'),
    path('DeleteCompanys/<int:id>', views.DeleteCompanys, name='DeleteCompanys'),

    #Jobs
    path('ViewJobsPanel', views.ViewJobsPanel, name='ViewJobsPanel'),
    path('ViewCompanyPostJobs/<int:id>', views.ViewCompanyPostJobs, name='ViewCompanyPostJobs'),
    path('adminDeleteAppier/<int:id>', views.adminDeleteAppier, name='adminDeleteAppier'),
    path('adminDeleteJob/<int:id>', views.adminDeleteJob, name='adminDeleteJob'),

    #Subscriptions
    path('PanelViewSubscriptions', views.PanelViewSubscriptions, name='PanelViewSubscriptions'),
    path('PanelAddSubscriptions', views.PanelAddSubscriptions, name='PanelAddSubscriptions'),
    path('PanelEditSubscriptions/<int:id>', views.PanelEditSubscriptions, name='PanelEditSubscriptions'),
]